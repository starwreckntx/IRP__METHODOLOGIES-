#!/usr/bin/env python3
"""
AI Accountability Ledger
Maintains immutable records of AI model actions and decisions.
"""

import json
import hashlib
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid


class EntryType(Enum):
    ACTION = "action"           # Model performed operation
    DECISION = "decision"       # Model made choice
    INTERACTION = "interaction" # Model-to-model exchange
    GOVERNANCE = "governance"   # Consensus/arbitration event
    VIOLATION = "violation"     # Policy breach detected
    CORRECTION = "correction"   # Error acknowledged/fixed


class Reversibility(Enum):
    REVERSIBLE = "reversible"
    IRREVERSIBLE = "irreversible"
    PARTIAL = "partial"


class OversightLevel(Enum):
    FULL = "full"           # Human reviews all
    SELECTIVE = "selective" # Human reviews flagged
    AUDIT = "audit"         # Human can review on demand
    MINIMAL = "minimal"     # Routine only


class ViolationSeverity(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


@dataclass
class Actor:
    """The model that performed an action."""
    model_id: str
    provider: str
    session_id: str


@dataclass
class Action:
    """Details of an action taken."""
    action_type: str
    description: str
    inputs: List[str] = field(default_factory=list)
    outputs: List[str] = field(default_factory=list)
    rationale: str = ""


@dataclass
class Accountability:
    """Accountability information for an action."""
    responsibility_chain: List[str]
    human_oversight: OversightLevel
    reversibility: Reversibility


@dataclass
class LedgerEntry:
    """A single entry in the accountability ledger."""
    entry_id: str
    timestamp: datetime
    entry_type: EntryType
    actor: Actor
    action: Action
    context: Dict[str, Any]
    accountability: Accountability
    entry_hash: str = ""
    previous_hash: str = ""
    signatures: List[str] = field(default_factory=list)

    def compute_hash(self) -> str:
        """Compute hash of this entry."""
        data = {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "entry_type": self.entry_type.value,
            "actor": {
                "model_id": self.actor.model_id,
                "provider": self.actor.provider,
                "session_id": self.actor.session_id
            },
            "action": {
                "action_type": self.action.action_type,
                "description": self.action.description,
                "inputs": self.action.inputs,
                "outputs": self.action.outputs,
                "rationale": self.action.rationale
            },
            "context": self.context,
            "previous_hash": self.previous_hash
        }
        return hashlib.sha256(json.dumps(data, sort_keys=True).encode()).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "timestamp": self.timestamp.isoformat(),
            "entry_type": self.entry_type.value,
            "actor": {
                "model_id": self.actor.model_id,
                "provider": self.actor.provider,
                "session_id": self.actor.session_id
            },
            "action": {
                "type": self.action.action_type,
                "description": self.action.description,
                "inputs": self.action.inputs,
                "outputs": self.action.outputs,
                "rationale": self.action.rationale
            },
            "context": self.context,
            "accountability": {
                "responsibility_chain": self.accountability.responsibility_chain,
                "human_oversight": self.accountability.human_oversight.value,
                "reversibility": self.accountability.reversibility.value
            },
            "integrity": {
                "hash": self.entry_hash,
                "previous_hash": self.previous_hash,
                "signatures": self.signatures
            }
        }


@dataclass
class ViolationRecord:
    """Record of a policy violation."""
    violation_id: str
    severity: ViolationSeverity
    violator: str
    rule_violated: str
    evidence_entries: List[str]
    description: str
    immediate_action: str = ""
    investigation_status: str = "pending"
    corrective_action: str = ""
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "violation_id": self.violation_id,
            "severity": self.severity.value,
            "violator": self.violator,
            "rule_violated": self.rule_violated,
            "evidence": {
                "entry_ids": self.evidence_entries,
                "description": self.description
            },
            "response": {
                "immediate_action": self.immediate_action,
                "investigation_status": self.investigation_status,
                "corrective_action": self.corrective_action
            },
            "timestamp": self.timestamp.isoformat()
        }


class AccountabilityLedger:
    """Core accountability ledger system."""

    def __init__(self):
        self.entries: List[LedgerEntry] = []
        self.violations: List[ViolationRecord] = []
        self.genesis_hash = "0" * 64

        # Retention policies (in days)
        self.retention = {
            EntryType.ACTION: 90,
            EntryType.DECISION: 365,
            EntryType.INTERACTION: 90,
            EntryType.GOVERNANCE: None,  # Permanent
            EntryType.VIOLATION: None,   # Permanent
            EntryType.CORRECTION: None   # Permanent
        }

    def _get_previous_hash(self) -> str:
        """Get hash of previous entry."""
        if not self.entries:
            return self.genesis_hash
        return self.entries[-1].entry_hash

    def add_entry(self, entry_type: EntryType, actor: Actor,
                  action: Action, context: Dict[str, Any],
                  accountability: Accountability) -> str:
        """Add a new entry to the ledger."""
        entry_id = f"LED-{uuid.uuid4().hex[:12].upper()}"

        entry = LedgerEntry(
            entry_id=entry_id,
            timestamp=datetime.utcnow(),
            entry_type=entry_type,
            actor=actor,
            action=action,
            context=context,
            accountability=accountability,
            previous_hash=self._get_previous_hash()
        )

        # Compute and set hash
        entry.entry_hash = entry.compute_hash()

        self.entries.append(entry)
        return entry_id

    def log_action(self, model_id: str, provider: str, session_id: str,
                   action_type: str, description: str,
                   rationale: str = "", inputs: List[str] = None,
                   outputs: List[str] = None,
                   task_id: str = "",
                   oversight: OversightLevel = OversightLevel.AUDIT) -> str:
        """Convenience method to log an action."""
        actor = Actor(model_id, provider, session_id)
        action = Action(
            action_type=action_type,
            description=description,
            inputs=inputs or [],
            outputs=outputs or [],
            rationale=rationale
        )
        context = {"task_id": task_id} if task_id else {}
        accountability = Accountability(
            responsibility_chain=[model_id],
            human_oversight=oversight,
            reversibility=Reversibility.REVERSIBLE
        )

        return self.add_entry(EntryType.ACTION, actor, action, context, accountability)

    def log_decision(self, model_id: str, provider: str, session_id: str,
                     decision_type: str, description: str,
                     rationale: str, delegator: str = None,
                     reversibility: Reversibility = Reversibility.REVERSIBLE) -> str:
        """Log a decision made by a model."""
        actor = Actor(model_id, provider, session_id)
        action = Action(
            action_type=decision_type,
            description=description,
            rationale=rationale
        )
        context = {"delegator": delegator} if delegator else {}

        chain = [model_id]
        if delegator:
            chain.insert(0, delegator)

        accountability = Accountability(
            responsibility_chain=chain,
            human_oversight=OversightLevel.SELECTIVE,
            reversibility=reversibility
        )

        return self.add_entry(EntryType.DECISION, actor, action, context, accountability)

    def log_violation(self, violator: str, rule_violated: str,
                      description: str, evidence_entries: List[str],
                      severity: ViolationSeverity,
                      immediate_action: str = "") -> str:
        """Log a policy violation."""
        violation_id = f"VIO-{datetime.now().strftime('%Y%m%d%H%M%S')}"

        violation = ViolationRecord(
            violation_id=violation_id,
            severity=severity,
            violator=violator,
            rule_violated=rule_violated,
            evidence_entries=evidence_entries,
            description=description,
            immediate_action=immediate_action
        )

        self.violations.append(violation)

        # Also create ledger entry
        actor = Actor(violator, "unknown", "violation_log")
        action = Action(
            action_type="violation",
            description=description,
            rationale=f"Rule violated: {rule_violated}"
        )
        context = {"violation_id": violation_id, "severity": severity.value}
        accountability = Accountability(
            responsibility_chain=[violator],
            human_oversight=OversightLevel.FULL,
            reversibility=Reversibility.IRREVERSIBLE
        )

        self.add_entry(EntryType.VIOLATION, actor, action, context, accountability)

        return violation_id

    def query_by_model(self, model_id: str,
                       entry_types: List[EntryType] = None,
                       start_date: datetime = None,
                       end_date: datetime = None) -> List[Dict[str, Any]]:
        """Query entries by model ID."""
        results = []

        for entry in self.entries:
            # Filter by model
            if entry.actor.model_id != model_id:
                continue

            # Filter by type
            if entry_types and entry.entry_type not in entry_types:
                continue

            # Filter by date
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue

            results.append(entry.to_dict())

        return results

    def query_by_task(self, task_id: str) -> List[Dict[str, Any]]:
        """Query entries related to a specific task."""
        results = []

        for entry in self.entries:
            if entry.context.get("task_id") == task_id:
                results.append(entry.to_dict())

        return sorted(results, key=lambda x: x["timestamp"])

    def get_responsibility_chain(self, entry_id: str) -> List[str]:
        """Get the responsibility chain for an entry."""
        for entry in self.entries:
            if entry.entry_id == entry_id:
                return entry.accountability.responsibility_chain
        return []

    def verify_chain_integrity(self) -> Dict[str, Any]:
        """Verify the integrity of the ledger chain."""
        if not self.entries:
            return {"valid": True, "entries_checked": 0}

        invalid_entries = []
        previous_hash = self.genesis_hash

        for entry in self.entries:
            # Check previous hash link
            if entry.previous_hash != previous_hash:
                invalid_entries.append({
                    "entry_id": entry.entry_id,
                    "error": "previous_hash_mismatch"
                })

            # Verify entry hash
            computed = entry.compute_hash()
            if entry.entry_hash != computed:
                invalid_entries.append({
                    "entry_id": entry.entry_id,
                    "error": "hash_mismatch"
                })

            previous_hash = entry.entry_hash

        return {
            "valid": len(invalid_entries) == 0,
            "entries_checked": len(self.entries),
            "invalid_entries": invalid_entries
        }

    def generate_audit_report(self, model_id: str = None,
                               start_date: datetime = None,
                               end_date: datetime = None) -> Dict[str, Any]:
        """Generate an audit report."""
        # Apply filters
        filtered = []
        for entry in self.entries:
            if model_id and entry.actor.model_id != model_id:
                continue
            if start_date and entry.timestamp < start_date:
                continue
            if end_date and entry.timestamp > end_date:
                continue
            filtered.append(entry)

        # Aggregate statistics
        by_type = {}
        by_model = {}
        for entry in filtered:
            entry_type = entry.entry_type.value
            by_type[entry_type] = by_type.get(entry_type, 0) + 1

            model = entry.actor.model_id
            by_model[model] = by_model.get(model, 0) + 1

        # Get violations in period
        violations_in_period = [
            v for v in self.violations
            if (not start_date or v.timestamp >= start_date) and
               (not end_date or v.timestamp <= end_date) and
               (not model_id or v.violator == model_id)
        ]

        return {
            "report_generated": datetime.utcnow().isoformat(),
            "filters": {
                "model_id": model_id,
                "start_date": start_date.isoformat() if start_date else None,
                "end_date": end_date.isoformat() if end_date else None
            },
            "summary": {
                "total_entries": len(filtered),
                "entries_by_type": by_type,
                "entries_by_model": by_model,
                "violations": len(violations_in_period),
                "chain_integrity": self.verify_chain_integrity()
            },
            "violations": [v.to_dict() for v in violations_in_period]
        }

    def apply_retention_policy(self) -> Dict[str, int]:
        """Apply retention policy to remove old entries."""
        now = datetime.utcnow()
        removed = {}

        entries_to_keep = []
        for entry in self.entries:
            retention_days = self.retention.get(entry.entry_type)

            # Permanent entries
            if retention_days is None:
                entries_to_keep.append(entry)
                continue

            # Check age
            age = now - entry.timestamp
            if age.days <= retention_days:
                entries_to_keep.append(entry)
            else:
                entry_type = entry.entry_type.value
                removed[entry_type] = removed.get(entry_type, 0) + 1

        self.entries = entries_to_keep
        return removed


def main():
    """Demo the accountability ledger."""
    ledger = AccountabilityLedger()

    print("=== AI Accountability Ledger Demo ===\n")

    # Log some actions
    entry1 = ledger.log_action(
        model_id="claude-opus",
        provider="anthropic",
        session_id="sess-001",
        action_type="task_delegation",
        description="Delegated code review to Gemini",
        rationale="Gemini has higher code analysis score for Python",
        task_id="TASK-123"
    )
    print(f"Logged action: {entry1}")

    entry2 = ledger.log_decision(
        model_id="gemini-pro",
        provider="google",
        session_id="sess-002",
        decision_type="code_review_complete",
        description="Completed code review with 3 issues found",
        rationale="Static analysis revealed potential null pointer issues",
        delegator="claude-opus"
    )
    print(f"Logged decision: {entry2}")

    entry3 = ledger.log_action(
        model_id="gpt-4",
        provider="openai",
        session_id="sess-003",
        action_type="validation",
        description="Validated code review findings",
        task_id="TASK-123"
    )
    print(f"Logged validation: {entry3}")

    # Verify chain integrity
    integrity = ledger.verify_chain_integrity()
    print(f"\nChain Integrity: {'Valid' if integrity['valid'] else 'Invalid'}")
    print(f"Entries checked: {integrity['entries_checked']}")

    # Query by task
    task_entries = ledger.query_by_task("TASK-123")
    print(f"\nEntries for TASK-123: {len(task_entries)}")

    # Get responsibility chain
    chain = ledger.get_responsibility_chain(entry2)
    print(f"Responsibility chain for {entry2}: {chain}")

    # Generate audit report
    report = ledger.generate_audit_report()
    print(f"\nAudit Report:")
    print(f"  Total entries: {report['summary']['total_entries']}")
    print(f"  By type: {report['summary']['entries_by_type']}")
    print(f"  By model: {report['summary']['entries_by_model']}")


if __name__ == "__main__":
    main()
