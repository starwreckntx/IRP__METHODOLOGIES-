"""
Path Tracer — Phase 2
=====================
Tracks the lifecycle of any discrete piece of information from its
origin (verbatim user input) through every transformation (compaction,
synthesis, memory generation) to its current state or point of death.

Provides fidelity scoring via text similarity (fallback to token-level
overlap when embedding models are unavailable) and maintains the full
transformation chain for audit.
"""

import hashlib
import json
import re
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    ContextPathTrace,
    ItemStatus,
    Transformation,
    TransformationType,
)


class FidelityScorer:
    """
    Computes semantic fidelity between original verbatim and transformed
    representations.

    Uses token-level Jaccard similarity as a baseline.  When an external
    embedding function is provided, uses cosine similarity on embeddings
    instead (higher accuracy).
    """

    def __init__(self, embed_fn=None):
        """
        Args:
            embed_fn: Optional callable(str) -> List[float] that returns
                      an embedding vector.  If None, falls back to
                      token-level Jaccard similarity.
        """
        self.embed_fn = embed_fn

    def compute_fidelity(self, original: str, transformed: str) -> float:
        """
        Semantic similarity between original verbatim and current
        representation.

        Returns:
            0.0 (total loss) to 1.0 (verbatim preservation).
        """
        if not original or not transformed:
            return 0.0

        if original == transformed:
            return 1.0

        if self.embed_fn is not None:
            return self._embedding_similarity(original, transformed)

        return self._token_jaccard(original, transformed)

    # ------------------------------------------------------------------
    # Similarity backends
    # ------------------------------------------------------------------

    def _token_jaccard(self, a: str, b: str) -> float:
        """Token-level Jaccard similarity (bag-of-words baseline)."""
        tokens_a = set(self._tokenize(a))
        tokens_b = set(self._tokenize(b))
        if not tokens_a and not tokens_b:
            return 1.0
        intersection = tokens_a & tokens_b
        union = tokens_a | tokens_b
        return len(intersection) / len(union) if union else 0.0

    def _embedding_similarity(self, a: str, b: str) -> float:
        """Cosine similarity using externally supplied embeddings."""
        vec_a = self.embed_fn(a)
        vec_b = self.embed_fn(b)
        dot = sum(x * y for x, y in zip(vec_a, vec_b))
        norm_a = sum(x * x for x in vec_a) ** 0.5
        norm_b = sum(x * x for x in vec_b) ** 0.5
        if norm_a == 0 or norm_b == 0:
            return 0.0
        return max(0.0, min(1.0, dot / (norm_a * norm_b)))

    @staticmethod
    def _tokenize(text: str) -> List[str]:
        """Simple whitespace + punctuation tokenizer."""
        return [t.lower() for t in re.findall(r"\w+", text)]


class PathTracer:
    """
    Maintains a registry of ContextPathTrace objects and provides
    lookup, update, and query capabilities.

    Storage: JSONL file (one trace per line), consistent with the GAM
    pattern used elsewhere in the codebase.
    """

    def __init__(
        self,
        store_path: Optional[str] = None,
        embed_fn=None,
    ):
        if store_path is None:
            store_path = str(Path(__file__).parent / "path_traces.jsonl")
        self.store_path = Path(store_path)
        self.scorer = FidelityScorer(embed_fn=embed_fn)
        self.traces: Dict[str, ContextPathTrace] = {}
        self._load()

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _load(self) -> None:
        """Load existing traces from the JSONL store."""
        if not self.store_path.exists():
            return
        with open(self.store_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    trace = ContextPathTrace.from_dict(data)
                    self.traces[trace.origin_content_hash] = trace
                except (json.JSONDecodeError, TypeError):
                    continue

    def _persist(self) -> None:
        """Rewrite the full JSONL store from in-memory state."""
        with open(self.store_path, "w", encoding="utf-8") as f:
            for trace in self.traces.values():
                f.write(
                    json.dumps(trace.to_dict(), ensure_ascii=False) + "\n"
                )

    def _append(self, trace: ContextPathTrace) -> None:
        """Append a single trace to the JSONL store."""
        with open(self.store_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(trace.to_dict(), ensure_ascii=False) + "\n")

    # ------------------------------------------------------------------
    # Registration
    # ------------------------------------------------------------------

    def register_origin(
        self,
        session_id: str,
        turn_index: int,
        timestamp: str,
        verbatim: str,
    ) -> ContextPathTrace:
        """
        Register a new piece of context at its origin point.

        If a trace with the same content hash already exists, returns
        the existing trace.

        Args:
            session_id: Source session.
            turn_index: Turn number within the session.
            timestamp: ISO 8601 timestamp.
            verbatim: The original verbatim text.

        Returns:
            The new or existing ContextPathTrace.
        """
        content_hash = hashlib.sha256(verbatim.encode("utf-8")).hexdigest()

        if content_hash in self.traces:
            return self.traces[content_hash]

        trace = ContextPathTrace(
            origin_session_id=session_id,
            origin_turn_index=turn_index,
            origin_timestamp=timestamp,
            origin_verbatim=verbatim,
            origin_content_hash=content_hash,
            current_status=ItemStatus.ALIVE.value,
            recovery_path=f"transcript://{session_id}/turn/{turn_index}",
        )
        self.traces[content_hash] = trace
        self._append(trace)
        return trace

    # ------------------------------------------------------------------
    # Transformation recording
    # ------------------------------------------------------------------

    def record_transformation(
        self,
        content_hash: str,
        event: str,
        survived: bool,
        transformed_form: Optional[str] = None,
        reason: Optional[str] = None,
    ) -> Optional[ContextPathTrace]:
        """
        Record a transformation event for a tracked context item.

        Computes fidelity score between the original verbatim and the
        new transformed form (if provided).

        Args:
            content_hash: SHA-256 hash of the original content.
            event: TransformationType value.
            survived: Whether the item survived this transformation.
            transformed_form: The new representation after transformation.
            reason: Why the transformation happened.

        Returns:
            The updated ContextPathTrace, or None if not found.
        """
        trace = self.traces.get(content_hash)
        if trace is None:
            return None

        fidelity = 0.0
        if transformed_form:
            fidelity = self.scorer.compute_fidelity(
                trace.origin_verbatim, transformed_form
            )

        transformation = Transformation(
            event=event,
            timestamp=datetime.utcnow().isoformat() + "Z",
            survived=survived,
            transformed_form=transformed_form,
            fidelity_score=round(fidelity, 4),
            reason=reason,
        )
        trace.add_transformation(transformation)

        if not survived:
            trace.current_status = ItemStatus.DEAD.value
            trace.last_seen_in = event

        self._persist()
        return trace

    def record_death(
        self,
        content_hash: str,
        event: str,
        reason: Optional[str] = None,
    ) -> Optional[ContextPathTrace]:
        """Convenience method: record a transformation where item died."""
        return self.record_transformation(
            content_hash=content_hash,
            event=event,
            survived=False,
            transformed_form=None,
            reason=reason,
        )

    def record_recovery(
        self,
        content_hash: str,
        recovered_form: str,
    ) -> Optional[ContextPathTrace]:
        """Record that a previously dead item has been recovered."""
        trace = self.traces.get(content_hash)
        if trace is None:
            return None

        fidelity = self.scorer.compute_fidelity(
            trace.origin_verbatim, recovered_form
        )
        transformation = Transformation(
            event=TransformationType.RECONTEXT_RECOVERY.value,
            timestamp=datetime.utcnow().isoformat() + "Z",
            survived=True,
            transformed_form=recovered_form,
            fidelity_score=round(fidelity, 4),
            reason="recontext_recovery",
        )
        trace.add_transformation(transformation)
        trace.current_status = ItemStatus.RECOVERED.value
        self._persist()
        return trace

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def lookup(self, content_hash: str) -> Optional[ContextPathTrace]:
        """Look up a trace by content hash."""
        return self.traces.get(content_hash)

    def search(self, keyword: str) -> List[ContextPathTrace]:
        """
        Search traces by keyword match against the original verbatim.

        Args:
            keyword: Case-insensitive search term.

        Returns:
            Matching traces.
        """
        keyword_lower = keyword.lower()
        return [
            t
            for t in self.traces.values()
            if keyword_lower in t.origin_verbatim.lower()
        ]

    def get_dead_items(self) -> List[ContextPathTrace]:
        """Return all traces with DEAD status."""
        return [
            t
            for t in self.traces.values()
            if t.current_status == ItemStatus.DEAD.value
        ]

    def get_alive_items(self) -> List[ContextPathTrace]:
        """Return all traces with ALIVE status."""
        return [
            t
            for t in self.traces.values()
            if t.current_status == ItemStatus.ALIVE.value
        ]

    def get_fidelity_report(self) -> Dict[str, Any]:
        """
        Generate a summary of fidelity scores across all tracked items.

        Returns:
            Report dict with min/max/mean fidelity, counts by status, etc.
        """
        fidelity_values: List[float] = []
        status_counts: Counter = Counter()

        for trace in self.traces.values():
            status_counts[trace.current_status] += 1
            curve = trace.get_fidelity_curve()
            if curve:
                fidelity_values.append(curve[-1])  # Latest fidelity

        mean_fidelity = (
            sum(fidelity_values) / len(fidelity_values)
            if fidelity_values
            else 0.0
        )

        return {
            "total_tracked": len(self.traces),
            "status_counts": dict(status_counts),
            "fidelity_stats": {
                "mean": round(mean_fidelity, 4),
                "min": round(min(fidelity_values), 4) if fidelity_values else 0.0,
                "max": round(max(fidelity_values), 4) if fidelity_values else 0.0,
                "count": len(fidelity_values),
            },
            "store_path": str(self.store_path),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Alias for get_fidelity_report."""
        return self.get_fidelity_report()
