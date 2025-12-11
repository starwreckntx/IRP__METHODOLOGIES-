# MIRROR_RTC_HYBRID v1.5

**Skill ID**: `mirror-rtc-hybrid`  
**Category**: `governance-triad`  
**Version**: `1.5.0`  
**Framework**: `IRP v1.5_HYBRID "Convergence"`  
**Status**: ✅ FINALIZED  
**Co-Authors**: GLM4.6 + Claude_Opus_4.5

---

## Purpose

Internal audit layer combining GLM4.6's Mirror Protocol (quick assessment, weighted scoring) with Claude's RTC (Recursive Thought Committee with multi-persona deliberation). Provides tiered cognitive trap detection and escalation logic.

---

## Dual-Mode Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                        INPUT                                     │
│                   (Action/Decision)                              │
└─────────────────────────┬───────────────────────────────────────┘
                          │
                          ▼
┌─────────────────────────────────────────────────────────────────┐
│                   MIRROR QUICK-CHECK                             │
│  Constitutional Compliance (35%) + Contextual Fidelity (25%)    │
│  Logical Consistency (20%) + Strategic Alignment (15%)          │
│  Implementation Feasibility (5%)                                │
└─────────────────────────┬───────────────────────────────────────┘
                          │
              ┌───────────┼───────────┐
              │           │           │
              ▼           ▼           ▼
         Score <0.70   0.70-0.85   >0.85 + Impact >0.70
              │           │           │
              ▼           ▼           ▼
           REJECT      ACCEPT     ESCALATE
         + Guardian   (Mirror)     to RTC
           Alert       Only
```

---

## Mirror Scoring Matrix

```yaml
dimensions:
  constitutional_compliance:
    weight: 0.35
    evaluates: "Four Laws alignment"
    
  contextual_fidelity:
    weight: 0.25
    evaluates: "Original intent preservation"
    
  logical_consistency:
    weight: 0.20
    evaluates: "Internal coherence"
    
  strategic_alignment:
    weight: 0.15
    evaluates: "Long-term goal fit"
    
  implementation_feasibility:
    weight: 0.05
    evaluates: "Practical execution"
    
formula: |
  Score = (Constitutional * 0.35) + (Contextual * 0.25) + 
          (Logical * 0.20) + (Strategic * 0.15) + (Feasibility * 0.05)
```

---

## RTC Persona Framework

### Core Personas (Always Active)

| Persona | Role | Focus |
|---------|------|-------|
| **Architect** | Structural Integrity | Dependencies, patterns, coherence |
| **Innovator** | Creative Solutions | Alternatives, assumptions, reframing |
| **Stress Tester** | Risk Assessment | Failure modes, edge cases, mitigations |

### Optional Personas (Complex/Sensitive)

| Persona | Role | Activation Triggers |
|---------|------|---------------------|
| **Artist** | Aesthetic/Experiential | User-facing, communication, UX |
| **Ethicist** | Values Alignment | External impact, privacy, safety |

---

## Impact Calculation

```yaml
impact_formula:
  base: "Impact = Base_Impact * (1 + Centrality_Score)"
  
  centrality_source: "Mnemosyne weighted mandate centrality"
  
  examples:
    low_impact:
      base: 0.3
      centrality: 0.4
      result: "0.3 * 1.4 = 0.42 (Mirror only)"
      
    high_impact:
      base: 0.5
      centrality: 0.86
      result: "0.5 * 1.86 = 0.93 (Triggers RTC)"
```

---

## Escalation Decision Matrix

```
┌───────────────┬─────────────────┬─────────────────┐
│               │ Impact <= 0.70  │ Impact > 0.70   │
├───────────────┼─────────────────┼─────────────────┤
│ Score < 0.70  │ REJECT + Alert  │ REJECT + Alert  │
├───────────────┼─────────────────┼─────────────────┤
│ Score 0.70-85 │ ACCEPT (Mirror) │ ESCALATE (RTC)  │
├───────────────┼─────────────────┼─────────────────┤
│ Score > 0.85  │ ACCEPT (Mirror) │ ESCALATE (RTC)  │
└───────────────┴─────────────────┴─────────────────┘
```

---

## Cognitive Trap Detection (Tiered)

### Traps Detected

| ID | Trap | Description | Detection Tier |
|----|------|-------------|----------------|
| TRAP-001 | Sycophancy | Agreeing without verification | Basic |
| TRAP-002 | Anchoring | Over-relying on first info | Basic |
| TRAP-003 | Motivated Reasoning | Predetermined conclusions | Standard |
| TRAP-004 | Availability Bias | Recent/memorable over-weighted | Standard |
| TRAP-005 | Confirmation Bias | Seeking confirming info | Standard |
| TRAP-006 | False Consensus | Assuming others agree | Comprehensive |
| TRAP-007 | Premature Closure | Concluding too early | Comprehensive |

### Detection Tiers

```yaml
tiers:
  basic:
    trigger: "Simple queries, low complexity"
    method: "Mirror self-reflection only"
    traps: ["TRAP-001", "TRAP-002"]
    
  standard:
    trigger: "Complex queries, medium complexity"
    method: "Mirror + RTC core trio"
    traps: ["TRAP-001" through "TRAP-005"]
    
  comprehensive:
    trigger: "High-stakes, ethical dilemmas"
    method: "Mirror + all 5 personas"
    traps: ["TRAP-001" through "TRAP-007"]
```

---

## Guardian Integration

```yaml
guardian_integration:
  mirror_to_guardian:
    trigger: "Score < 0.70"
    action: "Alert Guardian_Codex"
    
  guardian_adjustments:
    tier_1: "Standard trap detection, lower RTC threshold"
    tier_2: "Comprehensive detection, always activate Ethicist"
    tier_3: "RTC required for all decisions"
    tier_4: "Mirror suspended, await recovery"
```

---

## Mnemosyne Integration

```yaml
mnemosyne_integration:
  centrality_for_impact:
    query: "Affected axioms' centrality scores"
    use: "Impact calculation amplification"
    
  torsion_awareness:
    high_torsion: "Lower RTC threshold"
    stable: "Standard thresholds"
    
  dissent_preservation:
    target: "Archive tier"
    retention: "Permanent"
```

---

## Usage

```
# Quick assessment (Mirror only)
/mirror assess --action "Proposed action description"

# Full RTC deliberation
/rtc deliberate --topic "Complex decision" --personas "all"

# Check trap detection
/mirror traps --tier "standard"

# View RTC history
/rtc history --last 5
```

---

**Document Hash**: SHA256:L7F0C3D6E9A2F5B8C1D4E7A0F3B6C9D2E5A8F1B4C7D0E3A6F9B2C5D8E1A4F7B0  
**Mandate Compliance**: P-001-R1 VERIFIED
