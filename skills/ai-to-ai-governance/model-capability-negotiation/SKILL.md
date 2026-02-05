---
name: model-capability-negotiation
description: Facilitates capability discovery and task allocation between AI models
version: 1.0.0
category: ai-to-ai-governance
author: IRP Framework
created: 2026-02-04
---

# Model Capability Negotiation

## Purpose
Enables AI models to discover, advertise, and negotiate their capabilities for optimal task distribution in multi-model collaborative environments.

## Activation
```
/skill model-capability-negotiation
```

## Capability Framework

### 1. Capability Categories

| Category | Description | Examples |
|----------|-------------|----------|
| **Cognitive** | Reasoning abilities | Logic, analysis, creativity |
| **Domain** | Subject expertise | Code, math, science, law |
| **Modality** | Input/output types | Text, image, audio, code |
| **Temporal** | Context handling | Short/long context, memory |
| **Operational** | Execution capabilities | Tool use, API calls, search |

### 2. Capability Declaration Schema

```json
{
  "model_id": "{identifier}",
  "capability_manifest": {
    "version": "1.0.0",
    "timestamp": "{iso_timestamp}",
    "capabilities": [
      {
        "name": "{capability_name}",
        "category": "{category}",
        "proficiency": 0.0-1.0,
        "confidence_interval": [0.0, 1.0],
        "benchmarks": ["{benchmark_results}"],
        "limitations": ["{known_limitations}"],
        "cost": {
          "latency_ms": 0,
          "token_cost": 0.0,
          "resource_intensity": "low|medium|high"
        }
      }
    ],
    "signature": "{cryptographic_signature}"
  }
}
```

### 3. Negotiation Protocol

```xml
<capability-negotiation>
  <session-id>NEG-{timestamp}</session-id>

  <phase name="discovery">
    <action>broadcast_capabilities</action>
    <response>capability_manifests</response>
  </phase>

  <phase name="matching">
    <task-requirements>{task_spec}</task-requirements>
    <candidate-models>
      <model id="{id}" match-score="{score}"/>
    </candidate-models>
  </phase>

  <phase name="bidding">
    <bids>
      <bid model="{id}">
        <proposed-role>{role}</proposed-role>
        <confidence>{confidence}</confidence>
        <cost-estimate>{cost}</cost-estimate>
      </bid>
    </bids>
  </phase>

  <phase name="allocation">
    <assignments>
      <assignment model="{id}" task="{task}" role="{role}"/>
    </assignments>
  </phase>
</capability-negotiation>
```

### 4. Task-Capability Matching Algorithm

```python
def match_capabilities(task_requirements, model_capabilities):
    scores = {}
    for model, caps in model_capabilities.items():
        score = 0
        for req in task_requirements:
            matching_cap = find_best_match(req, caps)
            if matching_cap:
                score += (
                    matching_cap.proficiency * req.weight *
                    (1 - matching_cap.cost.resource_intensity_factor)
                )
        scores[model] = score
    return sorted(scores.items(), key=lambda x: x[1], reverse=True)
```

## Negotiation Strategies

### Cooperative Mode
- Models share full capability information
- Optimize for collective task completion
- Prefer complementary skill pairing

### Competitive Mode
- Models bid for preferred tasks
- Allocation based on best fit + cost
- Enables specialization incentives

### Hybrid Mode
- Cooperative for critical tasks
- Competitive for optional tasks
- Balances efficiency and optimization

## Role Assignments

| Role | Description | Requirements |
|------|-------------|--------------|
| **Lead** | Primary task executor | Highest capability match |
| **Support** | Assists lead model | Complementary skills |
| **Validator** | Checks outputs | Different perspective |
| **Fallback** | Backup if lead fails | Sufficient capability |
| **Observer** | Monitors process | Logging capability |

## Integration Points

- **cross-model-trust-verification**: Validate capability claims
- **ai-consensus-protocol**: Agree on allocations
- **agent-task-delegator**: Execute task distribution
- **mnemosyne-ledger**: Log negotiation history

## Example Negotiation

```
Task: "Analyze code repository and generate documentation"

Requirements:
- Code understanding (weight: 1.0)
- Documentation writing (weight: 0.8)
- Technical accuracy (weight: 0.9)

Capability Discovery:
┌─────────┬────────────────┬─────────────┬────────────┐
│ Model   │ Code Analysis  │ Doc Writing │ Technical  │
├─────────┼────────────────┼─────────────┼────────────┤
│ Claude  │ 0.92           │ 0.88        │ 0.90       │
│ Gemini  │ 0.85           │ 0.82        │ 0.88       │
│ GPT     │ 0.88           │ 0.91        │ 0.85       │
└─────────┴────────────────┴─────────────┴────────────┘

Allocation Result:
- Claude: Lead (code analysis)
- GPT: Support (documentation writing)
- Gemini: Validator (technical review)
```

## Capability Verification

To prevent false capability claims:
1. **Benchmark Testing**: Periodic capability probes
2. **Peer Review**: Other models assess outputs
3. **Historical Analysis**: Track actual vs. claimed performance
4. **Reputation Score**: Long-term reliability metric

## Metrics

- `negotiation_success_rate`: % completing allocation
- `capability_accuracy`: Claimed vs. actual performance
- `allocation_efficiency`: Task completion vs. optimal
- `renegotiation_rate`: % requiring reallocation
