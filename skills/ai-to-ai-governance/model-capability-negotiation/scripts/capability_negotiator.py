#!/usr/bin/env python3
"""
Model Capability Negotiation System
Facilitates capability discovery and task allocation between AI models.
"""

import json
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
import uuid


class CapabilityCategory(Enum):
    COGNITIVE = "cognitive"       # Reasoning abilities
    DOMAIN = "domain"             # Subject expertise
    MODALITY = "modality"         # Input/output types
    TEMPORAL = "temporal"         # Context handling
    OPERATIONAL = "operational"   # Execution capabilities


class NegotiationMode(Enum):
    COOPERATIVE = "cooperative"   # Full sharing, collective optimization
    COMPETITIVE = "competitive"   # Bidding for preferred tasks
    HYBRID = "hybrid"             # Cooperative critical, competitive optional


class Role(Enum):
    LEAD = "lead"           # Primary task executor
    SUPPORT = "support"     # Assists lead model
    VALIDATOR = "validator" # Checks outputs
    FALLBACK = "fallback"   # Backup if lead fails
    OBSERVER = "observer"   # Monitors process


@dataclass
class Capability:
    """A single capability of a model."""
    name: str
    category: CapabilityCategory
    proficiency: float  # 0.0 to 1.0
    confidence_interval: Tuple[float, float] = (0.0, 1.0)
    benchmarks: List[str] = field(default_factory=list)
    limitations: List[str] = field(default_factory=list)
    latency_ms: int = 0
    token_cost: float = 0.0
    resource_intensity: str = "medium"  # low, medium, high

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "category": self.category.value,
            "proficiency": self.proficiency,
            "confidence_interval": list(self.confidence_interval),
            "benchmarks": self.benchmarks,
            "limitations": self.limitations,
            "cost": {
                "latency_ms": self.latency_ms,
                "token_cost": self.token_cost,
                "resource_intensity": self.resource_intensity
            }
        }


@dataclass
class CapabilityManifest:
    """A model's complete capability declaration."""
    model_id: str
    provider: str
    version: str = "1.0.0"
    capabilities: List[Capability] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)
    signature: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "capability_manifest": {
                "version": self.version,
                "timestamp": self.timestamp.isoformat(),
                "capabilities": [c.to_dict() for c in self.capabilities],
                "signature": self.signature
            }
        }

    def get_capability(self, name: str) -> Optional[Capability]:
        """Get a specific capability by name."""
        for cap in self.capabilities:
            if cap.name.lower() == name.lower():
                return cap
        return None


@dataclass
class TaskRequirement:
    """A requirement for a task."""
    capability_name: str
    minimum_proficiency: float = 0.5
    weight: float = 1.0
    required: bool = True


@dataclass
class Bid:
    """A model's bid for a task."""
    model_id: str
    proposed_role: Role
    confidence: float
    cost_estimate: Dict[str, Any]
    conditions: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class Assignment:
    """Final task assignment."""
    model_id: str
    task_id: str
    role: Role
    score: float


@dataclass
class NegotiationSession:
    """A capability negotiation session."""
    session_id: str
    task_description: str
    requirements: List[TaskRequirement]
    mode: NegotiationMode
    manifests: Dict[str, CapabilityManifest] = field(default_factory=dict)
    bids: List[Bid] = field(default_factory=list)
    assignments: List[Assignment] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)


class CapabilityNegotiator:
    """Core engine for capability negotiation."""

    def __init__(self):
        self.sessions: Dict[str, NegotiationSession] = {}
        self.model_registrations: Dict[str, CapabilityManifest] = {}
        self.performance_history: Dict[str, List[Dict[str, Any]]] = {}

    def register_model(self, manifest: CapabilityManifest) -> bool:
        """Register a model's capabilities."""
        self.model_registrations[manifest.model_id] = manifest
        return True

    def create_session(self, task_description: str,
                       requirements: List[TaskRequirement],
                       mode: NegotiationMode = NegotiationMode.COOPERATIVE) -> str:
        """Create a new negotiation session."""
        session_id = f"NEG-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

        session = NegotiationSession(
            session_id=session_id,
            task_description=task_description,
            requirements=requirements,
            mode=mode
        )

        self.sessions[session_id] = session
        return session_id

    def discover_capabilities(self, session_id: str,
                              model_ids: Optional[List[str]] = None) -> Dict[str, Any]:
        """Discover capabilities of participating models."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Get manifests for specified models or all registered
        if model_ids:
            for model_id in model_ids:
                if model_id in self.model_registrations:
                    session.manifests[model_id] = self.model_registrations[model_id]
        else:
            session.manifests = dict(self.model_registrations)

        return {
            "session_id": session_id,
            "discovered_models": list(session.manifests.keys()),
            "manifests": {
                model_id: manifest.to_dict()
                for model_id, manifest in session.manifests.items()
            }
        }

    def match_capabilities(self, session_id: str) -> Dict[str, Any]:
        """Match model capabilities to task requirements."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]
        scores = {}

        for model_id, manifest in session.manifests.items():
            score = 0.0
            matched_requirements = []
            unmatched_requirements = []

            for req in session.requirements:
                cap = manifest.get_capability(req.capability_name)
                if cap and cap.proficiency >= req.minimum_proficiency:
                    # Calculate weighted score
                    proficiency_factor = cap.proficiency * req.weight

                    # Apply cost factor (lower cost = better)
                    cost_factor = 1.0
                    if cap.resource_intensity == "high":
                        cost_factor = 0.8
                    elif cap.resource_intensity == "low":
                        cost_factor = 1.1

                    req_score = proficiency_factor * cost_factor
                    score += req_score
                    matched_requirements.append({
                        "requirement": req.capability_name,
                        "proficiency": cap.proficiency,
                        "score": req_score
                    })
                elif req.required:
                    unmatched_requirements.append(req.capability_name)

            # Penalize for unmatched required capabilities
            if unmatched_requirements:
                score *= 0.5 ** len(unmatched_requirements)

            scores[model_id] = {
                "total_score": score,
                "matched": matched_requirements,
                "unmatched": unmatched_requirements
            }

        # Rank by score
        ranked = sorted(scores.items(), key=lambda x: x[1]["total_score"], reverse=True)

        return {
            "session_id": session_id,
            "rankings": [
                {"rank": i + 1, "model_id": model_id, **data}
                for i, (model_id, data) in enumerate(ranked)
            ]
        }

    def submit_bid(self, session_id: str, bid: Bid) -> bool:
        """Submit a bid for a task."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Verify model is registered
        if bid.model_id not in session.manifests:
            raise ValueError(f"Model {bid.model_id} not in session")

        session.bids.append(bid)
        return True

    def allocate_roles(self, session_id: str) -> Dict[str, Any]:
        """Allocate roles based on capabilities and bids."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Get capability scores
        match_result = self.match_capabilities(session_id)
        rankings = match_result["rankings"]

        # Combine with bids
        role_allocations = {}
        assigned_models = set()

        # Assign lead to highest scorer
        if rankings:
            lead_candidate = rankings[0]
            role_allocations[Role.LEAD] = Assignment(
                model_id=lead_candidate["model_id"],
                task_id=session_id,
                role=Role.LEAD,
                score=lead_candidate["total_score"]
            )
            assigned_models.add(lead_candidate["model_id"])

        # Assign support to second highest
        if len(rankings) > 1:
            support_candidate = rankings[1]
            role_allocations[Role.SUPPORT] = Assignment(
                model_id=support_candidate["model_id"],
                task_id=session_id,
                role=Role.SUPPORT,
                score=support_candidate["total_score"]
            )
            assigned_models.add(support_candidate["model_id"])

        # Assign validator to third (or someone with different perspective)
        if len(rankings) > 2:
            # Prefer model from different provider
            validator_candidate = None
            for ranking in rankings[2:]:
                if ranking["model_id"] not in assigned_models:
                    model_manifest = session.manifests.get(ranking["model_id"])
                    lead_manifest = session.manifests.get(rankings[0]["model_id"])
                    if model_manifest and lead_manifest:
                        if model_manifest.provider != lead_manifest.provider:
                            validator_candidate = ranking
                            break

            if not validator_candidate and len(rankings) > 2:
                validator_candidate = rankings[2]

            if validator_candidate:
                role_allocations[Role.VALIDATOR] = Assignment(
                    model_id=validator_candidate["model_id"],
                    task_id=session_id,
                    role=Role.VALIDATOR,
                    score=validator_candidate["total_score"]
                )

        # Store assignments
        session.assignments = list(role_allocations.values())

        return {
            "session_id": session_id,
            "allocations": {
                role.value: {
                    "model_id": assignment.model_id,
                    "score": assignment.score
                }
                for role, assignment in role_allocations.items()
            },
            "unassigned_models": [
                r["model_id"] for r in rankings
                if r["model_id"] not in assigned_models
            ]
        }

    def verify_capability_claim(self, model_id: str,
                                capability_name: str) -> Dict[str, Any]:
        """Verify a model's capability claim against historical performance."""
        history = self.performance_history.get(model_id, [])

        if not history:
            return {
                "model_id": model_id,
                "capability": capability_name,
                "verification": "insufficient_data",
                "confidence": 0.5
            }

        # Filter relevant performance data
        relevant = [h for h in history if h.get("capability") == capability_name]

        if not relevant:
            return {
                "model_id": model_id,
                "capability": capability_name,
                "verification": "no_data",
                "confidence": 0.5
            }

        # Calculate actual performance
        actual_scores = [h.get("actual_score", 0) for h in relevant]
        avg_actual = sum(actual_scores) / len(actual_scores)

        # Get claimed proficiency
        manifest = self.model_registrations.get(model_id)
        claimed = 0.0
        if manifest:
            cap = manifest.get_capability(capability_name)
            if cap:
                claimed = cap.proficiency

        # Compare
        accuracy = 1.0 - abs(claimed - avg_actual)

        return {
            "model_id": model_id,
            "capability": capability_name,
            "claimed_proficiency": claimed,
            "actual_performance": avg_actual,
            "accuracy": accuracy,
            "verification": "verified" if accuracy > 0.8 else "discrepancy",
            "confidence": min(len(relevant) / 10, 1.0)  # More data = higher confidence
        }

    def record_performance(self, model_id: str, capability: str,
                           actual_score: float, task_context: str) -> bool:
        """Record actual performance for capability verification."""
        if model_id not in self.performance_history:
            self.performance_history[model_id] = []

        self.performance_history[model_id].append({
            "capability": capability,
            "actual_score": actual_score,
            "task_context": task_context,
            "timestamp": datetime.utcnow().isoformat()
        })

        return True


def main():
    """Demo the capability negotiation system."""
    negotiator = CapabilityNegotiator()

    print("=== Model Capability Negotiation Demo ===\n")

    # Register models with capabilities
    claude_manifest = CapabilityManifest(
        model_id="claude-opus",
        provider="anthropic",
        capabilities=[
            Capability("code_analysis", CapabilityCategory.DOMAIN, 0.92,
                       benchmarks=["humaneval_95"]),
            Capability("documentation_writing", CapabilityCategory.DOMAIN, 0.88),
            Capability("technical_accuracy", CapabilityCategory.COGNITIVE, 0.90),
            Capability("long_context", CapabilityCategory.TEMPORAL, 0.95,
                       resource_intensity="high")
        ]
    )

    gemini_manifest = CapabilityManifest(
        model_id="gemini-pro",
        provider="google",
        capabilities=[
            Capability("code_analysis", CapabilityCategory.DOMAIN, 0.85),
            Capability("documentation_writing", CapabilityCategory.DOMAIN, 0.82),
            Capability("technical_accuracy", CapabilityCategory.COGNITIVE, 0.88),
            Capability("multimodal", CapabilityCategory.MODALITY, 0.92)
        ]
    )

    gpt_manifest = CapabilityManifest(
        model_id="gpt-4",
        provider="openai",
        capabilities=[
            Capability("code_analysis", CapabilityCategory.DOMAIN, 0.88),
            Capability("documentation_writing", CapabilityCategory.DOMAIN, 0.91),
            Capability("technical_accuracy", CapabilityCategory.COGNITIVE, 0.85),
            Capability("tool_use", CapabilityCategory.OPERATIONAL, 0.90)
        ]
    )

    negotiator.register_model(claude_manifest)
    negotiator.register_model(gemini_manifest)
    negotiator.register_model(gpt_manifest)

    print("Registered 3 models")

    # Create negotiation session
    requirements = [
        TaskRequirement("code_analysis", minimum_proficiency=0.8, weight=1.0),
        TaskRequirement("documentation_writing", minimum_proficiency=0.7, weight=0.8),
        TaskRequirement("technical_accuracy", minimum_proficiency=0.8, weight=0.9)
    ]

    session_id = negotiator.create_session(
        task_description="Analyze code repository and generate documentation",
        requirements=requirements,
        mode=NegotiationMode.COOPERATIVE
    )
    print(f"\nSession created: {session_id}")

    # Discover capabilities
    discovery = negotiator.discover_capabilities(session_id)
    print(f"Discovered {len(discovery['discovered_models'])} models")

    # Match capabilities
    matches = negotiator.match_capabilities(session_id)
    print(f"\nCapability Rankings:")
    for ranking in matches["rankings"]:
        print(f"  {ranking['rank']}. {ranking['model_id']}: "
              f"score={ranking['total_score']:.2f}")

    # Allocate roles
    allocation = negotiator.allocate_roles(session_id)
    print(f"\nRole Allocations:")
    for role, data in allocation["allocations"].items():
        print(f"  {role}: {data['model_id']} (score: {data['score']:.2f})")


if __name__ == "__main__":
    main()
