"""
Context Death Audit (CDA) — Phase 1
====================================
Logs every piece of information evaluated and dropped during compaction
or synthesis, creating a recoverable "graveyard" of discarded context.

Operates as a diff layer between pre-compression and post-compression
states.  Produces structured JSON audit logs stored in a user-controlled
location.

Closed-box constraint: The actual compaction function is server-side.
This module implements the practical alternative described in the spec:
  1. Snapshot full context window state before compaction triggers
  2. Snapshot post-compaction summary
  3. Diff the two to produce the CDA log
  4. Store the diff with full provenance metadata
"""

import hashlib
import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set

from .models import (
    CDALog,
    ContextSnapshot,
    DroppedItem,
    SemanticUnit,
)
from .sovereignty import SovereigntyClassifier


class ContextDeathAudit:
    """
    Core CDA engine.

    Captures pre- and post-compaction states, diffs them,
    and persists the resulting death log as structured JSON.
    """

    def __init__(
        self,
        session_id: str,
        user_id: str,
        log_dir: Optional[str] = None,
    ):
        self.session_id = session_id
        self.user_id = user_id
        self.classifier = SovereigntyClassifier()

        if log_dir is None:
            log_dir = str(Path(__file__).parent / "cda_logs")
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(parents=True, exist_ok=True)

        self.pre_compaction_snapshot: Optional[ContextSnapshot] = None
        self.post_compaction_snapshot: Optional[ContextSnapshot] = None
        self.dropped_items: List[DroppedItem] = []
        self.retained_items: List[SemanticUnit] = []

    # ------------------------------------------------------------------
    # Semantic unit extraction
    # ------------------------------------------------------------------

    @staticmethod
    def extract_semantic_units(
        context_window: List[Dict[str, Any]],
        session_id: str = "",
    ) -> List[SemanticUnit]:
        """
        Extract discrete semantic units from a context window.

        Each message/turn in the context window is treated as one or more
        semantic units.  This is a deliberately simple extraction that
        treats each turn as a single unit; downstream callers may
        split turns further for finer granularity.

        Args:
            context_window: List of message dicts (role + content).
            session_id: Session identifier for provenance.

        Returns:
            List of SemanticUnit instances.
        """
        units: List[SemanticUnit] = []
        for idx, msg in enumerate(context_window):
            content = msg.get("content", "")
            if isinstance(content, list):
                # Handle multi-part content blocks
                content = " ".join(
                    block.get("text", "")
                    for block in content
                    if isinstance(block, dict)
                )
            if not content or not content.strip():
                continue

            timestamp = msg.get("timestamp", datetime.utcnow().isoformat() + "Z")
            units.append(
                SemanticUnit(
                    content=content.strip(),
                    turn_index=idx,
                    timestamp=timestamp,
                    session_id=session_id,
                )
            )
        return units

    # ------------------------------------------------------------------
    # Snapshot capture
    # ------------------------------------------------------------------

    def capture_pre_state(self, context_window: List[Dict[str, Any]]) -> ContextSnapshot:
        """
        Capture full context before compaction triggers.

        Args:
            context_window: The complete list of messages/turns.

        Returns:
            The captured ContextSnapshot.
        """
        units = self.extract_semantic_units(context_window, self.session_id)
        content_blob = json.dumps(
            [u.to_dict() for u in units], sort_keys=True, ensure_ascii=False
        )
        self.pre_compaction_snapshot = ContextSnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            token_count=_estimate_tokens(context_window),
            turn_count=len(context_window),
            content_hash=hashlib.sha256(content_blob.encode("utf-8")).hexdigest(),
            items=[u.to_dict() for u in units],
        )
        return self.pre_compaction_snapshot

    def capture_post_state(
        self, compacted_context: List[Dict[str, Any]]
    ) -> ContextSnapshot:
        """
        Capture compressed state after compaction completes.

        Args:
            compacted_context: The post-compaction message list.

        Returns:
            The captured ContextSnapshot.
        """
        units = self.extract_semantic_units(compacted_context, self.session_id)
        content_blob = json.dumps(
            [u.to_dict() for u in units], sort_keys=True, ensure_ascii=False
        )

        pre_tokens = (
            self.pre_compaction_snapshot.token_count
            if self.pre_compaction_snapshot
            else 1
        )
        post_tokens = _estimate_tokens(compacted_context)

        self.post_compaction_snapshot = ContextSnapshot(
            timestamp=datetime.utcnow().isoformat() + "Z",
            token_count=post_tokens,
            turn_count=len(compacted_context),
            content_hash=hashlib.sha256(content_blob.encode("utf-8")).hexdigest(),
            items=[u.to_dict() for u in units],
        )
        return self.post_compaction_snapshot

    # ------------------------------------------------------------------
    # Diff / death log generation
    # ------------------------------------------------------------------

    def generate_death_log(self) -> List[DroppedItem]:
        """
        Diff pre and post states to identify dropped context.

        Returns:
            List of DroppedItem instances representing dead context.

        Raises:
            ValueError: If pre- or post-compaction snapshots are missing.
        """
        if not self.pre_compaction_snapshot or not self.post_compaction_snapshot:
            raise ValueError(
                "Both pre- and post-compaction snapshots must be captured "
                "before generating the death log."
            )

        pre_hashes: Dict[str, Dict[str, Any]] = {
            item["content_hash"]: item
            for item in self.pre_compaction_snapshot.items
        }
        post_hashes: Set[str] = {
            item["content_hash"]
            for item in self.post_compaction_snapshot.items
        }

        dropped_hashes = set(pre_hashes.keys()) - post_hashes
        retained_hashes = set(pre_hashes.keys()) & post_hashes

        self.dropped_items = []
        for h in dropped_hashes:
            item = pre_hashes[h]
            self.dropped_items.append(
                DroppedItem(
                    id=str(uuid.uuid4()),
                    content=item["content"],
                    source_turn=item["turn_index"],
                    source_timestamp=item["timestamp"],
                    session_id=self.session_id,
                    category=self.classifier.classify(item["content"]),
                    recovery_path=f"transcript://{self.session_id}/turn/{item['turn_index']}",
                    appeal_status="pending",
                    content_hash=h,
                )
            )

        self.retained_items = [
            SemanticUnit.from_dict(pre_hashes[h]) for h in retained_hashes
        ]

        return self.dropped_items

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def build_cda_log(self) -> CDALog:
        """
        Assemble the full CDA log object from captured state.

        Returns:
            CDALog instance with all provenance metadata.
        """
        pre_tokens = (
            self.pre_compaction_snapshot.token_count
            if self.pre_compaction_snapshot
            else 0
        )
        post_tokens = (
            self.post_compaction_snapshot.token_count
            if self.post_compaction_snapshot
            else 0
        )
        compression_ratio = (pre_tokens / post_tokens) if post_tokens > 0 else 0.0

        return CDALog(
            session_id=self.session_id,
            user_id=self.user_id,
            pre_snapshot=(
                self.pre_compaction_snapshot.to_dict()
                if self.pre_compaction_snapshot
                else {}
            ),
            post_snapshot=(
                self.post_compaction_snapshot.to_dict()
                if self.post_compaction_snapshot
                else {}
            ),
            dropped_items=[d.to_dict() for d in self.dropped_items],
            retained_items=[r.to_dict() for r in self.retained_items],
            compression_ratio=compression_ratio,
        )

    def persist_log(self, cda_log: Optional[CDALog] = None) -> Path:
        """
        Write the CDA log to a JSON file in the configured log directory.

        Args:
            cda_log: Optional pre-built CDALog.  If None, builds one
                     from current state.

        Returns:
            Path to the written log file.
        """
        if cda_log is None:
            cda_log = self.build_cda_log()

        filename = f"cda_{self.session_id}_{cda_log.log_id}.json"
        filepath = self.log_dir / filename

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(cda_log.to_dict(), f, indent=2, ensure_ascii=False)

        return filepath

    # ------------------------------------------------------------------
    # Query / loading
    # ------------------------------------------------------------------

    def load_log(self, filepath: str) -> CDALog:
        """Load a CDA log from a JSON file."""
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
        return CDALog.from_dict(data)

    def list_logs(self) -> List[Path]:
        """List all CDA log files in the log directory."""
        return sorted(self.log_dir.glob("cda_*.json"))

    def get_graveyard(self) -> List[DroppedItem]:
        """
        Aggregate all dropped items across every CDA log in the log dir.

        Returns:
            Combined list of all DroppedItem instances from all logs.
        """
        graveyard: List[DroppedItem] = []
        for log_path in self.list_logs():
            cda_log = self.load_log(str(log_path))
            graveyard.extend(
                DroppedItem.from_dict(item) for item in cda_log.dropped_items
            )
        return graveyard

    def get_stats(self) -> Dict[str, Any]:
        """Return summary statistics about the CDA store."""
        logs = self.list_logs()
        total_dropped = 0
        total_retained = 0
        for log_path in logs:
            cda_log = self.load_log(str(log_path))
            total_dropped += len(cda_log.dropped_items)
            total_retained += len(cda_log.retained_items)

        return {
            "log_count": len(logs),
            "total_dropped": total_dropped,
            "total_retained": total_retained,
            "log_directory": str(self.log_dir),
            "session_id": self.session_id,
        }


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def _estimate_tokens(messages: List[Dict[str, Any]]) -> int:
    """
    Rough token estimate: ~4 characters per token (GPT/Claude heuristic).
    This is intentionally approximate — real token counts require the
    model's tokenizer, which is not available in this closed-box context.
    """
    total_chars = 0
    for msg in messages:
        content = msg.get("content", "")
        if isinstance(content, list):
            for block in content:
                if isinstance(block, dict):
                    total_chars += len(block.get("text", ""))
        else:
            total_chars += len(str(content))
    return max(total_chars // 4, 1)
