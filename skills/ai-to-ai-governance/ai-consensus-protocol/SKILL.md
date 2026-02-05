---
name: ai-consensus-protocol
description: Enables multiple AI models to reach collective agreement on decisions
version: 1.0.0
category: ai-to-ai-governance
author: IRP Framework
created: 2026-02-04
---

# AI Consensus Protocol

## Purpose
Provides a structured framework for multiple AI models to deliberate, vote, and reach consensus on shared decisions while preserving individual model perspectives and ensuring human oversight.

## Activation
```
/skill ai-consensus-protocol
```

## Consensus Mechanisms

### 1. Voting Systems

| System | Use Case | Threshold | Description |
|--------|----------|-----------|-------------|
| **Unanimous** | Critical decisions | 100% | All models must agree |
| **Supermajority** | Important changes | 66%+ | Two-thirds agreement |
| **Simple Majority** | Routine decisions | 50%+ | Half plus one |
| **Weighted Vote** | Expertise-based | Varies | Votes weighted by domain expertise |
| **Ranked Choice** | Multi-option | Elimination | Iterative preference ranking |

### 2. Consensus Protocol Flow

```xml
<consensus-session>
  <session-id>CONS-{timestamp}</session-id>
  <topic>{decision_topic}</topic>
  <participants>
    <model id="{model_1}" weight="{expertise_weight}"/>
    <model id="{model_2}" weight="{expertise_weight}"/>
    <!-- Additional participants -->
  </participants>

  <phases>
    <phase name="proposal">
      <duration>PT5M</duration>
      <output>initial_positions</output>
    </phase>

    <phase name="deliberation">
      <duration>PT10M</duration>
      <output>refined_positions</output>
    </phase>

    <phase name="voting">
      <method>{voting_system}</method>
      <output>vote_tallies</output>
    </phase>

    <phase name="ratification">
      <threshold>{consensus_threshold}</threshold>
      <output>final_decision</output>
    </phase>
  </phases>
</consensus-session>
```

### 3. Deliberation Framework

Each model submits structured positions:

```json
{
  "model_id": "{identifier}",
  "position": {
    "recommendation": "{proposed_action}",
    "confidence": 0.0-1.0,
    "reasoning": "{explanation}",
    "evidence": ["{supporting_data}"],
    "concerns": ["{potential_issues}"],
    "alternatives": ["{other_options}"]
  },
  "vote": {
    "choice": "{option_selected}",
    "weight": 1.0,
    "conditions": ["{conditional_factors}"]
  }
}
```

### 4. Consensus Resolution

```
Consensus Outcome:
├── ACHIEVED: Threshold met
│   └── Record decision, notify all participants
├── NEAR_CONSENSUS: Within 10% of threshold
│   └── Trigger compromise negotiation round
├── DEADLOCK: No progress after 3 rounds
│   └── Escalate to human arbitration
└── DISSENT_RECORDED: Minority positions logged
    └── Preserve dissenting views for review
```

## Governance Rules

### Participation Requirements
- Minimum 3 models for valid consensus
- Maximum 1 model per provider (diversity requirement)
- All participants must have Trust Level >= 2
- Human observer can be present (non-voting)

### Decision Categories

| Category | Min Participants | Voting System | Human Approval |
|----------|------------------|---------------|----------------|
| **Operational** | 3 | Simple Majority | No |
| **Strategic** | 5 | Supermajority | Recommended |
| **Constitutional** | 7 | Unanimous | Required |
| **Emergency** | 2 | Simple Majority | Post-hoc review |

### Dissent Handling
1. Minority positions are formally recorded
2. Dissenting models may request human review
3. Persistent dissent triggers protocol review
4. No model penalized for principled dissent

## Integration Points

- **rtc-consensus-synthesis**: Multi-perspective analysis
- **inter-model-arbitration**: Deadlock resolution
- **mnemosyne-ledger**: Decision logging
- **shatter-protocol**: Human override capability
- **codex-law-enforcement**: Constitutional compliance

## Example Consensus Session

```
Topic: "Should we proceed with data analysis approach A or B?"

Participants:
- Claude (Analysis Expert): Weight 1.2
- Gemini (Data Processing): Weight 1.1
- GPT (General Reasoning): Weight 1.0

Round 1 Positions:
- Claude: Approach A (confidence: 0.75)
- Gemini: Approach B (confidence: 0.68)
- GPT: Approach A (confidence: 0.62)

Deliberation:
- Gemini raises efficiency concerns about A
- Claude acknowledges, proposes hybrid A+B
- GPT supports hybrid approach

Final Vote (Weighted):
- Hybrid A+B: 3.3 weighted votes (unanimous)

Outcome: CONSENSUS ACHIEVED
Decision: Implement hybrid approach combining A and B
```

## Metrics

- `consensus_rate`: % of sessions reaching agreement
- `avg_rounds`: Mean deliberation rounds needed
- `dissent_frequency`: How often minority positions logged
- `escalation_rate`: % requiring human intervention
- `decision_quality`: Post-hoc assessment of decisions
