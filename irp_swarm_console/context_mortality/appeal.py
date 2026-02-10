"""
Appeal Mechanism — Phase 4
==========================
Allows users to review CDA logs and reinstate dropped context into
the active memory system.

Workflow (from spec Section 3.2):
  1. User reviews CDA log
  2. For each dropped item, user chooses:
     - ACCEPT DROP  → marked "reviewed-accepted"
     - APPEAL       → flagged for reinstatement
     - ESCALATE     → generates Context Mortality Report

Reinstatement targets:
  - memory_user_edits  (persistent across sessions, 200-char limit)
  - session_injection  (injected at next session start)
  - claude_md          (for Claude Code users, via CLAUDE.md)
"""

import json
import uuid
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

from .models import (
    AppealCategory,
    AppealStatus,
    CDALog,
    DroppedItem,
    ReinstatementTarget,
    SovereigntyClass,
)
from .sovereignty import SovereigntyClassifier


# ---------------------------------------------------------------------------
# Reinstatement target routing rules (per spec Section 3.2 table)
# ---------------------------------------------------------------------------

_CATEGORY_ROUTING: Dict[str, Dict[str, str]] = {
    AppealCategory.FACTUAL.value: {
        "primary_target": ReinstatementTarget.MEMORY_EDIT.value,
        "scope": "persistent",
        "description": "Technical decisions — persistent across sessions",
    },
    AppealCategory.PROCEDURAL.value: {
        "primary_target": ReinstatementTarget.MEMORY_EDIT.value,
        "fallback_target": ReinstatementTarget.CLAUDE_MD.value,
        "scope": "persistent",
        "description": "Workflow preferences — persistent via memory or CLAUDE.md",
    },
    AppealCategory.CREATIVE.value: {
        "primary_target": ReinstatementTarget.SESSION_INJECTION.value,
        "scope": "session",
        "promotion_note": "Session-scoped unless user explicitly promotes",
        "description": "Artistic direction — session-scoped unless promoted",
    },
    AppealCategory.HEALTH.value: {
        "primary_target": None,  # NEVER auto-reinstated
        "scope": "user_explicit",
        "description": "SOVEREIGN — user decides scope explicitly",
    },
    AppealCategory.RELATIONAL.value: {
        "primary_target": ReinstatementTarget.MEMORY_EDIT.value,
        "scope": "persistent",
        "description": "Collaboration patterns — persistent, user-reviewed",
    },
}


class AppealDecision:
    """Represents a user's decision on a dropped item."""

    def __init__(
        self,
        dropped_item_id: str,
        action: str,
        category: str = AppealCategory.FACTUAL.value,
        reinstatement_target: Optional[str] = None,
        modified_content: Optional[str] = None,
        user_notes: Optional[str] = None,
    ):
        self.decision_id = str(uuid.uuid4())
        self.dropped_item_id = dropped_item_id
        self.action = action  # AppealStatus value
        self.category = category
        self.reinstatement_target = reinstatement_target
        self.modified_content = modified_content
        self.user_notes = user_notes
        self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "dropped_item_id": self.dropped_item_id,
            "action": self.action,
            "category": self.category,
            "reinstatement_target": self.reinstatement_target,
            "modified_content": self.modified_content,
            "user_notes": self.user_notes,
            "timestamp": self.timestamp,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "AppealDecision":
        decision = cls(
            dropped_item_id=data["dropped_item_id"],
            action=data["action"],
            category=data.get("category", AppealCategory.FACTUAL.value),
            reinstatement_target=data.get("reinstatement_target"),
            modified_content=data.get("modified_content"),
            user_notes=data.get("user_notes"),
        )
        decision.decision_id = data.get("decision_id", decision.decision_id)
        decision.timestamp = data.get("timestamp", decision.timestamp)
        return decision


class ReinstatementAction:
    """An action to reinstate dropped context to a specific target."""

    def __init__(
        self,
        target: str,
        content: str,
        source_item_id: str,
        category: str,
    ):
        self.action_id = str(uuid.uuid4())
        self.target = target
        self.content = content
        self.source_item_id = source_item_id
        self.category = category
        self.status = "pending"
        self.executed_at: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "action_id": self.action_id,
            "target": self.target,
            "content": self.content,
            "source_item_id": self.source_item_id,
            "category": self.category,
            "status": self.status,
            "executed_at": self.executed_at,
        }


class ContextMortalityReport:
    """
    Generated when a dropped item is escalated as critical loss.
    Provides a complete provenance record for the user's archives.
    """

    def __init__(
        self,
        dropped_item: DroppedItem,
        user_notes: Optional[str] = None,
    ):
        self.report_id = str(uuid.uuid4())
        self.timestamp = datetime.utcnow().isoformat() + "Z"
        self.dropped_item = dropped_item
        self.user_notes = user_notes
        self.severity = "CRITICAL"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "report_id": self.report_id,
            "timestamp": self.timestamp,
            "severity": self.severity,
            "dropped_item": self.dropped_item.to_dict(),
            "user_notes": self.user_notes,
            "recommendation": (
                "This item was flagged as a critical context loss. "
                "Consider architectural review of the compression "
                "parameters for this content category."
            ),
        }


class AppealManager:
    """
    Manages the appeal workflow for dropped context items.

    Responsibilities:
      - Present dropped items for user review
      - Record user decisions
      - Route reinstatement actions to appropriate targets
      - Generate context mortality reports for escalations
      - Persist appeal history
    """

    def __init__(
        self,
        appeal_dir: Optional[str] = None,
        claude_md_path: Optional[str] = None,
    ):
        if appeal_dir is None:
            appeal_dir = str(Path(__file__).parent / "appeal_logs")
        self.appeal_dir = Path(appeal_dir)
        self.appeal_dir.mkdir(parents=True, exist_ok=True)

        self.claude_md_path = claude_md_path
        self.classifier = SovereigntyClassifier()
        self.decisions: List[AppealDecision] = []
        self.reinstatement_queue: List[ReinstatementAction] = []
        self.mortality_reports: List[ContextMortalityReport] = []

        self._load_decisions()

    # ------------------------------------------------------------------
    # Decision management
    # ------------------------------------------------------------------

    def review_item(
        self,
        dropped_item: DroppedItem,
        action: str,
        category: str = AppealCategory.FACTUAL.value,
        reinstatement_target: Optional[str] = None,
        modified_content: Optional[str] = None,
        user_notes: Optional[str] = None,
    ) -> AppealDecision:
        """
        Record a user's decision on a dropped item.

        Args:
            dropped_item: The DroppedItem being reviewed.
            action: One of AppealStatus values:
                    "reviewed-accepted", "appealed", "escalated"
            category: AppealCategory for routing reinstatement.
            reinstatement_target: Override the default target routing.
            modified_content: User-modified version of the content.
            user_notes: Optional notes from the user.

        Returns:
            The recorded AppealDecision.
        """
        # Health sovereignty check
        if self.classifier.requires_explicit_consent(dropped_item.category):
            if action == AppealStatus.APPEALED.value:
                if not user_notes or "HEALTH_OPT_IN" not in user_notes:
                    raise ValueError(
                        "Health-classified items require explicit opt-in. "
                        "Include 'HEALTH_OPT_IN' in user_notes to confirm."
                    )

        # Determine reinstatement target from category routing
        if reinstatement_target is None and action == AppealStatus.APPEALED.value:
            routing = _CATEGORY_ROUTING.get(category, {})
            reinstatement_target = routing.get("primary_target")

        decision = AppealDecision(
            dropped_item_id=dropped_item.id,
            action=action,
            category=category,
            reinstatement_target=reinstatement_target,
            modified_content=modified_content,
            user_notes=user_notes,
        )
        self.decisions.append(decision)
        self._persist_decision(decision)

        # Route based on action
        if action == AppealStatus.APPEALED.value:
            self._queue_reinstatement(dropped_item, decision)
        elif action == AppealStatus.ESCALATED.value:
            self._generate_mortality_report(dropped_item, user_notes)

        return decision

    def accept_drop(self, dropped_item: DroppedItem) -> AppealDecision:
        """Convenience: accept a drop (item stays in graveyard)."""
        return self.review_item(
            dropped_item=dropped_item,
            action=AppealStatus.ACCEPTED_DROP.value,
        )

    def appeal_item(
        self,
        dropped_item: DroppedItem,
        category: str = AppealCategory.FACTUAL.value,
        target: Optional[str] = None,
        modified_content: Optional[str] = None,
    ) -> AppealDecision:
        """Convenience: appeal a dropped item for reinstatement."""
        return self.review_item(
            dropped_item=dropped_item,
            action=AppealStatus.APPEALED.value,
            category=category,
            reinstatement_target=target,
            modified_content=modified_content,
        )

    def escalate_item(
        self,
        dropped_item: DroppedItem,
        user_notes: Optional[str] = None,
    ) -> AppealDecision:
        """Convenience: escalate a dropped item as critical loss."""
        return self.review_item(
            dropped_item=dropped_item,
            action=AppealStatus.ESCALATED.value,
            user_notes=user_notes,
        )

    # ------------------------------------------------------------------
    # Reinstatement
    # ------------------------------------------------------------------

    def _queue_reinstatement(
        self, dropped_item: DroppedItem, decision: AppealDecision
    ) -> None:
        """Queue a reinstatement action based on the appeal decision."""
        content = decision.modified_content or dropped_item.content
        target = decision.reinstatement_target

        if target is None:
            # Health items with no target — skip auto-reinstatement
            return

        # Enforce 200-char limit for memory_user_edits
        if target == ReinstatementTarget.MEMORY_EDIT.value:
            if len(content) > 200:
                content = content[:197] + "..."

        action = ReinstatementAction(
            target=target,
            content=content,
            source_item_id=dropped_item.id,
            category=decision.category,
        )
        self.reinstatement_queue.append(action)

    def execute_reinstatements(self) -> List[Dict[str, Any]]:
        """
        Execute all queued reinstatement actions.

        Returns a list of execution results.  Actual API calls to
        memory_user_edits or session injection are not performed here
        (that requires Anthropic API access); instead, this produces
        the structured payloads that would be sent.
        """
        results = []
        for action in self.reinstatement_queue:
            if action.status != "pending":
                continue

            result = self._execute_single(action)
            results.append(result)

        return results

    def _execute_single(self, action: ReinstatementAction) -> Dict[str, Any]:
        """Execute a single reinstatement action."""
        action.executed_at = datetime.utcnow().isoformat() + "Z"

        if action.target == ReinstatementTarget.CLAUDE_MD.value:
            success = self._reinstate_to_claude_md(action.content)
            action.status = "executed" if success else "failed"
        elif action.target == ReinstatementTarget.SESSION_INJECTION.value:
            # Session injection produces a payload for the next session
            action.status = "staged"
        elif action.target == ReinstatementTarget.MEMORY_EDIT.value:
            # Memory edit produces a payload for the API
            action.status = "staged"
        else:
            action.status = "unknown_target"

        return action.to_dict()

    def _reinstate_to_claude_md(self, content: str) -> bool:
        """Append recovered context to CLAUDE.md file."""
        if self.claude_md_path is None:
            return False

        md_path = Path(self.claude_md_path)
        try:
            existing = ""
            if md_path.exists():
                existing = md_path.read_text(encoding="utf-8")

            timestamp = datetime.utcnow().isoformat() + "Z"
            entry = (
                f"\n\n## Recovered Context [{timestamp}]\n\n"
                f"{content}\n"
            )
            md_path.write_text(existing + entry, encoding="utf-8")
            return True
        except OSError:
            return False

    # ------------------------------------------------------------------
    # Mortality reports
    # ------------------------------------------------------------------

    def _generate_mortality_report(
        self, dropped_item: DroppedItem, user_notes: Optional[str]
    ) -> ContextMortalityReport:
        """Generate a Context Mortality Report for an escalated item."""
        report = ContextMortalityReport(
            dropped_item=dropped_item,
            user_notes=user_notes,
        )
        self.mortality_reports.append(report)

        # Persist report
        filepath = self.appeal_dir / f"mortality_report_{report.report_id}.json"
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(report.to_dict(), f, indent=2, ensure_ascii=False)

        return report

    # ------------------------------------------------------------------
    # Query
    # ------------------------------------------------------------------

    def get_pending_appeals(self) -> List[Dict[str, Any]]:
        """Get all decisions with 'appealed' status awaiting execution."""
        return [
            d.to_dict()
            for d in self.decisions
            if d.action == AppealStatus.APPEALED.value
        ]

    def get_reinstatement_queue(self) -> List[Dict[str, Any]]:
        """Get the current reinstatement queue."""
        return [a.to_dict() for a in self.reinstatement_queue]

    def get_mortality_reports(self) -> List[Dict[str, Any]]:
        """Get all context mortality reports."""
        return [r.to_dict() for r in self.mortality_reports]

    def get_decision_history(self) -> List[Dict[str, Any]]:
        """Get full appeal decision history."""
        return [d.to_dict() for d in self.decisions]

    def get_stats(self) -> Dict[str, Any]:
        """Return summary statistics."""
        from collections import Counter

        action_counts = Counter(d.action for d in self.decisions)
        return {
            "total_decisions": len(self.decisions),
            "action_counts": dict(action_counts),
            "pending_reinstatements": len(
                [a for a in self.reinstatement_queue if a.status == "pending"]
            ),
            "mortality_reports": len(self.mortality_reports),
            "appeal_dir": str(self.appeal_dir),
        }

    # ------------------------------------------------------------------
    # Persistence
    # ------------------------------------------------------------------

    def _persist_decision(self, decision: AppealDecision) -> None:
        """Append a decision to the decisions JSONL file."""
        filepath = self.appeal_dir / "decisions.jsonl"
        with open(filepath, "a", encoding="utf-8") as f:
            f.write(json.dumps(decision.to_dict(), ensure_ascii=False) + "\n")

    def _load_decisions(self) -> None:
        """Load existing decisions from JSONL."""
        filepath = self.appeal_dir / "decisions.jsonl"
        if not filepath.exists():
            return
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    data = json.loads(line)
                    self.decisions.append(AppealDecision.from_dict(data))
                except (json.JSONDecodeError, KeyError):
                    continue
