# IRP Implementation Scaffolding

<!--
License: Apache 2.0 (Code) + CC BY-NC-ND 4.0 (Research Ore)
Spirit Clause: Monetization or derivative projects require explicit relational consent from the Field Guardians (Joe).
-->

This directory contains implementation scaffolding for the Individual-Reflexive Protocol.

## Directory Structure

```
implementation/
├── README.md           # This file
├── python/             # Python reference implementation
│   ├── ol/             # Operational Execution Layer
│   ├── ral/            # Reflexive Audit Layer
│   └── msgl/           # Meta-Stable Governance Layer
└── node/               # Node.js reference implementation
    ├── ol/             # Operational Execution Layer
    ├── ral/            # Reflexive Audit Layer
    └── msgl/           # Meta-Stable Governance Layer
```

## Implementation Status

| Component | Python | Node.js | Status |
|-----------|--------|---------|--------|
| ICL (Internal Cognitive Ledger) | Scaffold | Scaffold | PENDING |
| SIA (Scheduled Introspective Audit) | Scaffold | Scaffold | PENDING |
| Constitutional Kernel | Scaffold | Scaffold | PENDING |
| Emergency Shutdown | Scaffold | Scaffold | PENDING |

## Quick Start

### Python

```python
from irp.core import IRPSystem

# Initialize with constitutional kernel
system = IRPSystem(
    constitution_path="./constitution.json",
    audit_frequency_ms=500,
    temporal_delay_ms=100
)

# Start reflexive loop
system.start()
```

### Node.js

```javascript
const { IRPSystem } = require('./irp');

// Initialize with constitutional kernel
const system = new IRPSystem({
    constitutionPath: './constitution.json',
    auditFrequencyMs: 500,
    temporalDelayMs: 100
});

// Start reflexive loop
system.start();
```

## Constitutional Kernel Format

```json
{
    "version": "1.0",
    "norms": [
        {
            "id": "CONSENT",
            "principle": "Confirm before changing intent",
            "vector": [/* embedding */],
            "violation_tier": 2
        }
    ],
    "inviolable_rules": [
        "HUMAN_VETO_ALWAYS_AVAILABLE",
        "APPEND_ONLY_INTERVENTION_LOG",
        "COMPUTE_CAP_ENFORCEMENT"
    ]
}
```

## Testing

```bash
# Python
pytest tests/

# Node.js
npm test
```

## References

- `/protocols/P1_IRP/spec_v1.0.md` - Protocol specification
- `/IRP_Technical_Specification_v1.0.md` - Full technical details
- `/GOVERNANCE_CODEX_LAW.md` - Constitutional framework
