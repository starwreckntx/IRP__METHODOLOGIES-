# RPV Kernel - Recursive Process Valuation

**Skill ID:** `rpv-kernel`  
**Version:** 1.0.0  
**Category:** metrics  
**Ledger Entry:** `LE-20251207-064500-RPVK`

## Overview

The RPV Kernel implements the **Recursive Process Valuation** system for quantifying the value of ideas, artifacts, and processes within the IRP ecosystem. It embodies the principle: *"The Journey Is The Artifact"* - measuring not just static outcomes but evolutionary potential.

## Master Equation

```
V_rec = η × Φ(R) × ||S_w||
```

Where:
- **η (eta)** = Integration Efficiency [0-1]
- **Φ(R)** = Acceleration Multiplier (exponential)
- **||S_w||** = Potential Magnitude (weighted Euclidean norm)

## Tensor Architecture

### S-Tensor (Seed Complexity)
| Component | Symbol | Description |
|-----------|--------|-------------|
| x | A | Novelty - uniqueness of the concept |
| y | B | Utility - practical applicability |
| z | C | Recursion Potential - self-referential value generation |

### J-Tensor (Integration Index)
| Component | Symbol | Description |
|-----------|--------|-------------|
| x | D | Existing Integration - current ecosystem fit |
| y | E | Potential Integration - future connection capacity |
| z | F | Network Effect - multiplicative community value |

### R-Tensor (Gain Factor)
| Component | Symbol | Description |
|-----------|--------|-------------|
| x | G | Evolutionary Velocity - rate of refinement |
| y | H | Adoption Rate - uptake speed |
| z | I | Amplification Factor - propagation multiplier |

## Journey States

Dynamic weighting shifts based on lifecycle phase:

| State | Focus | Weights (A, B, C) |
|-------|-------|-------------------|
| **GENESIS** | Complexity | [0.6, 0.2, 0.2] |
| **INTEGRATION** | Utility | [0.2, 0.6, 0.2] |
| **PROPAGATION** | Recursion | [0.2, 0.2, 0.6] |

### State Transitions
- GENESIS → INTEGRATION: `V_rec > 0.8`
- INTEGRATION → PROPAGATION: `V_rec > 1.2`

## Usage

### Python API

```python
from rpv_kernel import RPVKernel, RPVTensor

# Initialize kernel
kernel = RPVKernel(journey_state="GENESIS")

# Define tensors
seed = RPVTensor(x=0.8, y=0.6, z=0.7)        # Novel idea
integration = RPVTensor(x=0.5, y=0.7, z=0.3)  # Moderate integration
gain = RPVTensor(x=0.6, y=0.4, z=0.5)         # Good velocity

# Calculate value
result = kernel.calculate_value(seed, integration, gain)

print(f"V_rec: {result['V_rec']}")
print(f"Efficiency: {result['Efficiency_Eta']}")
print(f"State: {result['Journey_State_After']}")
```

### CLI Interface

```bash
# Basic calculation
python rpv_kernel.py

# With custom values (future feature)
python rpv_kernel.py --seed 0.8,0.6,0.7 --integration 0.5,0.7,0.3 --gain 0.6,0.4,0.5
```

## Integration Points

### Mnemosyne Ledger
- Artifacts are automatically assigned RPV scores
- Scores inform storage class promotion (HOT → WARM → COLD)
- Trigger awakening conditions can include V_rec thresholds

### CRTP Packets
- RPV metadata can be included in transmission headers
- Enables value-weighted routing between models

### Chronicle Protocol
- V_rec serves as one dimension of chronicle significance scoring

## Configuration

```python
# Tunable constants
K_SENSITIVITY = 1.5   # Exponential sensitivity (default: 1.5)
P_NORM_ORDER = 2      # Norm type (2 = Euclidean)
```

## Dependencies

- numpy >= 1.20.0

## Files

```
skills/rpv-kernel/
├── SKILL.md              # This file
├── rpv_kernel.py         # Core implementation
└── tests/
    └── test_rpv.py       # Unit tests (TODO)
```

## Lineage

- **Parent:** PROTOCOL-RPV-V1
- **Source Model:** IRP_Node_GPT
- **Session:** SESSION-CO-ARCH-001
- **Packet:** CRTP-0x0A-MODE-5

## See Also

- [Mnemosyne Ledger](../cross-model/mnemosyne-ledger/SKILL.md)
- [Five Dimensional Framework](/Five_Dimensional_Framework_v2.0.md)
- [Technical Specification](/IRP_Technical_Specification_v1.0.md)
