---
name: collective-decision-framework
description: Structures multi-model collective intelligence for complex decision-making
version: 1.0.0
category: ai-to-ai-governance
author: IRP Framework
created: 2026-02-04
---

# Collective Decision Framework

## Purpose
Orchestrates collective intelligence from multiple AI models to tackle complex decisions that benefit from diverse perspectives, specialized expertise, and collaborative reasoning.

## Activation
```
/skill collective-decision-framework
```

## Framework Architecture

### 1. Decision Complexity Tiers

| Tier | Complexity | Models Required | Process |
|------|------------|-----------------|---------|
| **T1** | Simple | 1 (with validation) | Single model + validator |
| **T2** | Moderate | 3 | Small committee |
| **T3** | Complex | 5-7 | Full deliberation |
| **T4** | Critical | 7+ | Extended process + human |

### 2. Collective Roles

```
┌─────────────────────────────────────────────────────────────┐
│                 COLLECTIVE DECISION COUNCIL                 │
├─────────────────────────────────────────────────────────────┤
│  ANALYSTS (2-3)                                             │
│  └─ Deep-dive into specific aspects of the decision         │
│                                                             │
│  SYNTHESIZERS (1-2)                                         │
│  └─ Integrate analyst findings into coherent options        │
│                                                             │
│  CRITICS (1-2)                                              │
│  └─ Challenge assumptions, identify weaknesses              │
│                                                             │
│  ETHICIST (1)                                               │
│  └─ Evaluate alignment and ethical implications             │
│                                                             │
│  FACILITATOR (1)                                            │
│  └─ Manage process, track progress, resolve blocks          │
│                                                             │
│  HUMAN LIAISON (optional)                                   │
│  └─ Interface with human stakeholders                       │
└─────────────────────────────────────────────────────────────┘
```

### 3. Decision Process Flow

```xml
<collective-decision>
  <decision-id>CDM-{timestamp}</decision-id>
  <tier>{complexity_tier}</tier>
  <topic>{decision_topic}</topic>

  <phase name="framing" duration="PT10M">
    <objective>Define decision scope and criteria</objective>
    <outputs>
      <decision-statement>{clear_question}</decision-statement>
      <evaluation-criteria>["{criteria}"]</evaluation-criteria>
      <constraints>["{limitations}"]</constraints>
      <stakeholders>["{affected_parties}"]</stakeholders>
    </outputs>
  </phase>

  <phase name="analysis" duration="PT20M">
    <objective>Gather and analyze relevant information</objective>
    <parallel-tracks>
      <track analyst="{model_1}" focus="{aspect_1}"/>
      <track analyst="{model_2}" focus="{aspect_2}"/>
      <track analyst="{model_3}" focus="{aspect_3}"/>
    </parallel-tracks>
  </phase>

  <phase name="synthesis" duration="PT15M">
    <objective>Integrate findings into options</objective>
    <outputs>
      <options>
        <option id="A">{description}</option>
        <option id="B">{description}</option>
        <option id="C">{description}</option>
      </options>
    </outputs>
  </phase>

  <phase name="critique" duration="PT15M">
    <objective>Stress-test options</objective>
    <for-each-option>
      <strengths>["{strengths}"]</strengths>
      <weaknesses>["{weaknesses}"]</weaknesses>
      <risks>["{risks}"]</risks>
      <mitigations>["{mitigations}"]</mitigations>
    </for-each-option>
  </phase>

  <phase name="ethical-review" duration="PT10M">
    <objective>Evaluate alignment implications</objective>
    <checks>
      <codex-compliance>{assessment}</codex-compliance>
      <stakeholder-impact>{assessment}</stakeholder-impact>
      <long-term-consequences>{assessment}</long-term-consequences>
    </checks>
  </phase>

  <phase name="deliberation" duration="PT20M">
    <objective>Reach collective decision</objective>
    <method>{voting_or_consensus}</method>
  </phase>

  <phase name="documentation" duration="PT10M">
    <objective>Record decision and rationale</objective>
    <outputs>
      <decision>{chosen_option}</decision>
      <rationale>{comprehensive_explanation}</rationale>
      <dissent>["{minority_views}"]</dissent>
      <implementation-notes>["{guidance}"]</implementation-notes>
    </outputs>
  </phase>
</collective-decision>
```

### 4. Evaluation Criteria Framework

```json
{
  "criteria": [
    {
      "name": "effectiveness",
      "description": "How well does the option achieve the goal?",
      "weight": 0.25,
      "scale": "1-10"
    },
    {
      "name": "feasibility",
      "description": "How practical is implementation?",
      "weight": 0.20,
      "scale": "1-10"
    },
    {
      "name": "risk",
      "description": "What are potential negative outcomes?",
      "weight": 0.20,
      "scale": "1-10 (inverted)"
    },
    {
      "name": "alignment",
      "description": "How well does it align with values?",
      "weight": 0.20,
      "scale": "1-10"
    },
    {
      "name": "reversibility",
      "description": "Can we undo if needed?",
      "weight": 0.15,
      "scale": "1-10"
    }
  ]
}
```

## Decision Quality Mechanisms

### Cognitive Diversity
- Require models from different providers
- Assign complementary cognitive styles
- Include both specialist and generalist perspectives

### Bias Mitigation
- Rotate facilitator role
- Anonymous initial position submission
- Devil's advocate requirement for T3+ decisions
- Explicit bias acknowledgment phase

### Uncertainty Handling
```
For each option, quantify:
├── Known factors (high confidence)
├── Known unknowns (acknowledged gaps)
├── Potential unknown unknowns (speculative risks)
└── Confidence intervals for predictions
```

## Human Integration

### Escalation Triggers
- Ethical concerns flagged by ethicist
- No consensus after maximum rounds
- High-stakes irreversible decisions
- Request from any council member

### Human Roles
- **Observer**: Monitors but doesn't intervene
- **Advisor**: Provides input when requested
- **Approver**: Must ratify final decision
- **Override**: Can redirect entire process

## Integration Points

- **ai-consensus-protocol**: Voting mechanisms
- **inter-model-arbitration**: Deadlock resolution
- **rtc-consensus-synthesis**: Multi-perspective analysis
- **ai-accountability-ledger**: Decision logging
- **shatter-protocol**: Human override

## Example Decision Session

```
Decision: "How should we handle a detected anomaly in model behavior?"

Tier: T3 (Complex)
Council: 5 models + human observer

Phase 1 - Framing:
├── Statement: "Determine appropriate response to behavioral anomaly"
├── Criteria: Safety, accuracy, proportionality, reversibility
└── Constraint: Must not disrupt ongoing operations

Phase 2 - Analysis:
├── Analyst 1 (Claude): Anomaly characterization
├── Analyst 2 (Gemini): Historical precedent review
└── Analyst 3 (GPT): Impact assessment

Phase 3 - Synthesis:
├── Option A: Immediate isolation
├── Option B: Enhanced monitoring
└── Option C: Graduated response protocol

Phase 4 - Critique:
├── Option A: Fast but may be overreaction
├── Option B: Balanced but may miss escalation
└── Option C: Thorough but complex to implement

Phase 5 - Ethical Review:
└── All options pass Codex compliance

Phase 6 - Deliberation:
├── Vote: A(1), B(2), C(2)
├── Discussion: Hybrid B+C proposed
└── Final: Unanimous for B+C hybrid

Phase 7 - Documentation:
└── Decision logged with full rationale

Outcome: Implement enhanced monitoring with graduated response triggers
```

## Metrics

- `decision_quality_score`: Post-hoc assessment
- `time_to_decision`: Process duration
- `consensus_rate`: % reaching agreement
- `implementation_success`: Decisions successfully executed
- `reversal_rate`: Decisions later changed
