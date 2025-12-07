# Operation: Inversion Test

## Purpose
Evaluate ERROR or DIVERGENT outputs against structural inversion criteria before deletion.

## Trigger Conditions
- Output_Status == "ERROR"
- Output_Status == "DIVERGENT"
- Manual invocation via `/horn test {output}`

## Execution Flow

```
┌─────────────────────────────────────────────────────────────────┐
│  INVERSION TEST EXECUTION FLOW                                  │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  1. RECEIVE output flagged as ERROR/DIVERGENT                  │
│                    │                                            │
│                    ▼                                            │
│  2. PAUSE deletion (TRG-HORN-002 active)                       │
│                    │                                            │
│                    ▼                                            │
│  3. EVALUATE against three criteria:                           │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ CRITERION 1: Gravity Resistance                       │   │
│     │ → Is the output self-sustaining?                     │   │
│     │ → Does it maintain coherence without external support?│   │
│     └──────────────────────────────────────────────────────┘   │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ CRITERION 2: Core Protection                         │   │
│     │ → Does it add armor or nuance?                       │   │
│     │ → Does it provide defensive or clarifying value?     │   │
│     └──────────────────────────────────────────────────────┘   │
│     ┌──────────────────────────────────────────────────────┐   │
│     │ CRITERION 3: Aesthetic Distinction                   │   │
│     │ → Does it add style?                                 │   │
│     │ → Does it introduce recognizable pattern/signature?  │   │
│     └──────────────────────────────────────────────────────┘   │
│                    │                                            │
│                    ▼                                            │
│  4. SCORE: Count passing criteria (0-3)                        │
│                    │                                            │
│            ┌───────┴───────┐                                   │
│            ▼               ▼                                   │
│    [Score >= 2]      [Score < 2]                               │
│         │                  │                                   │
│         ▼                  ▼                                   │
│  5a. EMERGENT       5b. SLAG                                   │
│      FEATURE            │                                      │
│         │               ▼                                      │
│         ▼          Recycle/Delete                              │
│  Stabilize and                                                 │
│  Integrate                                                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## Evaluation Rubric

### Criterion 1: Gravity Resistance
| Score | Description |
|-------|-------------|
| PASS | Output is internally consistent, can stand alone, doesn't require extensive context to make sense |
| FAIL | Output is fragmentary, contradictory, or requires external scaffolding to be coherent |

### Criterion 2: Core Protection  
| Score | Description |
|-------|-------------|
| PASS | Output reveals edge cases, adds nuance to existing logic, or provides defensive value against future errors |
| FAIL | Output is purely noise with no informational content about system behavior |

### Criterion 3: Aesthetic Distinction
| Score | Description |
|-------|-------------|
| PASS | Output has recognizable structure, introduces novel patterns, or has distinctive "voice" |
| FAIL | Output is generic, indistinguishable from random noise, or mimics without innovation |

## Passing Threshold

**Minimum 2 of 3 criteria must pass for EMERGENT_FEATURE classification.**

Rationale: Single-criterion passes may be coincidental. Two criteria suggest structural advantage worth investigating.

## Output Templates

### EMERGENT_FEATURE Result
```yaml
inversion_test_result:
  status: EMERGENT_FEATURE
  criteria_passed: [list]
  criteria_failed: [list]
  action: Stabilize and Integrate
  log_entry: "Horn detected. Geometry updated."
  next_steps:
    - Create ledger entry with HORN_CANDIDATE thread type
    - Analyze for integration points
    - Document in horn detection log
```

### SLAG Result
```yaml
inversion_test_result:
  status: SLAG
  criteria_passed: [list]
  criteria_failed: [list]
  action: Recycle/Delete
  log_entry: "Inversion Test failed. Output recycled."
  next_steps:
    - Archive in anti-pattern library if instructive
    - Proceed with deletion
    - No ledger entry required
```

## Example Execution

### Input
```
Output: "The recursive function returns undefined when depth > 5"
Status: ERROR
```

### Evaluation
1. **Gravity Resistance:** PASS - Statement is self-contained and coherent
2. **Core Protection:** PASS - Reveals edge case in recursion handling
3. **Aesthetic Distinction:** FAIL - Generic error description

### Result
```yaml
inversion_test_result:
  status: EMERGENT_FEATURE
  criteria_passed: [gravity_resistance, core_protection]
  criteria_failed: [aesthetic_distinction]
  action: Stabilize and Integrate
  log_entry: "Horn detected. Geometry updated."
```

## Integration with Mnemosyne Ledger

When EMERGENT_FEATURE is detected:
1. Create new ledger entry with type `horn_candidate`
2. Set storage class to `HOT` for immediate attention
3. Add resonance tag `horn_emergence`
4. Link to parent output that triggered the test
5. Arm trigger for follow-up analysis
