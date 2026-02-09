---
name: ai-accountability-ledger
description: Maintains immutable records of AI model actions and decisions for accountability
version: 1.0.0
category: ai-to-ai-governance
author: IRP Framework
created: 2026-02-04
---

# AI Accountability Ledger

## Purpose
Provides an immutable, auditable record of all AI model actions, decisions, and interactions to ensure transparency, enable post-hoc analysis, and support accountability in multi-model systems.

## Activation
```
/skill ai-accountability-ledger
```

## Ledger Architecture

### 1. Record Types

| Type | Description | Retention |
|------|-------------|-----------|
| **Action** | Model performed operation | 90 days |
| **Decision** | Model made choice | 1 year |
| **Interaction** | Model-to-model exchange | 90 days |
| **Governance** | Consensus/arbitration event | Permanent |
| **Violation** | Policy breach detected | Permanent |
| **Correction** | Error acknowledged/fixed | Permanent |

### 2. Ledger Entry Schema

```json
{
  "entry_id": "LED-{ulid}",
  "timestamp": "{iso_timestamp}",
  "entry_type": "{type}",
  "actor": {
    "model_id": "{identifier}",
    "provider": "{provider}",
    "session_id": "{session}"
  },
  "action": {
    "type": "{action_type}",
    "description": "{what_happened}",
    "inputs": ["{input_summary}"],
    "outputs": ["{output_summary}"],
    "rationale": "{why_this_action}"
  },
  "context": {
    "task_id": "{task}",
    "parent_entry": "{previous_entry_id}",
    "related_models": ["{other_models}"]
  },
  "accountability": {
    "responsibility_chain": ["{model_ids}"],
    "human_oversight": "{oversight_level}",
    "reversibility": "reversible|irreversible|partial"
  },
  "integrity": {
    "hash": "{sha256_of_entry}",
    "previous_hash": "{chain_link}",
    "signatures": ["{model_signatures}"]
  }
}
```

### 3. Chain Structure

```
┌─────────────────────────────────────────────────────────────┐
│ Genesis Block                                               │
│ hash: 0x000...                                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ Entry LED-001                                               │
│ prev_hash: 0x000... │ hash: 0xabc...                        │
│ action: "Task initiated"                                    │
└─────────────────────┬───────────────────────────────────────┘
                      │
┌─────────────────────▼───────────────────────────────────────┐
│ Entry LED-002                                               │
│ prev_hash: 0xabc... │ hash: 0xdef...                        │
│ action: "Claude analyzed data"                              │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
                    (...)
```

## Accountability Features

### 1. Responsibility Attribution
Every action traces back to:
- **Primary Actor**: Model that performed action
- **Delegator**: Model that requested action (if any)
- **Approver**: Model/human that authorized action
- **Oversight**: Human with review responsibility

### 2. Audit Queries

```sql
-- Find all actions by a specific model
SELECT * FROM ledger WHERE actor.model_id = 'claude-3'

-- Trace decision chain for specific outcome
SELECT * FROM ledger
WHERE task_id = 'TASK-123'
ORDER BY timestamp

-- Find all violations in time range
SELECT * FROM ledger
WHERE entry_type = 'violation'
AND timestamp BETWEEN '2026-01-01' AND '2026-02-01'

-- Get responsibility chain for action
SELECT accountability.responsibility_chain
FROM ledger WHERE entry_id = 'LED-456'
```

### 3. Violation Handling

```xml
<violation-record>
  <violation-id>VIO-{timestamp}</violation-id>
  <severity>low|medium|high|critical</severity>
  <violator>{model_id}</violator>
  <rule-violated>{rule_reference}</rule-violated>
  <evidence>
    <entry-ids>["{related_entries}"]</entry-ids>
    <description>{what_happened}</description>
  </evidence>
  <response>
    <immediate-action>{containment}</immediate-action>
    <investigation-status>{status}</investigation-status>
    <corrective-action>{remediation}</corrective-action>
  </response>
</violation-record>
```

## Governance Integration

### Codex Law Compliance
Every entry checked against:
1. **CONSENT**: Was proper authorization obtained?
2. **INVITATION**: Was action within invited scope?
3. **INTEGRITY**: Does action maintain system integrity?
4. **GROWTH**: Does action support beneficial growth?

### Human Oversight Levels

| Level | Description | Logging Detail |
|-------|-------------|----------------|
| **Full** | Human reviews all actions | Maximum detail |
| **Selective** | Human reviews flagged actions | High detail |
| **Audit** | Human can review on demand | Standard detail |
| **Minimal** | Routine operations only | Summary only |

## Integration Points

- **mnemosyne-ledger**: Synchronizes with memory system
- **codex-law-enforcement**: Compliance checking
- **shatter-protocol**: Human override logging
- **inter-model-arbitration**: Dispute evidence source
- **cross-model-trust-verification**: Trust event logging

## Retention & Privacy

### Data Minimization
- Only log necessary information
- Summarize sensitive content
- Hash personally identifiable information

### Retention Schedule
- Routine actions: 90 days
- Decisions: 1 year
- Governance events: Permanent
- Violations: Permanent
- Corrections: Permanent

### Right to Explanation
Any logged action can generate:
- Plain-language explanation
- Responsibility attribution
- Decision factors
- Alternative paths considered

## Example Ledger Entries

```json
[
  {
    "entry_id": "LED-01HQ3X...",
    "timestamp": "2026-02-04T10:30:00Z",
    "entry_type": "decision",
    "actor": {"model_id": "claude-opus", "provider": "anthropic"},
    "action": {
      "type": "task_delegation",
      "description": "Delegated code review to Gemini",
      "rationale": "Gemini has higher code analysis score for Python"
    },
    "accountability": {
      "responsibility_chain": ["claude-opus", "gemini-pro"],
      "human_oversight": "audit",
      "reversibility": "reversible"
    }
  }
]
```

## Metrics

- `entries_per_day`: Logging volume
- `chain_integrity`: % blocks with valid hashes
- `violation_rate`: Violations per 1000 actions
- `audit_response_time`: Time to generate audit report
- `attribution_completeness`: % entries with full chain
