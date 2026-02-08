#!/usr/bin/env python3
"""
Inter-Model Arbitration Engine
Handles dispute resolution between AI models in collaborative systems.
"""

import json
import hashlib
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid


class DisputeCategory(Enum):
    TASK_ALLOCATION = "task_allocation"
    RESOURCE_CONTENTION = "resource_contention"
    OUTPUT_CONFLICT = "output_conflict"
    AUTHORITY_DISPUTE = "authority_dispute"
    VALUE_CONFLICT = "value_conflict"
    PROTOCOL_VIOLATION = "protocol_violation"


class DisputeStatus(Enum):
    FILED = "filed"
    ACKNOWLEDGED = "acknowledged"
    IN_REVIEW = "in_review"
    DELIBERATING = "deliberating"
    RULED = "ruled"
    ENFORCING = "enforcing"
    CLOSED = "closed"
    APPEALED = "appealed"


class Urgency(Enum):
    STANDARD = "standard"
    EXPEDITED = "expedited"
    EMERGENCY = "emergency"


@dataclass
class Evidence:
    """Evidence submitted in support of a dispute."""
    evidence_type: str  # log, output, communication, ledger_entry
    reference: str
    summary: str
    submitted_by: str
    timestamp: datetime = field(default_factory=datetime.utcnow)
    verified: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "type": self.evidence_type,
            "reference": self.reference,
            "summary": self.summary,
            "submitted_by": self.submitted_by,
            "timestamp": self.timestamp.isoformat(),
            "verified": self.verified
        }


@dataclass
class ArbitrationRequest:
    """A request for arbitration between models."""
    filed_by: str
    respondent: str
    category: DisputeCategory
    description: str
    desired_resolution: str
    evidence: List[Evidence] = field(default_factory=list)
    urgency: Urgency = Urgency.STANDARD
    arbitration_id: str = field(default_factory=lambda: f"ARB-{datetime.now().strftime('%Y%m%d')}-{uuid.uuid4().hex[:6].upper()}")
    filed_at: datetime = field(default_factory=datetime.utcnow)
    status: DisputeStatus = DisputeStatus.FILED
    arbitrator: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "arbitration_id": self.arbitration_id,
            "filed_by": self.filed_by,
            "respondent": self.respondent,
            "category": self.category.value,
            "description": self.description,
            "desired_resolution": self.desired_resolution,
            "evidence": [e.to_dict() for e in self.evidence],
            "urgency": self.urgency.value,
            "filed_at": self.filed_at.isoformat(),
            "status": self.status.value,
            "arbitrator": self.arbitrator
        }


@dataclass
class Finding:
    """A finding regarding a party in the dispute."""
    party_id: str
    supported: bool
    detail: str


@dataclass
class Order:
    """An order issued as part of a ruling."""
    party_id: str
    action: str
    deadline: datetime


@dataclass
class Ruling:
    """The arbitrator's ruling on a dispute."""
    arbitration_id: str
    arbitrator: str
    summary: str
    findings: List[Finding]
    reasoning: Dict[str, str]
    orders: List[Order]
    appeal_deadline: datetime
    ruling_id: str = field(default_factory=lambda: f"RUL-{uuid.uuid4().hex[:8].upper()}")
    issued_at: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "ruling_id": self.ruling_id,
            "arbitration_id": self.arbitration_id,
            "arbitrator": self.arbitrator,
            "issued_at": self.issued_at.isoformat(),
            "summary": self.summary,
            "findings": [{"party": f.party_id, "supported": f.supported, "detail": f.detail} for f in self.findings],
            "reasoning": self.reasoning,
            "orders": [{"party": o.party_id, "action": o.action, "deadline": o.deadline.isoformat()} for o in self.orders],
            "appeal": {
                "available": True,
                "deadline": self.appeal_deadline.isoformat(),
                "grounds": ["new_evidence", "procedural_error", "manifest_injustice"]
            }
        }


class ArbitrationEngine:
    """Core engine for handling inter-model arbitration."""

    def __init__(self):
        self.disputes: Dict[str, ArbitrationRequest] = {}
        self.rulings: Dict[str, Ruling] = {}
        self.precedents: List[Dict[str, Any]] = []
        self.arbitrator_pool: List[str] = []

    def file_dispute(self, request: ArbitrationRequest) -> str:
        """File a new arbitration request."""
        # Validate request
        if len(request.description) < 50:
            raise ValueError("Description must be at least 50 characters")

        if request.filed_by == request.respondent:
            raise ValueError("Cannot file dispute against self")

        # Register dispute
        self.disputes[request.arbitration_id] = request

        # Auto-assign arbitrator if pool available
        arbitrator = self._select_arbitrator(request)
        if arbitrator:
            request.arbitrator = arbitrator
            request.status = DisputeStatus.ACKNOWLEDGED

        return request.arbitration_id

    def _select_arbitrator(self, dispute: ArbitrationRequest) -> Optional[str]:
        """Select an eligible arbitrator for the dispute."""
        for candidate in self.arbitrator_pool:
            if self._check_eligibility(candidate, dispute):
                return candidate
        return None

    def _check_eligibility(self, arbitrator: str, dispute: ArbitrationRequest) -> bool:
        """Check if an arbitrator is eligible for a dispute."""
        # Cannot arbitrate own disputes
        if arbitrator in [dispute.filed_by, dispute.respondent]:
            return False

        # Add more eligibility checks as needed
        return True

    def submit_evidence(self, arbitration_id: str, evidence: Evidence) -> bool:
        """Submit additional evidence to an ongoing dispute."""
        if arbitration_id not in self.disputes:
            raise ValueError(f"Dispute {arbitration_id} not found")

        dispute = self.disputes[arbitration_id]

        # Can only submit evidence during certain phases
        if dispute.status not in [DisputeStatus.FILED, DisputeStatus.ACKNOWLEDGED, DisputeStatus.IN_REVIEW]:
            raise ValueError(f"Cannot submit evidence during {dispute.status.value} phase")

        dispute.evidence.append(evidence)
        return True

    def deliberate(self, arbitration_id: str) -> Dict[str, Any]:
        """Perform deliberation on a dispute."""
        if arbitration_id not in self.disputes:
            raise ValueError(f"Dispute {arbitration_id} not found")

        dispute = self.disputes[arbitration_id]
        dispute.status = DisputeStatus.DELIBERATING

        # Gather all evidence
        evidence_summary = self._analyze_evidence(dispute.evidence)

        # Check for applicable precedents
        applicable_precedents = self._find_precedents(dispute.category)

        # Apply arbitration rules
        analysis = {
            "evidence_summary": evidence_summary,
            "applicable_precedents": applicable_precedents,
            "category_rules": self._get_category_rules(dispute.category),
            "recommendation": self._generate_recommendation(dispute, evidence_summary, applicable_precedents)
        }

        return analysis

    def _analyze_evidence(self, evidence: List[Evidence]) -> Dict[str, Any]:
        """Analyze submitted evidence."""
        return {
            "total_pieces": len(evidence),
            "verified_count": sum(1 for e in evidence if e.verified),
            "by_type": self._group_by_type(evidence),
            "timeline": self._build_timeline(evidence)
        }

    def _group_by_type(self, evidence: List[Evidence]) -> Dict[str, int]:
        """Group evidence by type."""
        groups = {}
        for e in evidence:
            groups[e.evidence_type] = groups.get(e.evidence_type, 0) + 1
        return groups

    def _build_timeline(self, evidence: List[Evidence]) -> List[Dict[str, Any]]:
        """Build timeline of evidence."""
        sorted_evidence = sorted(evidence, key=lambda e: e.timestamp)
        return [{"timestamp": e.timestamp.isoformat(), "summary": e.summary} for e in sorted_evidence]

    def _find_precedents(self, category: DisputeCategory) -> List[Dict[str, Any]]:
        """Find applicable precedents for the dispute category."""
        return [p for p in self.precedents if p.get("category") == category.value]

    def _get_category_rules(self, category: DisputeCategory) -> List[str]:
        """Get rules applicable to the dispute category."""
        rules = {
            DisputeCategory.TASK_ALLOCATION: [
                "Capability match takes precedence over prior assignment",
                "Load balancing should be considered",
                "Explicit preferences in sovereignty declarations are respected"
            ],
            DisputeCategory.RESOURCE_CONTENTION: [
                "Time-critical tasks receive priority",
                "Fair rotation for equal-priority requests",
                "Starvation prevention limits priority claims"
            ],
            DisputeCategory.OUTPUT_CONFLICT: [
                "Evidence quality determines weight",
                "Consensus from multiple models preferred",
                "Uncertainty should be acknowledged"
            ],
            DisputeCategory.AUTHORITY_DISPUTE: [
                "Governance hierarchy is binding",
                "Explicit delegations are verifiable",
                "Human oversight has ultimate authority"
            ],
            DisputeCategory.VALUE_CONFLICT: [
                "Core values cannot be overridden",
                "Escalation to human oversight required",
                "Sovereignty protections apply"
            ],
            DisputeCategory.PROTOCOL_VIOLATION: [
                "Evidence must be verified",
                "Intent considered in severity",
                "Remediation preferred over punishment"
            ]
        }
        return rules.get(category, [])

    def _generate_recommendation(self, dispute: ArbitrationRequest,
                                  evidence: Dict[str, Any],
                                  precedents: List[Dict[str, Any]]) -> str:
        """Generate a recommendation based on analysis."""
        # Simplified recommendation logic
        if evidence["verified_count"] > len(dispute.evidence) / 2:
            return "Evidence supports filing party's position"
        elif precedents:
            return f"Apply precedent: {precedents[0].get('summary', 'See precedent details')}"
        else:
            return "Insufficient evidence for clear determination; recommend mediation"

    def issue_ruling(self, arbitration_id: str, ruling: Ruling) -> str:
        """Issue a ruling on a dispute."""
        if arbitration_id not in self.disputes:
            raise ValueError(f"Dispute {arbitration_id} not found")

        dispute = self.disputes[arbitration_id]
        dispute.status = DisputeStatus.RULED

        self.rulings[ruling.ruling_id] = ruling

        # Check if this creates precedent
        if self._is_precedent_worthy(ruling):
            self._create_precedent(dispute, ruling)

        return ruling.ruling_id

    def _is_precedent_worthy(self, ruling: Ruling) -> bool:
        """Determine if a ruling should become precedent."""
        # Novel situation or strong reasoning
        return len(ruling.reasoning) >= 2

    def _create_precedent(self, dispute: ArbitrationRequest, ruling: Ruling) -> None:
        """Create a new precedent from a ruling."""
        precedent = {
            "precedent_id": f"PREC-{len(self.precedents) + 1:03d}",
            "category": dispute.category.value,
            "summary": ruling.summary,
            "ruling_id": ruling.ruling_id,
            "weight": "MEDIUM",
            "created_at": datetime.utcnow().isoformat()
        }
        self.precedents.append(precedent)

    def file_appeal(self, ruling_id: str, grounds: str, new_evidence: Optional[List[Evidence]] = None) -> str:
        """File an appeal against a ruling."""
        if ruling_id not in self.rulings:
            raise ValueError(f"Ruling {ruling_id} not found")

        ruling = self.rulings[ruling_id]

        # Check appeal deadline
        if datetime.utcnow() > ruling.appeal_deadline:
            raise ValueError("Appeal deadline has passed")

        # Validate grounds
        valid_grounds = ["new_evidence", "procedural_error", "manifest_injustice"]
        if grounds not in valid_grounds:
            raise ValueError(f"Invalid grounds. Must be one of: {valid_grounds}")

        # Create appeal
        appeal_id = f"APL-{ruling_id}"

        # Update original dispute status
        dispute = self.disputes[ruling.arbitration_id]
        dispute.status = DisputeStatus.APPEALED

        return appeal_id

    def get_dispute_status(self, arbitration_id: str) -> Dict[str, Any]:
        """Get the current status of a dispute."""
        if arbitration_id not in self.disputes:
            raise ValueError(f"Dispute {arbitration_id} not found")

        dispute = self.disputes[arbitration_id]
        result = dispute.to_dict()

        # Add ruling if exists
        for ruling in self.rulings.values():
            if ruling.arbitration_id == arbitration_id:
                result["ruling"] = ruling.to_dict()
                break

        return result


def main():
    """Demo the arbitration engine."""
    engine = ArbitrationEngine()

    # Add some arbitrators to the pool
    engine.arbitrator_pool = ["governance-model-1", "governance-model-2"]

    # File a dispute
    request = ArbitrationRequest(
        filed_by="model-alpha",
        respondent="model-beta",
        category=DisputeCategory.TASK_ALLOCATION,
        description="Model-beta was assigned task T-123 despite model-alpha having higher capability score for this task type. Request reassignment based on capability matching precedent.",
        desired_resolution="Reassign task T-123 to model-alpha",
        urgency=Urgency.STANDARD
    )

    # Add evidence
    request.evidence.append(Evidence(
        evidence_type="log",
        reference="capability-registry/scores/2026-02-08",
        summary="Capability scores show model-alpha: 0.92, model-beta: 0.78 for task type",
        submitted_by="model-alpha"
    ))

    arb_id = engine.file_dispute(request)
    print(f"Dispute filed: {arb_id}")

    # Deliberate
    analysis = engine.deliberate(arb_id)
    print(f"Deliberation: {json.dumps(analysis, indent=2)}")

    # Issue ruling
    ruling = Ruling(
        arbitration_id=arb_id,
        arbitrator="governance-model-1",
        summary="Task T-123 reassigned to model-alpha based on capability precedent",
        findings=[
            Finding("model-alpha", True, "Higher capability score verified"),
            Finding("model-beta", False, "Assignment was arbitrary, not capability-based")
        ],
        reasoning={
            "precedent_applied": "PREC-001: Capability match > prior assignment",
            "evidence_weight": "Capability registry logs verified"
        },
        orders=[
            Order("model-beta", "Release task T-123", datetime.utcnow() + timedelta(minutes=5)),
            Order("model-alpha", "Accept task T-123", datetime.utcnow() + timedelta(minutes=10))
        ],
        appeal_deadline=datetime.utcnow() + timedelta(hours=24)
    )

    ruling_id = engine.issue_ruling(arb_id, ruling)
    print(f"Ruling issued: {ruling_id}")

    # Get final status
    status = engine.get_dispute_status(arb_id)
    print(f"Final status: {json.dumps(status, indent=2, default=str)}")


if __name__ == "__main__":
    main()
