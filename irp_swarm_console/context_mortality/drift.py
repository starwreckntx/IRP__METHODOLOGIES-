"""
Drift Trajectory Analysis (DTA) — Phase 5
==========================================
Detects systematic bias in compression/synthesis by comparing memory
states across parallel accounts with identical (or near-identical)
conversation histories.

Produces drift coefficients (Jaccard distance), identifies bias vectors,
and tracks longitudinal drift trajectories over time.

This is the research-grade component described in spec Section 3.5.
"""

import hashlib
import json
import uuid
from collections import Counter
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

from .models import BiasVector, DriftReport


class MemoryState:
    """
    Snapshot of an account's memory state at a point in time.

    Each item is a string representing a memory entry.  Items are
    compared by their content hash for deterministic diffing.
    """

    def __init__(
        self,
        account_id: str,
        items: List[str],
        snapshot_timestamp: Optional[str] = None,
    ):
        self.account_id = account_id
        self.snapshot_timestamp = (
            snapshot_timestamp or datetime.utcnow().isoformat() + "Z"
        )
        self.items = items
        self.item_hashes: Dict[str, str] = {}  # hash -> content
        for item in items:
            h = hashlib.sha256(item.strip().encode("utf-8")).hexdigest()
            self.item_hashes[h] = item.strip()

    def get_hash_set(self) -> Set[str]:
        return set(self.item_hashes.keys())

    def get_content(self, item_hash: str) -> Optional[str]:
        return self.item_hashes.get(item_hash)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "account_id": self.account_id,
            "snapshot_timestamp": self.snapshot_timestamp,
            "item_count": len(self.items),
            "items": self.items,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "MemoryState":
        return cls(
            account_id=data["account_id"],
            items=data["items"],
            snapshot_timestamp=data.get("snapshot_timestamp"),
        )


class DriftTrajectoryAnalysis:
    """
    Compares two parallel memory states to detect compression bias.

    Produces:
      - Drift coefficient (Jaccard distance, 0.0 = identical, 1.0 = fully divergent)
      - Convergent items (both retained)
      - Divergent items (one retained, one dropped)
      - Doubly-dead items (both dropped, relative to a reference set)
      - Bias vectors (hypothesized causes for each divergent item)
    """

    # Possible bias causes
    BIAS_CAUSES = [
        "recency_weighting",
        "token_budget_race",
        "semantic_clustering",
        "stochastic_variance",
        "category_bias",
    ]

    def __init__(
        self,
        account_a: MemoryState,
        account_b: MemoryState,
        reference_items: Optional[List[str]] = None,
    ):
        """
        Args:
            account_a: Memory state from account A.
            account_b: Memory state from account B.
            reference_items: Optional "ground truth" list of all items
                             that should exist.  Used to compute
                             doubly-dead items.
        """
        self.a = account_a
        self.b = account_b

        self.reference_hashes: Optional[Set[str]] = None
        if reference_items:
            self.reference_hashes = set(
                hashlib.sha256(item.strip().encode("utf-8")).hexdigest()
                for item in reference_items
            )

    # ------------------------------------------------------------------
    # Core metrics
    # ------------------------------------------------------------------

    def compute_drift_coefficient(self) -> float:
        """
        Jaccard distance between the two memory states.

        0.0 = identical memories (no drift)
        1.0 = completely divergent (maximum drift)
        """
        a_hashes = self.a.get_hash_set()
        b_hashes = self.b.get_hash_set()
        union = a_hashes | b_hashes
        if not union:
            return 0.0
        intersection = a_hashes & b_hashes
        return 1.0 - (len(intersection) / len(union))

    def get_convergent(self) -> List[str]:
        """Items retained in both accounts."""
        intersection = self.a.get_hash_set() & self.b.get_hash_set()
        return [self.a.get_content(h) for h in intersection if self.a.get_content(h)]

    def get_divergent(self) -> List[Dict[str, Any]]:
        """Items retained in one account but not the other."""
        a_hashes = self.a.get_hash_set()
        b_hashes = self.b.get_hash_set()
        symmetric_diff = a_hashes ^ b_hashes

        divergent = []
        for h in symmetric_diff:
            if h in a_hashes:
                content = self.a.get_content(h)
                retained_in = self.a.account_id
                dropped_from = self.b.account_id
            else:
                content = self.b.get_content(h)
                retained_in = self.b.account_id
                dropped_from = self.a.account_id

            divergent.append({
                "content": content,
                "content_hash": h,
                "retained_in": retained_in,
                "dropped_from": dropped_from,
            })

        return divergent

    def get_doubly_dead(self) -> List[str]:
        """
        Items present in the reference set but absent from BOTH accounts.
        Indicates systematic deprioritization.

        Returns empty list if no reference set was provided.
        """
        if self.reference_hashes is None:
            return []

        surviving = self.a.get_hash_set() | self.b.get_hash_set()
        dead_hashes = self.reference_hashes - surviving

        # We can't recover content from dead hashes without the reference
        # items.  Return the hashes themselves.
        return sorted(dead_hashes)

    # ------------------------------------------------------------------
    # Bias vector analysis
    # ------------------------------------------------------------------

    def identify_bias_vectors(self) -> List[BiasVector]:
        """
        For each divergent item, hypothesize the cause of divergence.

        Uses heuristics based on content characteristics to assign a
        likely bias cause.
        """
        divergent = self.get_divergent()
        vectors = []

        for item in divergent:
            content = item.get("content", "")
            cause = self._infer_cause(content)
            confidence = self._estimate_confidence(content, cause)

            vectors.append(
                BiasVector(
                    item_content=content or "",
                    item_hash=item["content_hash"],
                    retained_in=item["retained_in"],
                    dropped_from=item["dropped_from"],
                    hypothesized_cause=cause,
                    confidence=confidence,
                )
            )

        return vectors

    def _infer_cause(self, content: str) -> str:
        """
        Heuristic inference of bias cause based on content.

        This is deliberately simple — accurate causal attribution would
        require access to the compression algorithm internals.
        """
        if not content:
            return "stochastic_variance"

        content_lower = content.lower()
        word_count = len(content.split())

        # Very short items may be lost to token budget races
        if word_count < 10:
            return "token_budget_race"

        # Technical jargon may cluster differently
        technical_markers = [
            "function", "class", "api", "endpoint", "config",
            "algorithm", "architecture", "protocol", "schema",
        ]
        if any(marker in content_lower for marker in technical_markers):
            return "semantic_clustering"

        # Personal/relational content may have category bias
        personal_markers = [
            "prefer", "always", "never", "feel", "think",
            "collaborate", "relationship", "trust",
        ]
        if any(marker in content_lower for marker in personal_markers):
            return "category_bias"

        # Long items in the middle of conversations may suffer recency bias
        if word_count > 50:
            return "recency_weighting"

        return "stochastic_variance"

    @staticmethod
    def _estimate_confidence(content: str, cause: str) -> float:
        """
        Estimate confidence in the inferred cause.
        Returns 0.0 to 1.0.
        """
        # Base confidence is low — we're guessing at internal mechanisms
        base = 0.3

        if cause == "stochastic_variance":
            return base  # Can't be confident about randomness

        if cause == "token_budget_race":
            # Higher confidence for very short items
            if len(content.split()) < 5:
                return 0.6
            return 0.4

        if cause in ("semantic_clustering", "category_bias"):
            return 0.5  # Moderate confidence from keyword matching

        if cause == "recency_weighting":
            return 0.45

        return base

    # ------------------------------------------------------------------
    # Report generation
    # ------------------------------------------------------------------

    def generate_drift_report(self) -> DriftReport:
        """Generate a comprehensive drift analysis report."""
        convergent = self.get_convergent()
        divergent = self.get_divergent()
        doubly_dead = self.get_doubly_dead()
        bias_vectors = self.identify_bias_vectors()

        recommendations = self._generate_recommendations(
            len(convergent), len(divergent), len(doubly_dead), bias_vectors
        )

        return DriftReport(
            drift_coefficient=round(self.compute_drift_coefficient(), 4),
            convergent_count=len(convergent),
            divergent_count=len(divergent),
            doubly_dead_count=len(doubly_dead),
            bias_vectors=[bv.to_dict() for bv in bias_vectors],
            recommendations=recommendations,
            account_a_id=self.a.account_id,
            account_b_id=self.b.account_id,
        )

    @staticmethod
    def _generate_recommendations(
        convergent_count: int,
        divergent_count: int,
        doubly_dead_count: int,
        bias_vectors: List[BiasVector],
    ) -> List[str]:
        """Generate human-readable recommendations from analysis."""
        recs = []

        total = convergent_count + divergent_count
        if total == 0:
            return ["No items to analyze. Ensure both accounts have memory content."]

        drift_pct = (divergent_count / total) * 100 if total > 0 else 0

        if drift_pct > 50:
            recs.append(
                f"CRITICAL: {drift_pct:.0f}% divergence detected. "
                "Compression is highly non-deterministic for this content."
            )
        elif drift_pct > 20:
            recs.append(
                f"WARNING: {drift_pct:.0f}% divergence detected. "
                "Consider increasing memory protection for important items."
            )
        else:
            recs.append(
                f"Drift is within acceptable range ({drift_pct:.0f}%). "
                "Compression is relatively stable."
            )

        if doubly_dead_count > 0:
            recs.append(
                f"{doubly_dead_count} items were dropped by BOTH accounts, "
                "indicating systematic deprioritization. "
                "Review these items for recontext recovery."
            )

        # Analyze bias cause distribution
        if bias_vectors:
            cause_counts = Counter(bv.hypothesized_cause for bv in bias_vectors)
            dominant_cause = cause_counts.most_common(1)[0]
            recs.append(
                f"Most common bias pattern: {dominant_cause[0]} "
                f"({dominant_cause[1]} items). "
                "Consider targeted protection for affected content types."
            )

        return recs


class DriftTracker:
    """
    Longitudinal drift tracking across multiple snapshots over time.
    Stores a time-series of drift coefficients for trend analysis.
    """

    def __init__(self, store_path: Optional[str] = None):
        if store_path is None:
            store_path = str(Path(__file__).parent / "drift_trajectory.jsonl")
        self.store_path = Path(store_path)
        self.trajectory: List[Dict[str, Any]] = []
        self._load()

    def _load(self) -> None:
        if not self.store_path.exists():
            return
        with open(self.store_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                try:
                    self.trajectory.append(json.loads(line))
                except json.JSONDecodeError:
                    continue

    def _append(self, entry: Dict[str, Any]) -> None:
        with open(self.store_path, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

    def record_snapshot(self, report: DriftReport) -> Dict[str, Any]:
        """
        Record a drift report as a point in the longitudinal trajectory.

        Args:
            report: DriftReport from a DriftTrajectoryAnalysis.

        Returns:
            The trajectory entry.
        """
        entry = {
            "timestamp": report.timestamp,
            "report_id": report.report_id,
            "drift_coefficient": report.drift_coefficient,
            "convergent_count": report.convergent_count,
            "divergent_count": report.divergent_count,
            "doubly_dead_count": report.doubly_dead_count,
            "account_a": report.account_a_id,
            "account_b": report.account_b_id,
        }
        self.trajectory.append(entry)
        self._append(entry)
        return entry

    def get_trajectory(self) -> List[Dict[str, Any]]:
        """Return the full time-series of drift snapshots."""
        return list(self.trajectory)

    def get_trend(self) -> Dict[str, Any]:
        """
        Analyze the drift trajectory for trends.

        Returns:
            Trend analysis with direction, volatility, and summary.
        """
        if len(self.trajectory) < 2:
            return {
                "status": "insufficient_data",
                "message": "Need at least 2 snapshots for trend analysis.",
                "data_points": len(self.trajectory),
            }

        coefficients = [t["drift_coefficient"] for t in self.trajectory]

        # Simple linear trend (positive = diverging, negative = converging)
        n = len(coefficients)
        x_mean = (n - 1) / 2
        y_mean = sum(coefficients) / n
        numerator = sum(
            (i - x_mean) * (c - y_mean) for i, c in enumerate(coefficients)
        )
        denominator = sum((i - x_mean) ** 2 for i in range(n))
        slope = numerator / denominator if denominator != 0 else 0.0

        # Volatility (standard deviation of drift coefficients)
        variance = sum((c - y_mean) ** 2 for c in coefficients) / n
        volatility = variance ** 0.5

        if slope > 0.01:
            direction = "DIVERGING"
        elif slope < -0.01:
            direction = "CONVERGING"
        else:
            direction = "STABLE"

        return {
            "status": "analyzed",
            "data_points": n,
            "direction": direction,
            "slope": round(slope, 6),
            "mean_drift": round(y_mean, 4),
            "volatility": round(volatility, 4),
            "latest_coefficient": coefficients[-1],
            "first_coefficient": coefficients[0],
            "summary": (
                f"Over {n} snapshots, drift is {direction.lower()} "
                f"(slope={slope:.4f}, volatility={volatility:.4f}). "
                f"Mean drift coefficient: {y_mean:.4f}."
            ),
        }

    def get_stats(self) -> Dict[str, Any]:
        """Return summary statistics about the trajectory store."""
        return {
            "data_points": len(self.trajectory),
            "store_path": str(self.store_path),
            "trend": self.get_trend(),
        }
