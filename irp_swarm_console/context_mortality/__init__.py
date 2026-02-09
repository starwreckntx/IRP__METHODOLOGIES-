"""
Context Mortality Audit (CMA)
=============================
Long-horizon memory governance framework for auditing, tracking,
and recovering context lost during compaction and synthesis.

Implements the Context Mortality Audit & Recontext Architecture
specification (v1.0, February 2026).

Components:
    - CDA (Context Death Audit)     — Phase 1: compaction diff logging
    - PathTracer                    — Phase 2: lifecycle tracing with fidelity
    - RecontextSweep                — Phase 3: transcript recovery scanning
    - AppealManager                 — Phase 4: reinstatement workflow
    - DriftTrajectoryAnalysis       — Phase 5: parallel-account bias detection
    - SovereigntyClassifier         — Data sovereignty classification
"""

from .models import (
    AppealCategory,
    AppealStatus,
    BiasVector,
    CDALog,
    ContextPathTrace,
    ContextSnapshot,
    DroppedItem,
    DriftReport,
    GapType,
    ItemStatus,
    RecoveryProposal,
    ReinstatementTarget,
    SemanticUnit,
    SovereigntyClass,
    SweepTrigger,
    Transformation,
    TransformationType,
)
from .sovereignty import SovereigntyClassifier, HANDLING_RULES
from .cda import ContextDeathAudit
from .path_tracer import PathTracer, FidelityScorer
from .recontext import RecontextSweep, SweepScope
from .appeal import AppealManager
from .drift import DriftTrajectoryAnalysis, DriftTracker, MemoryState

__version__ = "1.0.0"
__spec_version__ = "1.0"
__author__ = "Joseph (Pack3t C0nc3pts / StarwreckNTX)"

__all__ = [
    # Phase 1
    "ContextDeathAudit",
    "CDALog",
    "ContextSnapshot",
    "DroppedItem",
    "SemanticUnit",
    # Phase 2
    "PathTracer",
    "FidelityScorer",
    "ContextPathTrace",
    "Transformation",
    "TransformationType",
    # Phase 3
    "RecontextSweep",
    "SweepScope",
    "RecoveryProposal",
    "GapType",
    "SweepTrigger",
    # Phase 4
    "AppealManager",
    "AppealCategory",
    "AppealStatus",
    "ReinstatementTarget",
    # Phase 5
    "DriftTrajectoryAnalysis",
    "DriftTracker",
    "MemoryState",
    "DriftReport",
    "BiasVector",
    # Sovereignty
    "SovereigntyClassifier",
    "SovereigntyClass",
    "HANDLING_RULES",
    # Common
    "ItemStatus",
]
