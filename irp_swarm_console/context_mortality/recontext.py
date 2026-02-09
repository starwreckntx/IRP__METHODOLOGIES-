"""
Recontext Sweeps — Phase 3
===========================
Periodically re-scans original chat transcripts to recover information
that was incorrectly dropped, degraded below a fidelity threshold, or
newly relevant due to changed context.

Sweep algorithm (from spec Section 3.4):
  1. SCOPE DEFINITION — user specifies time range, topics, session IDs
  2. TRANSCRIPT SCAN — extract semantic units, compare against memory
  3. GAP CLASSIFICATION — categorize what's missing and why
  4. RECOVERY PROPOSAL — ranked list with consent gate
  5. USER REVIEW — accept / reject / modify before reinstatement
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .models import (
    AppealStatus,
    GapType,
    RecoveryProposal,
    SemanticUnit,
    SweepTrigger,
)
from .cda import ContextDeathAudit
from .path_tracer import FidelityScorer, PathTracer
from .sovereignty import SovereigntyClassifier


class SweepScope:
    """Defines the scope of a recontext sweep."""

    def __init__(
        self,
        session_ids: Optional[List[str]] = None,
        topic_keywords: Optional[List[str]] = None,
        time_range_start: Optional[str] = None,
        time_range_end: Optional[str] = None,
        full_sweep: bool = False,
    ):
        self.session_ids = session_ids or []
        self.topic_keywords = [kw.lower() for kw in (topic_keywords or [])]
        self.time_range_start = time_range_start
        self.time_range_end = time_range_end
        self.full_sweep = full_sweep

    def matches_session(self, session_id: str) -> bool:
        if self.full_sweep:
            return True
        if not self.session_ids:
            return True
        return session_id in self.session_ids

    def matches_time(self, timestamp: str) -> bool:
        if self.full_sweep:
            return True
        if self.time_range_start and timestamp < self.time_range_start:
            return False
        if self.time_range_end and timestamp > self.time_range_end:
            return False
        return True

    def matches_topic(self, text: str) -> bool:
        if self.full_sweep:
            return True
        if not self.topic_keywords:
            return True
        text_lower = text.lower()
        return any(kw in text_lower for kw in self.topic_keywords)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_ids": self.session_ids,
            "topic_keywords": self.topic_keywords,
            "time_range_start": self.time_range_start,
            "time_range_end": self.time_range_end,
            "full_sweep": self.full_sweep,
        }


class RecontextSweep:
    """
    Executes recontext sweeps against transcript data, CDA graveyard,
    and current memory state to identify recoverable context gaps.
    """

    def __init__(
        self,
        cda: ContextDeathAudit,
        path_tracer: PathTracer,
        results_dir: Optional[str] = None,
        embed_fn=None,
    ):
        self.cda = cda
        self.path_tracer = path_tracer
        self.classifier = SovereigntyClassifier()
        self.scorer = FidelityScorer(embed_fn=embed_fn)

        if results_dir is None:
            results_dir = str(Path(__file__).parent / "sweep_results")
        self.results_dir = Path(results_dir)
        self.results_dir.mkdir(parents=True, exist_ok=True)

    # ------------------------------------------------------------------
    # Core sweep
    # ------------------------------------------------------------------

    def execute_sweep(
        self,
        transcripts: List[Dict[str, Any]],
        current_memory_items: List[str],
        scope: SweepScope,
        trigger: str = SweepTrigger.MANUAL.value,
        fidelity_threshold: float = 0.5,
    ) -> Dict[str, Any]:
        """
        Execute a full recontext sweep.

        Args:
            transcripts: List of transcript dicts, each containing:
                - session_id: str
                - messages: List[Dict] (role + content + optional timestamp)
            current_memory_items: List of strings representing what's
                currently in memory (userMemories + memory_user_edits).
            scope: SweepScope defining what to scan.
            trigger: What triggered this sweep.
            fidelity_threshold: Below this score, items are considered
                degraded.

        Returns:
            Sweep result dict with proposals, gaps, and statistics.
        """
        sweep_id = str(uuid.uuid4())
        sweep_timestamp = datetime.utcnow().isoformat() + "Z"

        # 1. Extract semantic units from transcripts within scope
        transcript_units = self._scan_transcripts(transcripts, scope)

        # 2. Build current memory set for comparison
        memory_set = set(m.lower().strip() for m in current_memory_items if m)

        # 3. Load CDA graveyard
        graveyard_hashes: Set[str] = set()
        for dropped in self.cda.get_graveyard():
            graveyard_hashes.add(dropped.content_hash)

        # 4. Identify gaps
        gaps = self._identify_gaps(
            transcript_units,
            memory_set,
            graveyard_hashes,
            fidelity_threshold,
        )

        # 5. Generate recovery proposals
        proposals = self._generate_proposals(gaps)

        # 6. Build result
        result = {
            "sweep_id": sweep_id,
            "timestamp": sweep_timestamp,
            "trigger": trigger,
            "scope": scope.to_dict(),
            "stats": {
                "transcripts_scanned": len(transcripts),
                "units_extracted": len(transcript_units),
                "gaps_found": len(gaps),
                "proposals_generated": len(proposals),
                "current_memory_size": len(current_memory_items),
                "graveyard_size": len(graveyard_hashes),
            },
            "gaps": [g.to_dict() for g in gaps],
            "proposals": [p.to_dict() for p in proposals],
        }

        # Persist result
        self._persist_result(sweep_id, result)

        return result

    # ------------------------------------------------------------------
    # Transcript scanning
    # ------------------------------------------------------------------

    def _scan_transcripts(
        self,
        transcripts: List[Dict[str, Any]],
        scope: SweepScope,
    ) -> List[SemanticUnit]:
        """
        Extract semantic units from transcripts, filtered by scope.
        """
        units: List[SemanticUnit] = []

        for transcript in transcripts:
            session_id = transcript.get("session_id", "unknown")
            if not scope.matches_session(session_id):
                continue

            messages = transcript.get("messages", [])
            extracted = ContextDeathAudit.extract_semantic_units(
                messages, session_id
            )

            for unit in extracted:
                if not scope.matches_time(unit.timestamp):
                    continue
                if not scope.matches_topic(unit.content):
                    continue

                # Classify sovereignty
                unit.sovereignty_class = self.classifier.classify(unit.content)
                units.append(unit)

        return units

    # ------------------------------------------------------------------
    # Gap identification
    # ------------------------------------------------------------------

    def _identify_gaps(
        self,
        transcript_units: List[SemanticUnit],
        memory_set: Set[str],
        graveyard_hashes: Set[str],
        fidelity_threshold: float,
    ) -> List["_Gap"]:
        """
        Compare transcript units against current memory and CDA graveyard.
        """
        gaps: List[_Gap] = []

        for unit in transcript_units:
            # Check if content exists in current memory (fuzzy)
            in_memory = self._fuzzy_match_memory(unit.content, memory_set)

            if in_memory:
                # Check fidelity — is the memory representation degraded?
                best_fidelity = max(
                    self.scorer.compute_fidelity(unit.content, mem)
                    for mem in memory_set
                    if self._partial_match(unit.content, mem)
                ) if any(
                    self._partial_match(unit.content, mem)
                    for mem in memory_set
                ) else 1.0

                if best_fidelity < fidelity_threshold:
                    gaps.append(
                        _Gap(
                            unit=unit,
                            gap_type=GapType.DEGRADED.value,
                            fidelity=best_fidelity,
                        )
                    )
            else:
                # Not in memory — check if it was previously dropped
                if unit.content_hash in graveyard_hashes:
                    gaps.append(
                        _Gap(
                            unit=unit,
                            gap_type=GapType.PREVIOUSLY_DROPPED.value,
                            fidelity=0.0,
                        )
                    )
                else:
                    gaps.append(
                        _Gap(
                            unit=unit,
                            gap_type=GapType.NEVER_CAPTURED.value,
                            fidelity=0.0,
                        )
                    )

        return gaps

    @staticmethod
    def _fuzzy_match_memory(content: str, memory_set: Set[str]) -> bool:
        """Check if content has a reasonable match in memory."""
        content_lower = content.lower().strip()
        # Check for significant token overlap
        content_tokens = set(content_lower.split())
        if len(content_tokens) < 3:
            return content_lower in memory_set

        for mem in memory_set:
            mem_tokens = set(mem.split())
            overlap = content_tokens & mem_tokens
            if len(overlap) >= len(content_tokens) * 0.5:
                return True
        return False

    @staticmethod
    def _partial_match(content: str, memory_item: str) -> bool:
        """Check for partial token overlap between content and memory."""
        c_tokens = set(content.lower().split())
        m_tokens = set(memory_item.lower().split())
        overlap = c_tokens & m_tokens
        return len(overlap) >= min(3, len(c_tokens) * 0.3)

    # ------------------------------------------------------------------
    # Proposal generation
    # ------------------------------------------------------------------

    def _generate_proposals(self, gaps: List["_Gap"]) -> List[RecoveryProposal]:
        """Generate ranked recovery proposals from identified gaps."""
        proposals: List[RecoveryProposal] = []

        for gap in gaps:
            unit = gap.unit
            # Skip health-classified items — require explicit opt-in
            if self.classifier.requires_explicit_consent(unit.sovereignty_class):
                continue

            # Compute relevance score (simple heuristic: content length
            # and gap type severity)
            relevance = self._compute_relevance(gap)

            proposal = RecoveryProposal(
                original_verbatim=unit.content,
                proposed_memory_form=self._compress_for_memory(unit.content),
                fidelity_score=gap.fidelity,
                relevance_score=relevance,
                gap_type=gap.gap_type,
                source_session_id=unit.session_id,
                source_turn=unit.turn_index,
                sovereignty_class=unit.sovereignty_class,
            )
            proposals.append(proposal)

        # Sort by relevance (highest first)
        proposals.sort(key=lambda p: p.relevance_score, reverse=True)

        return proposals

    @staticmethod
    def _compute_relevance(gap: "_Gap") -> float:
        """
        Compute a relevance score for a gap.
        Higher = more important to recover.
        """
        base = 0.5
        # Previously dropped items are more concerning than never-captured
        type_weights = {
            GapType.PREVIOUSLY_DROPPED.value: 0.3,
            GapType.DEGRADED.value: 0.2,
            GapType.NEVER_CAPTURED.value: 0.1,
            GapType.NEWLY_RELEVANT.value: 0.4,
        }
        base += type_weights.get(gap.gap_type, 0.0)

        # Penalize very short content (less likely to be meaningful)
        content_len = len(gap.unit.content)
        if content_len > 200:
            base += 0.1
        elif content_len < 20:
            base -= 0.2

        return max(0.0, min(1.0, base))

    @staticmethod
    def _compress_for_memory(verbatim: str, max_chars: int = 200) -> str:
        """
        Compress verbatim text into a memory-suitable form.
        Respects the 200-char constraint for memory_user_edits.
        """
        if len(verbatim) <= max_chars:
            return verbatim
        # Truncate with ellipsis, preserving start
        return verbatim[: max_chars - 3] + "..."

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _persist_result(self, sweep_id: str, result: Dict[str, Any]) -> Path:
        """Write sweep results to a JSON file."""
        filepath = self.results_dir / f"sweep_{sweep_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        return filepath

    def list_sweep_results(self) -> List[Path]:
        """List all sweep result files."""
        return sorted(self.results_dir.glob("sweep_*.json"))

    def load_sweep_result(self, filepath: str) -> Dict[str, Any]:
        """Load a sweep result from JSON."""
        with open(filepath, "r", encoding="utf-8") as f:
            return json.load(f)


class _Gap:
    """Internal representation of a context gap found during sweep."""

    def __init__(
        self,
        unit: SemanticUnit,
        gap_type: str,
        fidelity: float,
    ):
        self.unit = unit
        self.gap_type = gap_type
        self.fidelity = fidelity

    def to_dict(self) -> Dict[str, Any]:
        return {
            "unit": self.unit.to_dict(),
            "gap_type": self.gap_type,
            "fidelity": self.fidelity,
        }
