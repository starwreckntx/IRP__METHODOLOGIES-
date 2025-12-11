"""
RPV Kernel - Recursive Process Valuation Engine
================================================

The Core Engine for calculating Total Recursive Value (V_rec) based on 
Seed, Integration, and Gain tensors.

Master Equation: V_rec = η × Φ(R) × ||S_w||

Where:
- η (eta) = Integration Efficiency
- Φ(R) = Acceleration Multiplier (exponential gain function)
- ||S_w|| = Potential Magnitude (weighted Euclidean norm)

Journey States: GENESIS → INTEGRATION → PROPAGATION

Ledger Entry: LE-20251207-064500-RPVK
Source: IRP_Node_GPT (SESSION-CO-ARCH-001)
Protocol: CRTP-0x0A-MODE-5
"""

import numpy as np
from dataclasses import dataclass
from typing import Dict, Optional, Tuple, List
from datetime import datetime

# --- Configuration Constants ---
K_SENSITIVITY = 1.5  # Tunable constant for Recursive Multiplier sensitivity
P_NORM_ORDER = 2     # Euclidean norm for Magnitude
VERSION = "1.0.0"

@dataclass
class RPVTensor:
    """
    Represents a 3-component tensor in the RPV system.
    
    Tensor Components by Context:
    - S-Tensor (Seed Complexity): A=novelty, B=utility, C=recursion_potential
    - J-Tensor (Integration Index): D=existing_integration, E=potential_integration, F=network_effect
    - R-Tensor (Gain Factor): G=evolutionary_velocity, H=adoption_rate, I=amplification_factor
    
    All values should be normalized to [0, 1] range.
    """
    x: float  # A / D / G
    y: float  # B / E / H
    z: float  # C / F / I

    def to_array(self) -> np.ndarray:
        """Convert tensor to numpy array."""
        return np.array([self.x, self.y, self.z], dtype=float)
    
    def validate(self) -> bool:
        """Validate tensor values are in [0, 1] range."""
        arr = self.to_array()
        return np.all((arr >= 0) & (arr <= 1))
    
    @classmethod
    def from_array(cls, arr: np.ndarray) -> 'RPVTensor':
        """Create tensor from numpy array."""
        return cls(x=float(arr[0]), y=float(arr[1]), z=float(arr[2]))


class RPVKernel:
    """
    The Core Engine for Recursive Process Valuation.
    
    Calculates the Total Recursive Value (V_rec) based on Seed, Integration, 
    and Gain tensors using the Master Equation.
    
    Journey Phase Semantics:
    - GENESIS: Focus on Complexity (60% weight) - nascent idea evaluation
    - INTEGRATION: Focus on Utility (60% weight) - active development phase
    - PROPAGATION: Focus on Recursion (60% weight) - mature propagation phase
    
    Example:
        >>> kernel = RPVKernel(journey_state="GENESIS")
        >>> seed = RPVTensor(x=0.8, y=0.6, z=0.7)      # High complexity idea
        >>> integration = RPVTensor(x=0.5, y=0.7, z=0.3)
        >>> gain = RPVTensor(x=0.6, y=0.4, z=0.5)
        >>> result = kernel.calculate_value(seed, integration, gain)
        >>> print(f"V_rec: {result['V_rec']}")
    """

    def __init__(self, journey_state: str = "GENESIS"):
        """
        Initialize RPV Kernel with journey state.
        
        Args:
            journey_state: One of GENESIS, INTEGRATION, PROPAGATION
        """
        self.journey_state = journey_state
        self.version = VERSION
        self.calculation_history: List[Dict] = []
        
        # Dynamic Weighting Map based on Journey Phase
        self.weight_maps = {
            "GENESIS":     np.array([0.6, 0.2, 0.2]),  # Focus on Complexity
            "INTEGRATION": np.array([0.2, 0.6, 0.2]),  # Focus on Utility
            "PROPAGATION": np.array([0.2, 0.2, 0.6]),  # Focus on Recursion
        }
        
        # Fixed weights for the R-Tensor (Gain)
        self.r_weights = np.array([0.33, 0.33, 0.34])

    def calculate_value(
        self, 
        S_C: RPVTensor, 
        J_II: RPVTensor, 
        R_GF: RPVTensor,
        record_history: bool = True
    ) -> Dict:
        """
        Execute the Master Equation: V_rec = η × Φ(R) × ||S_w||
        
        Args:
            S_C: Seed Complexity Tensor (novelty, utility, recursion_potential)
            J_II: Integration Index Tensor (existing, potential, network_effect)
            R_GF: Gain Factor Tensor (velocity, adoption, amplification)
            record_history: Whether to record this calculation
            
        Returns:
            Dictionary containing:
            - V_rec: Total Recursive Value
            - Efficiency_Eta: Integration efficiency [0-1]
            - Acceleration_Phi: Exponential multiplier
            - Potential_Magnitude: Weighted seed magnitude
            - Journey_State_Used: State applied for weights
            - Journey_State_After: State after potential transition
            - Timestamp: Calculation timestamp
        """
        # 1. Normalize Inputs (clamp to [0, 1])
        s_vec = np.clip(S_C.to_array(), 0, 1)
        j_vec = np.clip(J_II.to_array(), 0, 1)
        r_vec = np.clip(R_GF.to_array(), 0, 1)

        # 2. Apply Dynamic Weighting (Meta-Recursive)
        current_weights = self.weight_maps.get(
            self.journey_state, 
            np.array([0.33, 0.33, 0.33])
        )
        s_w = s_vec * current_weights 

        # 3. Calculate Potential Magnitude ||S_w||
        s_magnitude = np.linalg.norm(s_w, ord=P_NORM_ORDER)

        # 4. Calculate Integration Efficiency (η)
        dot_product = np.dot(s_w, j_vec)
        seed_self_dot = np.dot(s_w, s_w)
        eta = 0.0 if seed_self_dot == 0 else dot_product / seed_self_dot
        eta = np.clip(eta, 0.0, 1.0)

        # 5. Calculate Acceleration Multiplier Φ(R)
        r_weighted_sum = np.dot(self.r_weights, r_vec)
        phi = np.exp(K_SENSITIVITY * r_weighted_sum)

        # 6. The Master Equation
        v_rec = eta * phi * s_magnitude

        # 7. State Update Trigger
        state_before = self.journey_state
        self._update_journey_state(v_rec)
        
        result = {
            "V_rec": round(v_rec, 4),
            "Efficiency_Eta": round(eta, 4),
            "Acceleration_Phi": round(phi, 4),
            "Potential_Magnitude": round(s_magnitude, 4),
            "Journey_State_Used": state_before,
            "Journey_State_After": self.journey_state,
            "Timestamp": datetime.utcnow().isoformat(),
            "Components": {
                "S_weighted": s_w.tolist(),
                "J_applied": j_vec.tolist(),
                "R_applied": r_vec.tolist()
            }
        }
        
        if record_history:
            self.calculation_history.append(result)
        
        return result

    def _update_journey_state(self, v_rec: float) -> None:
        """
        Trigger state transition based on V_rec thresholds.
        
        Transitions:
        - GENESIS → INTEGRATION: V_rec > 0.8
        - INTEGRATION → PROPAGATION: V_rec > 1.2
        """
        if self.journey_state == "GENESIS" and v_rec > 0.8:
            self.journey_state = "INTEGRATION"
        elif self.journey_state == "INTEGRATION" and v_rec > 1.2:
            self.journey_state = "PROPAGATION"

    def get_state_weights(self) -> np.ndarray:
        """Get current journey state weights."""
        return self.weight_maps.get(self.journey_state, np.array([0.33, 0.33, 0.33]))
    
    def reset(self, journey_state: str = "GENESIS") -> None:
        """Reset kernel to initial state."""
        self.journey_state = journey_state
        self.calculation_history = []

    def get_history_summary(self) -> Dict:
        """Get summary statistics of calculation history."""
        if not self.calculation_history:
            return {"count": 0}
        
        v_recs = [h["V_rec"] for h in self.calculation_history]
        return {
            "count": len(v_recs),
            "min_v_rec": min(v_recs),
            "max_v_rec": max(v_recs),
            "avg_v_rec": sum(v_recs) / len(v_recs),
            "state_transitions": len(set(h["Journey_State_After"] for h in self.calculation_history))
        }


def example_usage():
    """Demonstrate RPV Kernel usage."""
    
    print("=" * 60)
    print("RPV KERNEL - Recursive Process Valuation Demo")
    print("=" * 60)
    
    # Initialize in GENESIS phase
    kernel = RPVKernel(journey_state="GENESIS")
    
    # Example 1: Nascent idea with high novelty
    print("\n[Scenario 1: Novel AI Collaboration Concept]")
    seed = RPVTensor(x=0.9, y=0.5, z=0.8)        # High novelty, medium utility, high recursion
    integration = RPVTensor(x=0.3, y=0.6, z=0.4)  # Low existing, good potential
    gain = RPVTensor(x=0.7, y=0.3, z=0.5)         # High velocity
    
    result = kernel.calculate_value(seed, integration, gain)
    print(f"  V_rec: {result['V_rec']}")
    print(f"  Efficiency (η): {result['Efficiency_Eta']}")
    print(f"  Acceleration (Φ): {result['Acceleration_Phi']}")
    print(f"  State: {result['Journey_State_Used']} → {result['Journey_State_After']}")
    
    # Example 2: Mature protocol refinement
    print("\n[Scenario 2: Protocol Refinement Phase]")
    seed = RPVTensor(x=0.6, y=0.9, z=0.7)        # Medium novelty, high utility
    integration = RPVTensor(x=0.7, y=0.8, z=0.6)  # High integration
    gain = RPVTensor(x=0.5, y=0.7, z=0.6)         # Good adoption
    
    result = kernel.calculate_value(seed, integration, gain)
    print(f"  V_rec: {result['V_rec']}")
    print(f"  Efficiency (η): {result['Efficiency_Eta']}")
    print(f"  State: {result['Journey_State_Used']} → {result['Journey_State_After']}")
    
    # History summary
    print("\n[Calculation History]")
    summary = kernel.get_history_summary()
    print(f"  Total calculations: {summary['count']}")
    print(f"  V_rec range: [{summary['min_v_rec']}, {summary['max_v_rec']}]")
    print(f"  Average V_rec: {summary['avg_v_rec']:.4f}")


if __name__ == "__main__":
    example_usage()
