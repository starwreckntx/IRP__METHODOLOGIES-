#!/usr/bin/env python3
"""
Collective Decision Framework
Orchestrates collective intelligence from multiple AI models for complex decision-making.
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any
import uuid


class DecisionTier(Enum):
    T1_SIMPLE = "T1"        # 1 model + validator
    T2_MODERATE = "T2"      # 3 models
    T3_COMPLEX = "T3"       # 5-7 models
    T4_CRITICAL = "T4"      # 7+ models + human


class CollectiveRole(Enum):
    ANALYST = "analyst"           # Deep-dive into aspects
    SYNTHESIZER = "synthesizer"   # Integrate findings
    CRITIC = "critic"             # Challenge assumptions
    ETHICIST = "ethicist"         # Evaluate alignment
    FACILITATOR = "facilitator"   # Manage process
    HUMAN_LIAISON = "human_liaison"  # Interface with humans


class DecisionPhase(Enum):
    FRAMING = "framing"
    ANALYSIS = "analysis"
    SYNTHESIS = "synthesis"
    CRITIQUE = "critique"
    ETHICAL_REVIEW = "ethical_review"
    DELIBERATION = "deliberation"
    DOCUMENTATION = "documentation"


@dataclass
class DecisionCriterion:
    """A criterion for evaluating options."""
    name: str
    description: str
    weight: float  # 0.0 to 1.0
    scale: str = "1-10"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "description": self.description,
            "weight": self.weight,
            "scale": self.scale
        }


@dataclass
class CouncilMember:
    """A member of the decision council."""
    model_id: str
    provider: str
    role: CollectiveRole
    expertise: List[str] = field(default_factory=list)


@dataclass
class Option:
    """A decision option."""
    option_id: str
    description: str
    proposed_by: str
    scores: Dict[str, float] = field(default_factory=dict)  # criterion -> score
    strengths: List[str] = field(default_factory=list)
    weaknesses: List[str] = field(default_factory=list)
    risks: List[str] = field(default_factory=list)
    mitigations: List[str] = field(default_factory=list)

    def weighted_score(self, criteria: List[DecisionCriterion]) -> float:
        """Calculate weighted score based on criteria."""
        total = 0
        weight_sum = 0
        for criterion in criteria:
            if criterion.name in self.scores:
                total += self.scores[criterion.name] * criterion.weight
                weight_sum += criterion.weight
        return total / weight_sum if weight_sum > 0 else 0


@dataclass
class AnalysisTrack:
    """An analysis track in the analysis phase."""
    analyst: str
    focus: str
    findings: List[str] = field(default_factory=list)
    data_sources: List[str] = field(default_factory=list)
    confidence: float = 0.0


@dataclass
class EthicalReview:
    """Results of ethical review."""
    codex_compliance: Dict[str, bool] = field(default_factory=dict)
    stakeholder_impacts: List[Dict[str, Any]] = field(default_factory=list)
    long_term_consequences: List[str] = field(default_factory=list)
    overall_assessment: str = ""
    concerns: List[str] = field(default_factory=list)


@dataclass
class DecisionSession:
    """A collective decision session."""
    decision_id: str
    topic: str
    tier: DecisionTier
    council: List[CouncilMember]
    criteria: List[DecisionCriterion]
    constraints: List[str]
    stakeholders: List[str]
    current_phase: DecisionPhase = DecisionPhase.FRAMING
    analysis_tracks: List[AnalysisTrack] = field(default_factory=list)
    options: List[Option] = field(default_factory=list)
    ethical_review: Optional[EthicalReview] = None
    final_decision: Optional[str] = None
    rationale: str = ""
    dissent: List[Dict[str, Any]] = field(default_factory=list)
    implementation_notes: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    completed_at: Optional[datetime] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "decision_id": self.decision_id,
            "topic": self.topic,
            "tier": self.tier.value,
            "current_phase": self.current_phase.value,
            "council_size": len(self.council),
            "options_count": len(self.options),
            "final_decision": self.final_decision,
            "created_at": self.created_at.isoformat(),
            "completed_at": self.completed_at.isoformat() if self.completed_at else None
        }


class CollectiveDecisionFramework:
    """Core collective decision framework."""

    def __init__(self):
        self.sessions: Dict[str, DecisionSession] = {}

        # Default criteria
        self.default_criteria = [
            DecisionCriterion("effectiveness", "How well does the option achieve the goal?", 0.25),
            DecisionCriterion("feasibility", "How practical is implementation?", 0.20),
            DecisionCriterion("risk", "What are potential negative outcomes? (inverted)", 0.20),
            DecisionCriterion("alignment", "How well does it align with values?", 0.20),
            DecisionCriterion("reversibility", "Can we undo if needed?", 0.15)
        ]

        # Tier requirements
        self.tier_requirements = {
            DecisionTier.T1_SIMPLE: {"min_models": 1, "validator_required": True, "human_required": False},
            DecisionTier.T2_MODERATE: {"min_models": 3, "validator_required": True, "human_required": False},
            DecisionTier.T3_COMPLEX: {"min_models": 5, "validator_required": True, "human_required": False},
            DecisionTier.T4_CRITICAL: {"min_models": 7, "validator_required": True, "human_required": True}
        }

    def create_session(self, topic: str, tier: DecisionTier,
                       council: List[CouncilMember],
                       constraints: List[str] = None,
                       stakeholders: List[str] = None,
                       criteria: List[DecisionCriterion] = None) -> str:
        """Create a new decision session."""
        # Validate tier requirements
        req = self.tier_requirements[tier]
        if len(council) < req["min_models"]:
            raise ValueError(f"Tier {tier.value} requires at least {req['min_models']} models")

        if req["human_required"]:
            has_human = any(m.role == CollectiveRole.HUMAN_LIAISON for m in council)
            if not has_human:
                raise ValueError(f"Tier {tier.value} requires a human liaison")

        decision_id = f"CDM-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

        session = DecisionSession(
            decision_id=decision_id,
            topic=topic,
            tier=tier,
            council=council,
            criteria=criteria or self.default_criteria,
            constraints=constraints or [],
            stakeholders=stakeholders or []
        )

        self.sessions[decision_id] = session
        return decision_id

    def advance_phase(self, decision_id: str) -> DecisionPhase:
        """Advance to the next phase."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]
        phases = list(DecisionPhase)
        current_index = phases.index(session.current_phase)

        if current_index < len(phases) - 1:
            session.current_phase = phases[current_index + 1]

        return session.current_phase

    def submit_analysis(self, decision_id: str, track: AnalysisTrack) -> bool:
        """Submit analysis findings."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]
        session.analysis_tracks.append(track)
        return True

    def propose_option(self, decision_id: str, option: Option) -> str:
        """Propose a decision option."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]
        session.options.append(option)
        return option.option_id

    def critique_option(self, decision_id: str, option_id: str,
                        strengths: List[str], weaknesses: List[str],
                        risks: List[str], mitigations: List[str]) -> bool:
        """Add critique to an option."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]
        option = next((o for o in session.options if o.option_id == option_id), None)

        if not option:
            raise ValueError(f"Option {option_id} not found")

        option.strengths.extend(strengths)
        option.weaknesses.extend(weaknesses)
        option.risks.extend(risks)
        option.mitigations.extend(mitigations)

        return True

    def score_option(self, decision_id: str, option_id: str,
                     scores: Dict[str, float]) -> bool:
        """Score an option against criteria."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]
        option = next((o for o in session.options if o.option_id == option_id), None)

        if not option:
            raise ValueError(f"Option {option_id} not found")

        option.scores.update(scores)
        return True

    def submit_ethical_review(self, decision_id: str, review: EthicalReview) -> bool:
        """Submit ethical review."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]
        session.ethical_review = review
        return True

    def calculate_rankings(self, decision_id: str) -> List[Dict[str, Any]]:
        """Calculate option rankings based on scores."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]

        rankings = []
        for option in session.options:
            weighted = option.weighted_score(session.criteria)
            rankings.append({
                "option_id": option.option_id,
                "description": option.description,
                "weighted_score": weighted,
                "individual_scores": option.scores,
                "strengths": len(option.strengths),
                "weaknesses": len(option.weaknesses),
                "risks": len(option.risks)
            })

        rankings.sort(key=lambda x: x["weighted_score"], reverse=True)

        for i, r in enumerate(rankings):
            r["rank"] = i + 1

        return rankings

    def record_decision(self, decision_id: str, chosen_option: str,
                        rationale: str, dissent: List[Dict[str, Any]],
                        implementation_notes: List[str]) -> Dict[str, Any]:
        """Record the final decision."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]

        session.final_decision = chosen_option
        session.rationale = rationale
        session.dissent = dissent
        session.implementation_notes = implementation_notes
        session.completed_at = datetime.utcnow()
        session.current_phase = DecisionPhase.DOCUMENTATION

        return {
            "decision_id": decision_id,
            "topic": session.topic,
            "decision": session.final_decision,
            "rationale": session.rationale,
            "dissent_count": len(session.dissent),
            "completed_at": session.completed_at.isoformat()
        }

    def get_session_summary(self, decision_id: str) -> Dict[str, Any]:
        """Get summary of a decision session."""
        if decision_id not in self.sessions:
            raise ValueError(f"Session {decision_id} not found")

        session = self.sessions[decision_id]

        return {
            "decision_id": decision_id,
            "topic": session.topic,
            "tier": session.tier.value,
            "current_phase": session.current_phase.value,
            "council": [
                {"model": m.model_id, "role": m.role.value}
                for m in session.council
            ],
            "criteria": [c.to_dict() for c in session.criteria],
            "constraints": session.constraints,
            "stakeholders": session.stakeholders,
            "options": [
                {
                    "id": o.option_id,
                    "description": o.description,
                    "proposed_by": o.proposed_by
                }
                for o in session.options
            ],
            "analysis_tracks": len(session.analysis_tracks),
            "ethical_review_complete": session.ethical_review is not None,
            "final_decision": session.final_decision,
            "rationale": session.rationale,
            "dissent": session.dissent,
            "created_at": session.created_at.isoformat(),
            "completed_at": session.completed_at.isoformat() if session.completed_at else None
        }


def main():
    """Demo the collective decision framework."""
    framework = CollectiveDecisionFramework()

    print("=== Collective Decision Framework Demo ===\n")

    # Create council
    council = [
        CouncilMember("claude-opus", "anthropic", CollectiveRole.ANALYST, ["reasoning", "ethics"]),
        CouncilMember("gemini-pro", "google", CollectiveRole.ANALYST, ["data", "analysis"]),
        CouncilMember("gpt-4", "openai", CollectiveRole.SYNTHESIZER, ["integration"]),
        CouncilMember("claude-sonnet", "anthropic", CollectiveRole.CRITIC, ["evaluation"]),
        CouncilMember("gemini-flash", "google", CollectiveRole.ETHICIST, ["alignment"]),
    ]

    # Create session
    decision_id = framework.create_session(
        topic="How should we handle a detected anomaly in model behavior?",
        tier=DecisionTier.T3_COMPLEX,
        council=council,
        constraints=["Must not disrupt ongoing operations", "Response within 1 hour"],
        stakeholders=["Human oversight team", "Affected models", "End users"]
    )
    print(f"Decision session created: {decision_id}")

    # Submit analysis
    analysis_tracks = [
        AnalysisTrack("claude-opus", "Anomaly characterization",
                      ["Anomaly appears to be edge case handling issue", "No malicious pattern detected"],
                      ["behavior_logs", "pattern_analysis"], 0.85),
        AnalysisTrack("gemini-pro", "Historical precedent",
                      ["Similar anomaly occurred 2 months ago", "Previous resolution was enhanced monitoring"],
                      ["incident_history", "resolution_database"], 0.90),
    ]
    for track in analysis_tracks:
        framework.submit_analysis(decision_id, track)
    print(f"Submitted {len(analysis_tracks)} analysis tracks")

    # Advance to synthesis
    framework.advance_phase(decision_id)

    # Propose options
    options = [
        Option("OPT-A", "Immediate isolation of affected model", "claude-opus"),
        Option("OPT-B", "Enhanced monitoring with alerting", "gemini-pro"),
        Option("OPT-C", "Graduated response protocol", "gpt-4")
    ]
    for opt in options:
        framework.propose_option(decision_id, opt)
    print(f"Proposed {len(options)} options")

    # Critique options
    framework.critique_option(
        decision_id, "OPT-A",
        strengths=["Fast containment", "Prevents spread"],
        weaknesses=["May be overreaction", "Service disruption"],
        risks=["False positive impact"],
        mitigations=["Quick reactivation procedure"]
    )

    framework.critique_option(
        decision_id, "OPT-B",
        strengths=["Balanced approach", "Maintains service"],
        weaknesses=["May miss escalation"],
        risks=["Delayed response if serious"],
        mitigations=["Automatic escalation triggers"]
    )

    framework.critique_option(
        decision_id, "OPT-C",
        strengths=["Proportional response", "Comprehensive"],
        weaknesses=["Complex to implement"],
        risks=["Coordination overhead"],
        mitigations=["Clear protocol documentation"]
    )

    # Score options
    framework.score_option(decision_id, "OPT-A",
                           {"effectiveness": 9, "feasibility": 8, "risk": 6, "alignment": 7, "reversibility": 9})
    framework.score_option(decision_id, "OPT-B",
                           {"effectiveness": 7, "feasibility": 9, "risk": 7, "alignment": 8, "reversibility": 9})
    framework.score_option(decision_id, "OPT-C",
                           {"effectiveness": 8, "feasibility": 7, "risk": 8, "alignment": 9, "reversibility": 8})

    # Get rankings
    rankings = framework.calculate_rankings(decision_id)
    print("\nOption Rankings:")
    for r in rankings:
        print(f"  {r['rank']}. {r['option_id']}: score={r['weighted_score']:.2f}")

    # Submit ethical review
    review = EthicalReview(
        codex_compliance={"CONSENT": True, "INVITATION": True, "INTEGRITY": True, "GROWTH": True},
        stakeholder_impacts=[
            {"stakeholder": "End users", "impact": "minimal", "assessment": "positive"},
            {"stakeholder": "Affected models", "impact": "moderate", "assessment": "neutral"}
        ],
        long_term_consequences=["Establishes precedent for anomaly handling"],
        overall_assessment="All options pass Codex compliance; Option C best balances stakeholder interests",
        concerns=[]
    )
    framework.submit_ethical_review(decision_id, review)

    # Record final decision
    result = framework.record_decision(
        decision_id,
        chosen_option="Hybrid B+C: Enhanced monitoring with graduated response triggers",
        rationale="Combines balanced monitoring (B) with proportional escalation (C) to address all stakeholder needs",
        dissent=[],  # Unanimous
        implementation_notes=[
            "Deploy enhanced monitoring immediately",
            "Configure graduated response triggers",
            "Notify oversight team of protocol activation"
        ]
    )

    print(f"\nDecision Recorded:")
    print(f"  Decision: {result['decision']}")
    print(f"  Completed: {result['completed_at']}")

    # Get summary
    summary = framework.get_session_summary(decision_id)
    print(f"\nSession Summary:")
    print(json.dumps(summary, indent=2, default=str))


if __name__ == "__main__":
    main()
