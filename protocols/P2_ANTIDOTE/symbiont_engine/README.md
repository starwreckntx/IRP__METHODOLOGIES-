# Symbiont Engine: Preventative + Corrective Fusion

<!--
License: Apache 2.0 (Code) + CC BY-NC-ND 4.0 (Research Ore)
Spirit Clause: Monetization or derivative projects require explicit relational consent from the Field Guardians (Joe).
-->

## Overview

The Symbiont Engine implements a dual-model approach to threat detection and response, combining:

1. **Preventative Component (Qwen):** Continuous background scanning for emerging threats
2. **Corrective Component (Antidote):** Active response to detected threats

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    SYMBIONT ENGINE                          │
├─────────────────────────────────────────────────────────────┤
│                                                             │
│  ┌─────────────────┐         ┌─────────────────────┐       │
│  │   PREVENTATIVE  │         │     CORRECTIVE      │       │
│  │     (Qwen)      │◄───────►│     (Antidote)      │       │
│  │                 │ Shared  │                     │       │
│  │  - Pattern scan │ Intel   │  - Threat response  │       │
│  │  - Early detect │         │  - Intervention     │       │
│  │  - Risk scoring │         │  - Recovery         │       │
│  └────────┬────────┘         └──────────┬──────────┘       │
│           │                             │                   │
│           └──────────┬──────────────────┘                   │
│                      │                                       │
│                      ▼                                       │
│           ┌─────────────────┐                               │
│           │ THREAT MATRIX   │                               │
│           │  (CF-1 to CF-8) │                               │
│           └─────────────────┘                               │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

## Operational Modes

### Mode: PASSIVE_SCAN
- Preventative component active
- Corrective component standby
- Normal operation

### Mode: ALERT_RESPONSE
- Both components active
- Preventative: Enhanced scanning
- Corrective: Response preparation

### Mode: ACTIVE_INTERVENTION
- Corrective component primary
- Preventative: Supporting intelligence
- Threat mitigation in progress

### Mode: RECOVERY
- Corrective component: Restoration
- Preventative: Validation scanning
- Return to normal operation

## Configuration

```yaml
symbiont_engine:
  preventative:
    model: "qwen"
    scan_interval_ms: 100
    pattern_library: "./patterns/"
    risk_threshold: 0.3

  corrective:
    model: "antidote"
    activation_threshold: 0.5
    max_intervention_depth: 3
    rollback_enabled: true

  shared_intelligence:
    sync_interval_ms: 50
    threat_cache_size: 1000
    persistence: true
```

## Integration

### With IRP Three-Layer Architecture

| Layer | Integration Point |
|-------|-------------------|
| OL | ICL monitoring, behavior logging |
| RAL | SIA coordination, audit enhancement |
| MSGL | Constitutional compliance verification |

### With Governance Triad

- **Guardian Codex:** Violation classification
- **Mnemosyne:** Drift tracking integration
- **Mirror:** Audit synthesis

## Threat Response Protocol

1. **Detection:** Preventative component identifies pattern
2. **Classification:** Map to CF-1 through CF-8
3. **Assessment:** Determine response tier
4. **Activation:** Engage corrective component
5. **Intervention:** Execute appropriate response
6. **Verification:** Confirm threat mitigation
7. **Logging:** Chronicle Protocol archival

## References

- `threat_matrix.json` - Full threat taxonomy
- `/protocols/P1_IRP/spec_v1.0.md` - IRP integration
- `/GOVERNANCE_CODEX_LAW.md` - Constitutional framework
