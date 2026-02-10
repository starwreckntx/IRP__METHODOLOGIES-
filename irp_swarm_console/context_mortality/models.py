"""
Context Mortality Audit - Shared Data Models
=============================================
Core dataclasses and enums used across all CMA components.
Implements the semantic unit, transformation chain, and provenance
data structures described in the Context Mortality Audit specification.
"""

import hashlib
import json
import uuid
from dataclasses import dataclass, field, asdict
from datetime import datetime
from enum import Enum
from typing import Any, Dict, List, Optional


# ---------------------------------------------------------------------------
# Enumerations
# ---------------------------------------------------------------------------

class SovereigntyClass(str, Enum):
    """Sovereign data classification per spec Section 4."""
    HEALTH = "HEALTH"
    CREATIVE = "CREATIVE"
    TECHNICAL = "TECHNICAL"
    PROCEDURAL = "PROCEDURAL"
    RELATIONAL = "RELATIONAL"
    FOUNDRY = "FOUNDRY"


class ItemStatus(str, Enum):
    """Lifecycle status of a context item."""
    ALIVE = "ALIVE"
    COMPRESSED = "COMPRESSED"
    DEAD = "DEAD"
    RECOVERED = "RECOVERED"


class AppealStatus(str, Enum):
    """Appeal status for dropped items."""
    NOT_REVIEWED = "not_reviewed"
    PENDING = "pending"
    ACCEPTED_DROP = "reviewed-accepted"
    APPEALED = "appealed"
    REINSTATED = "reinstated"
    ESCALATED = "escalated"


class AppealCategory(str, Enum):
    """Categories for appeal reinstatement routing."""
    FACTUAL = "factual"
    PROCEDURAL = "procedural"
    CREATIVE = "creative"
    HEALTH = "health"
    RELATIONAL = "relational"


class ReinstatementTarget(str, Enum):
    """Where reinstated context should be placed."""
    MEMORY_EDIT = "memory_user_edits"
    SESSION_INJECTION = "session_injection"
    CLAUDE_MD = "claude_md"


class TransformationType(str, Enum):
    """Types of context transformation events."""
    COMPACTION = "compaction"
    MEMORY_SYNTHESIS = "memory_synthesis"
    MEMORY_RESYNTHESIS = "memory_resynthesis"
    USER_EDIT = "user_edit"
    RECONTEXT_RECOVERY = "recontext_recovery"


class SweepTrigger(str, Enum):
    """What triggered a recontext sweep."""
    SCHEDULED = "scheduled"
    EVENT_DRIVEN = "event_driven"
    MANUAL = "manual"
    THRESHOLD = "threshold"


class GapType(str, Enum):
    """Classification of gaps found during recontext sweeps."""
    PREVIOUSLY_DROPPED = "previously_dropped"
    NEVER_CAPTURED = "never_captured"
    DEGRADED = "degraded"
    NEWLY_RELEVANT = "newly_relevant"


# ---------------------------------------------------------------------------
# Core Data Models
# ---------------------------------------------------------------------------

@dataclass
class SemanticUnit:
    """
    A discrete unit of meaning extracted from conversation context.
    The atomic unit that CDA tracks through its lifecycle.
    """
    content: str
    turn_index: int
    timestamp: str
    session_id: str
    content_hash: str = ""
    sovereignty_class: str = SovereigntyClass.TECHNICAL.value
    unit_id: str = ""

    def __post_init__(self):
        if not self.unit_id:
            self.unit_id = str(uuid.uuid4())
        if not self.content_hash:
            self.content_hash = hashlib.sha256(
                self.content.encode("utf-8")
            ).hexdigest()

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "SemanticUnit":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})

    def __hash__(self):
        return hash(self.content_hash)

    def __eq__(self, other):
        if isinstance(other, SemanticUnit):
            return self.content_hash == other.content_hash
        return NotImplemented


@dataclass
class DroppedItem:
    """A context item that was evaluated and discarded during compaction."""
    id: str
    content: str
    source_turn: int
    source_timestamp: str
    session_id: str
    category: str = SovereigntyClass.TECHNICAL.value
    estimated_importance: Optional[float] = None
    reason_code: Optional[str] = None
    recovery_path: str = ""
    appeal_status: str = AppealStatus.PENDING.value
    content_hash: str = ""

    def __post_init__(self):
        if not self.content_hash:
            self.content_hash = hashlib.sha256(
                self.content.encode("utf-8")
            ).hexdigest()
        if not self.recovery_path:
            self.recovery_path = (
                f"transcript://{self.session_id}/turn/{self.source_turn}"
            )

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DroppedItem":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ContextSnapshot:
    """Snapshot of the context window state at a point in time."""
    timestamp: str
    token_count: int
    turn_count: int
    content_hash: str
    items: List[Dict[str, Any]] = field(default_factory=list)
    snapshot_id: str = ""

    def __post_init__(self):
        if not self.snapshot_id:
            self.snapshot_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextSnapshot":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class Transformation:
    """A single transformation event in a context item's lifecycle."""
    event: str
    timestamp: str
    survived: bool
    transformed_form: Optional[str] = None
    fidelity_score: float = 0.0
    reason: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Transformation":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class ContextPathTrace:
    """
    Full lifecycle trace for a single piece of information.
    Tracks from origin through every transformation to current state.
    """
    origin_session_id: str
    origin_turn_index: int
    origin_timestamp: str
    origin_verbatim: str
    origin_content_hash: str = ""
    transformations: List[Dict[str, Any]] = field(default_factory=list)
    current_status: str = ItemStatus.ALIVE.value
    last_seen_in: Optional[str] = None
    recoverable: bool = True
    recovery_path: str = ""
    appeal_status: str = AppealStatus.NOT_REVIEWED.value
    trace_id: str = ""

    def __post_init__(self):
        if not self.trace_id:
            self.trace_id = str(uuid.uuid4())
        if not self.origin_content_hash:
            self.origin_content_hash = hashlib.sha256(
                self.origin_verbatim.encode("utf-8")
            ).hexdigest()

    def add_transformation(self, transformation: Transformation) -> None:
        self.transformations.append(transformation.to_dict())
        if not transformation.survived:
            self.current_status = ItemStatus.DEAD.value

    def get_fidelity_curve(self) -> List[float]:
        """Return the sequence of fidelity scores across transformations."""
        return [t.get("fidelity_score", 0.0) for t in self.transformations]

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "ContextPathTrace":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class RecoveryProposal:
    """A proposed recovery of lost context from a recontext sweep."""
    original_verbatim: str
    proposed_memory_form: str
    fidelity_score: float
    relevance_score: float
    gap_type: str
    source_session_id: str
    source_turn: int
    sovereignty_class: str = SovereigntyClass.TECHNICAL.value
    proposal_id: str = ""
    status: str = "proposed"

    def __post_init__(self):
        if not self.proposal_id:
            self.proposal_id = str(uuid.uuid4())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "RecoveryProposal":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class BiasVector:
    """Describes a compression bias detected via drift analysis."""
    item_content: str
    item_hash: str
    retained_in: str  # "A" or "B"
    dropped_from: str  # "B" or "A"
    hypothesized_cause: str
    confidence: float = 0.0

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BiasVector":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class DriftReport:
    """Comprehensive report on systematic compression bias."""
    drift_coefficient: float
    convergent_count: int
    divergent_count: int
    doubly_dead_count: int
    bias_vectors: List[Dict[str, Any]] = field(default_factory=list)
    recommendations: List[str] = field(default_factory=list)
    report_id: str = ""
    timestamp: str = ""
    account_a_id: str = ""
    account_b_id: str = ""

    def __post_init__(self):
        if not self.report_id:
            self.report_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DriftReport":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})


@dataclass
class CDALog:
    """
    Complete Context Death Audit log for a single compaction event.
    Contains pre/post snapshots and the full list of dropped items.
    """
    session_id: str
    user_id: str
    pre_snapshot: Dict[str, Any] = field(default_factory=dict)
    post_snapshot: Dict[str, Any] = field(default_factory=dict)
    dropped_items: List[Dict[str, Any]] = field(default_factory=list)
    retained_items: List[Dict[str, Any]] = field(default_factory=list)
    compression_ratio: float = 0.0
    log_id: str = ""
    timestamp: str = ""

    def __post_init__(self):
        if not self.log_id:
            self.log_id = str(uuid.uuid4())
        if not self.timestamp:
            self.timestamp = datetime.utcnow().isoformat() + "Z"

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "CDALog":
        return cls(**{k: v for k, v in data.items() if k in cls.__dataclass_fields__})
