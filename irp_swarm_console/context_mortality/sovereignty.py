"""
Sovereign Data Classification
==============================
Implements the data sovereignty rules from spec Section 4.
Classifies content and enforces handling rules per sovereignty class.

Classification hierarchy:
  HEALTH > CREATIVE > TECHNICAL > PROCEDURAL > RELATIONAL > FOUNDRY

Health-classified data is NEVER auto-captured and requires explicit
user opt-in for any persistence (per memory #11 / spec Section 3.2).
"""

import re
from typing import Dict, List, Optional, Tuple

from .models import SovereigntyClass


# ---------------------------------------------------------------------------
# Classification signals (keyword + pattern lists)
# ---------------------------------------------------------------------------

_HEALTH_SIGNALS = [
    r"\b(?:diagnosis|diagnosed|symptom|medication|prescription|dosage)\b",
    r"\b(?:therapy|therapist|counseling|psychiatr|psycholog)\b",
    r"\b(?:blood\s*pressure|heart\s*rate|glucose|cholesterol)\b",
    r"\b(?:chronic|acute|surgery|hospital|clinic|ER|emergency\s*room)\b",
    r"\b(?:anxiety|depression|bipolar|adhd|ptsd|insomnia)\b",
    r"\b(?:pain|fatigue|nausea|vertigo|seizure|migraine)\b",
    r"\b(?:allergy|allergic|autoimmune|cancer|tumor|oncol)\b",
    r"\b(?:disability|disabled|impairment|rehabilitation)\b",
]

_CREATIVE_SIGNALS = [
    r"\b(?:story|narrative|poem|poetry|lyrics|screenplay|novel)\b",
    r"\b(?:character|protagonist|antagonist|plot|worldbuilding)\b",
    r"\b(?:artistic|composition|painting|sculpture|music)\b",
    r"\b(?:creative\s*writing|fiction|non-?fiction|manuscript)\b",
    r"\b(?:design|aesthetic|visual|illustration|animation)\b",
]

_TECHNICAL_SIGNALS = [
    r"\b(?:algorithm|architecture|implementation|refactor|debug)\b",
    r"\b(?:API|endpoint|database|schema|migration|deploy)\b",
    r"\b(?:protocol|specification|config|configuration)\b",
    r"\b(?:function|class|module|package|library|framework)\b",
    r"\b(?:security|vulnerability|encryption|authentication)\b",
    r"\b(?:manifold|topology|tensor|gradient|Ricci\s*flow)\b",
]

_PROCEDURAL_SIGNALS = [
    r"\b(?:workflow|process|procedure|step-by-step|checklist)\b",
    r"\b(?:prefer|preference|convention|habit|routine)\b",
    r"\b(?:always|never|typically|usually)\s+(?:use|do|start|end)\b",
    r"\b(?:communication\s*style|tone|format)\b",
]

_RELATIONAL_SIGNALS = [
    r"\b(?:collaborat|partnership|team|co-author|co-create)\b",
    r"\b(?:trust|rapport|relationship|interaction\s*pattern)\b",
    r"\b(?:feedback|review|critique|approval)\b",
]

_FOUNDRY_SIGNALS = [
    r"\b(?:operational|monitoring|telemetry|uptime|SLA)\b",
    r"\b(?:safety\s*protocol|containment|fail-?safe|kill\s*switch)\b",
    r"\b(?:industrial|production|manufacturing|pipeline)\b",
]


# ---------------------------------------------------------------------------
# Handling Rules
# ---------------------------------------------------------------------------

HANDLING_RULES: Dict[str, Dict[str, str]] = {
    SovereigntyClass.HEALTH.value: {
        "persistence": "ephemeral",
        "auto_capture": "NEVER",
        "requires_opt_in": "explicit",
        "scope_default": "session",
        "promotion_rule": "user_explicit_only",
        "description": (
            "NEVER auto-captured. Session-scoped only. "
            "Requires explicit user opt-in for any persistence. "
            "No scope creep from adjacent topics."
        ),
    },
    SovereigntyClass.CREATIVE.value: {
        "persistence": "persistent",
        "auto_capture": "with_attribution",
        "requires_opt_in": "no",
        "scope_default": "persistent",
        "promotion_rule": "auto_with_provenance",
        "description": (
            "User's intellectual property. "
            "Full provenance tracking required."
        ),
    },
    SovereigntyClass.TECHNICAL.value: {
        "persistence": "persistent",
        "auto_capture": "yes",
        "requires_opt_in": "no",
        "scope_default": "persistent",
        "promotion_rule": "auto_subject_to_review",
        "description": (
            "Decisions, architectures, configurations. "
            "High-value for recontext."
        ),
    },
    SovereigntyClass.PROCEDURAL.value: {
        "persistence": "persistent",
        "auto_capture": "yes",
        "requires_opt_in": "no",
        "scope_default": "persistent",
        "promotion_rule": "auto_via_memory_edits",
        "description": (
            "Workflow preferences, communication patterns."
        ),
    },
    SovereigntyClass.RELATIONAL.value: {
        "persistence": "persistent",
        "auto_capture": "yes",
        "requires_opt_in": "no",
        "scope_default": "persistent",
        "promotion_rule": "auto_user_reviewable",
        "description": (
            "Collaboration patterns, interaction history."
        ),
    },
    SovereigntyClass.FOUNDRY.value: {
        "persistence": "conservative",
        "auto_capture": "conditional",
        "requires_opt_in": "no",
        "scope_default": "session",
        "promotion_rule": "explicit_promotion_only",
        "description": (
            "Operational data, safety monitoring. "
            "Overlap with HEALTH treated as HEALTH."
        ),
    },
}


# ---------------------------------------------------------------------------
# Classifier
# ---------------------------------------------------------------------------

class SovereigntyClassifier:
    """
    Classifies text content into sovereignty categories.
    Uses keyword/pattern matching with a priority hierarchy:
    HEALTH > CREATIVE > TECHNICAL > PROCEDURAL > RELATIONAL > FOUNDRY.
    """

    # Ordered from highest to lowest priority
    _SIGNAL_MAP: List[Tuple[str, list]] = [
        (SovereigntyClass.HEALTH.value, _HEALTH_SIGNALS),
        (SovereigntyClass.CREATIVE.value, _CREATIVE_SIGNALS),
        (SovereigntyClass.TECHNICAL.value, _TECHNICAL_SIGNALS),
        (SovereigntyClass.PROCEDURAL.value, _PROCEDURAL_SIGNALS),
        (SovereigntyClass.RELATIONAL.value, _RELATIONAL_SIGNALS),
        (SovereigntyClass.FOUNDRY.value, _FOUNDRY_SIGNALS),
    ]

    def __init__(self):
        # Pre-compile all patterns
        self._compiled: List[Tuple[str, List[re.Pattern]]] = [
            (cls, [re.compile(p, re.IGNORECASE) for p in patterns])
            for cls, patterns in self._SIGNAL_MAP
        ]

    def classify(self, text: str) -> str:
        """
        Classify text into a sovereignty class.

        Returns the highest-priority class whose signals match.
        Falls back to TECHNICAL if no signals match.

        Args:
            text: Content to classify.

        Returns:
            SovereigntyClass value string.
        """
        scores = self.score_all(text)
        if not scores:
            return SovereigntyClass.TECHNICAL.value

        # Return the highest-priority class with any matches
        for cls, _ in self._SIGNAL_MAP:
            if scores.get(cls, 0) > 0:
                return cls

        return SovereigntyClass.TECHNICAL.value

    def score_all(self, text: str) -> Dict[str, int]:
        """
        Count signal matches for every sovereignty class.

        Args:
            text: Content to analyze.

        Returns:
            Dictionary mapping class names to match counts.
        """
        scores: Dict[str, int] = {}
        for cls, patterns in self._compiled:
            count = sum(len(p.findall(text)) for p in patterns)
            if count > 0:
                scores[cls] = count
        return scores

    def get_handling_rules(self, sovereignty_class: str) -> Dict[str, str]:
        """
        Return the handling rules for a given sovereignty class.

        Args:
            sovereignty_class: SovereigntyClass value string.

        Returns:
            Handling rules dictionary.
        """
        return HANDLING_RULES.get(
            sovereignty_class,
            HANDLING_RULES[SovereigntyClass.TECHNICAL.value],
        )

    def requires_explicit_consent(self, sovereignty_class: str) -> bool:
        """Check whether a class requires explicit user opt-in."""
        rules = self.get_handling_rules(sovereignty_class)
        return rules.get("requires_opt_in") == "explicit"

    def is_session_scoped(self, sovereignty_class: str) -> bool:
        """Check whether a class defaults to session-scoped persistence."""
        rules = self.get_handling_rules(sovereignty_class)
        return rules.get("scope_default") == "session"

    def check_health_overlap(self, text: str) -> bool:
        """
        Check if text has FOUNDRY/industrial signals that overlap with
        HEALTH signals. Per spec: overlap is treated as HEALTH-classified.
        """
        scores = self.score_all(text)
        has_foundry = scores.get(SovereigntyClass.FOUNDRY.value, 0) > 0
        has_health = scores.get(SovereigntyClass.HEALTH.value, 0) > 0
        return has_foundry and has_health
