#!/usr/bin/env python3
"""
AI Consensus Protocol Engine
Enables multiple AI models to reach collective agreement on decisions.
"""

import json
from datetime import datetime, timedelta
from enum import Enum
from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any, Tuple
import uuid
import statistics


class VotingSystem(Enum):
    UNANIMOUS = "unanimous"           # 100% agreement
    SUPERMAJORITY = "supermajority"   # 66%+ agreement
    SIMPLE_MAJORITY = "simple_majority"  # 50%+ agreement
    WEIGHTED = "weighted"             # Expertise-weighted
    RANKED_CHOICE = "ranked_choice"   # Iterative elimination


class ConsensusStatus(Enum):
    INITIATED = "initiated"
    PROPOSAL = "proposal"
    DELIBERATION = "deliberation"
    VOTING = "voting"
    ACHIEVED = "achieved"
    NEAR_CONSENSUS = "near_consensus"
    DEADLOCK = "deadlock"
    ESCALATED = "escalated"


class DecisionCategory(Enum):
    OPERATIONAL = "operational"       # Min 3, simple majority
    STRATEGIC = "strategic"           # Min 5, supermajority
    CONSTITUTIONAL = "constitutional" # Min 7, unanimous
    EMERGENCY = "emergency"           # Min 2, simple majority


@dataclass
class Participant:
    """A model participating in consensus."""
    model_id: str
    provider: str
    expertise_weight: float = 1.0
    trust_level: int = 2


@dataclass
class Position:
    """A model's position on a topic."""
    model_id: str
    recommendation: str
    confidence: float
    reasoning: str
    evidence: List[str] = field(default_factory=list)
    concerns: List[str] = field(default_factory=list)
    alternatives: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "model_id": self.model_id,
            "position": {
                "recommendation": self.recommendation,
                "confidence": self.confidence,
                "reasoning": self.reasoning,
                "evidence": self.evidence,
                "concerns": self.concerns,
                "alternatives": self.alternatives
            },
            "timestamp": self.timestamp.isoformat()
        }


@dataclass
class Vote:
    """A model's vote."""
    model_id: str
    choice: str
    weight: float = 1.0
    conditions: List[str] = field(default_factory=list)
    timestamp: datetime = field(default_factory=datetime.utcnow)


@dataclass
class ConsensusSession:
    """A consensus-building session."""
    session_id: str
    topic: str
    category: DecisionCategory
    voting_system: VotingSystem
    participants: List[Participant]
    positions: List[Position] = field(default_factory=list)
    votes: List[Vote] = field(default_factory=list)
    status: ConsensusStatus = ConsensusStatus.INITIATED
    rounds_completed: int = 0
    max_rounds: int = 3
    created_at: datetime = field(default_factory=datetime.utcnow)
    decision: Optional[str] = None
    dissent: List[Dict[str, Any]] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "session_id": self.session_id,
            "topic": self.topic,
            "category": self.category.value,
            "voting_system": self.voting_system.value,
            "participants": [{"model_id": p.model_id, "weight": p.expertise_weight}
                             for p in self.participants],
            "positions": [p.to_dict() for p in self.positions],
            "status": self.status.value,
            "rounds_completed": self.rounds_completed,
            "decision": self.decision,
            "dissent": self.dissent
        }


class ConsensusEngine:
    """Core engine for AI consensus protocol."""

    def __init__(self):
        self.sessions: Dict[str, ConsensusSession] = {}
        self.thresholds = {
            VotingSystem.UNANIMOUS: 1.0,
            VotingSystem.SUPERMAJORITY: 0.66,
            VotingSystem.SIMPLE_MAJORITY: 0.50,
            VotingSystem.WEIGHTED: 0.50,  # Of weighted votes
            VotingSystem.RANKED_CHOICE: 0.50  # After elimination
        }

    def create_session(self, topic: str, category: DecisionCategory,
                       participants: List[Participant],
                       voting_system: Optional[VotingSystem] = None) -> str:
        """Create a new consensus session."""
        # Validate minimum participants
        min_participants = {
            DecisionCategory.OPERATIONAL: 3,
            DecisionCategory.STRATEGIC: 5,
            DecisionCategory.CONSTITUTIONAL: 7,
            DecisionCategory.EMERGENCY: 2
        }

        if len(participants) < min_participants[category]:
            raise ValueError(
                f"{category.value} decisions require at least "
                f"{min_participants[category]} participants"
            )

        # Validate trust levels
        for p in participants:
            if p.trust_level < 2:
                raise ValueError(f"Participant {p.model_id} has insufficient trust level")

        # Default voting system based on category
        if voting_system is None:
            voting_system = {
                DecisionCategory.OPERATIONAL: VotingSystem.SIMPLE_MAJORITY,
                DecisionCategory.STRATEGIC: VotingSystem.SUPERMAJORITY,
                DecisionCategory.CONSTITUTIONAL: VotingSystem.UNANIMOUS,
                DecisionCategory.EMERGENCY: VotingSystem.SIMPLE_MAJORITY
            }[category]

        session_id = f"CONS-{datetime.now().strftime('%Y%m%d%H%M%S')}-{uuid.uuid4().hex[:6]}"

        session = ConsensusSession(
            session_id=session_id,
            topic=topic,
            category=category,
            voting_system=voting_system,
            participants=participants
        )

        self.sessions[session_id] = session
        return session_id

    def submit_position(self, session_id: str, position: Position) -> bool:
        """Submit a model's position on the topic."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Verify participant
        participant_ids = [p.model_id for p in session.participants]
        if position.model_id not in participant_ids:
            raise ValueError(f"Model {position.model_id} is not a participant")

        # Check if already submitted in this round
        existing = [p for p in session.positions
                    if p.model_id == position.model_id]
        if len(existing) > session.rounds_completed:
            raise ValueError(f"Model {position.model_id} has already submitted position this round")

        session.positions.append(position)
        session.status = ConsensusStatus.PROPOSAL

        # Check if all positions received for this round
        current_round_positions = [p for p in session.positions]
        if len(current_round_positions) >= len(session.participants) * (session.rounds_completed + 1):
            session.status = ConsensusStatus.DELIBERATION

        return True

    def analyze_positions(self, session_id: str) -> Dict[str, Any]:
        """Analyze current positions to find common ground."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Get latest positions
        latest_positions = {}
        for pos in session.positions:
            latest_positions[pos.model_id] = pos

        positions = list(latest_positions.values())

        if not positions:
            return {"status": "no_positions", "common_ground": [], "disagreements": []}

        # Extract unique recommendations
        recommendations = {}
        for pos in positions:
            rec = pos.recommendation
            if rec not in recommendations:
                recommendations[rec] = {
                    "supporters": [],
                    "confidence_sum": 0,
                    "evidence": set()
                }
            recommendations[rec]["supporters"].append(pos.model_id)
            recommendations[rec]["confidence_sum"] += pos.confidence
            recommendations[rec]["evidence"].update(pos.evidence)

        # Find common concerns
        all_concerns = []
        for pos in positions:
            all_concerns.extend(pos.concerns)
        concern_counts = {}
        for concern in all_concerns:
            concern_counts[concern] = concern_counts.get(concern, 0) + 1
        shared_concerns = [c for c, count in concern_counts.items()
                          if count > len(positions) / 2]

        # Calculate agreement level
        max_support = max(len(r["supporters"]) for r in recommendations.values())
        agreement_ratio = max_support / len(positions)

        return {
            "status": "analyzed",
            "recommendations": {
                k: {
                    "supporters": v["supporters"],
                    "avg_confidence": v["confidence_sum"] / len(v["supporters"]),
                    "evidence_count": len(v["evidence"])
                }
                for k, v in recommendations.items()
            },
            "shared_concerns": shared_concerns,
            "agreement_ratio": agreement_ratio,
            "near_consensus": agreement_ratio >= 0.66
        }

    def submit_vote(self, session_id: str, vote: Vote) -> bool:
        """Submit a model's vote."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        # Get participant weight
        participant = next(
            (p for p in session.participants if p.model_id == vote.model_id),
            None
        )
        if not participant:
            raise ValueError(f"Model {vote.model_id} is not a participant")

        # Apply expertise weight for weighted voting
        if session.voting_system == VotingSystem.WEIGHTED:
            vote.weight = participant.expertise_weight

        session.votes.append(vote)
        session.status = ConsensusStatus.VOTING

        return True

    def calculate_result(self, session_id: str) -> Dict[str, Any]:
        """Calculate voting result."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]

        if not session.votes:
            return {"status": "no_votes"}

        # Tally votes
        vote_tallies = {}
        total_weight = 0

        for vote in session.votes:
            if vote.choice not in vote_tallies:
                vote_tallies[vote.choice] = {"weight": 0, "count": 0, "voters": []}
            vote_tallies[vote.choice]["weight"] += vote.weight
            vote_tallies[vote.choice]["count"] += 1
            vote_tallies[vote.choice]["voters"].append(vote.model_id)
            total_weight += vote.weight

        # Find winner
        threshold = self.thresholds[session.voting_system]

        if session.voting_system == VotingSystem.RANKED_CHOICE:
            # Simplified ranked choice (would need ranked votes in real impl)
            winner = max(vote_tallies.items(), key=lambda x: x[1]["weight"])
            winner_ratio = winner[1]["weight"] / total_weight
        else:
            winner = max(vote_tallies.items(), key=lambda x: x[1]["weight"])
            winner_ratio = winner[1]["weight"] / total_weight

        # Determine outcome
        if winner_ratio >= threshold:
            session.status = ConsensusStatus.ACHIEVED
            session.decision = winner[0]

            # Record dissent
            for choice, data in vote_tallies.items():
                if choice != winner[0]:
                    session.dissent.append({
                        "choice": choice,
                        "supporters": data["voters"],
                        "weight": data["weight"]
                    })
        elif winner_ratio >= threshold - 0.10:
            session.status = ConsensusStatus.NEAR_CONSENSUS
        else:
            session.rounds_completed += 1
            if session.rounds_completed >= session.max_rounds:
                session.status = ConsensusStatus.DEADLOCK
            else:
                session.status = ConsensusStatus.DELIBERATION

        return {
            "status": session.status.value,
            "tallies": vote_tallies,
            "winner": winner[0] if session.decision else None,
            "winner_ratio": winner_ratio,
            "threshold_required": threshold,
            "rounds_completed": session.rounds_completed,
            "decision": session.decision,
            "dissent": session.dissent
        }

    def escalate_to_human(self, session_id: str, reason: str) -> Dict[str, Any]:
        """Escalate to human arbitration."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]
        session.status = ConsensusStatus.ESCALATED

        return {
            "session_id": session_id,
            "status": "escalated",
            "reason": reason,
            "context": session.to_dict(),
            "human_action_required": True
        }

    def get_session_status(self, session_id: str) -> Dict[str, Any]:
        """Get current session status."""
        if session_id not in self.sessions:
            raise ValueError(f"Session {session_id} not found")

        session = self.sessions[session_id]
        return session.to_dict()


def main():
    """Demo the consensus engine."""
    engine = ConsensusEngine()

    # Create participants
    participants = [
        Participant("claude-opus", "anthropic", expertise_weight=1.2),
        Participant("gemini-pro", "google", expertise_weight=1.1),
        Participant("gpt-4", "openai", expertise_weight=1.0),
    ]

    print("=== AI Consensus Protocol Demo ===\n")

    # Create session
    session_id = engine.create_session(
        topic="Should we proceed with data analysis approach A or B?",
        category=DecisionCategory.OPERATIONAL,
        participants=participants,
        voting_system=VotingSystem.WEIGHTED
    )
    print(f"Session created: {session_id}")

    # Submit positions
    positions = [
        Position(
            model_id="claude-opus",
            recommendation="Approach A",
            confidence=0.75,
            reasoning="Better accuracy for this data type",
            evidence=["benchmark_results_2026"],
            concerns=["Higher computational cost"]
        ),
        Position(
            model_id="gemini-pro",
            recommendation="Approach B",
            confidence=0.68,
            reasoning="More efficient processing",
            evidence=["efficiency_metrics"],
            concerns=["Slightly lower accuracy"],
            alternatives=["Hybrid A+B"]
        ),
        Position(
            model_id="gpt-4",
            recommendation="Approach A",
            confidence=0.62,
            reasoning="Proven reliability",
            evidence=["historical_performance"]
        )
    ]

    for pos in positions:
        engine.submit_position(session_id, pos)

    # Analyze positions
    analysis = engine.analyze_positions(session_id)
    print(f"\nPosition Analysis:")
    print(f"  Agreement ratio: {analysis['agreement_ratio']:.2f}")
    print(f"  Near consensus: {analysis['near_consensus']}")

    # Submit votes (after deliberation, Gemini changes to hybrid)
    votes = [
        Vote("claude-opus", "Hybrid A+B"),
        Vote("gemini-pro", "Hybrid A+B"),
        Vote("gpt-4", "Hybrid A+B")
    ]

    for vote in votes:
        engine.submit_vote(session_id, vote)

    # Calculate result
    result = engine.calculate_result(session_id)
    print(f"\nVoting Result:")
    print(f"  Status: {result['status']}")
    print(f"  Decision: {result['decision']}")
    print(f"  Winner ratio: {result['winner_ratio']:.2f}")

    # Final status
    status = engine.get_session_status(session_id)
    print(f"\nFinal Session Status: {json.dumps(status, indent=2, default=str)}")


if __name__ == "__main__":
    main()
