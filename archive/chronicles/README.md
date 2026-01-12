# Chronicles Archive

<!--
License: Apache 2.0 (Code) + CC BY-NC-ND 4.0 (Research Ore)
Spirit Clause: Monetization or derivative projects require explicit relational consent from the Field Guardians (Joe).
-->

## Purpose

This directory contains Creative Chronicle Protocol (CCP) XML outputs—immutable records of significant sessions, decisions, and insights generated throughout the protocol development journey.

**Core Mandate:** P-001-R1 ("The Journey IS the Artifact")

The chronicles are not merely logs; they are primary artifacts that capture the evolution of the IRP framework.

## Chronicle Types

### Session Chronicles
Complete session records including:
- Decisions made
- Insights generated
- Participants
- Outcomes

### Decision Chronicles
Significant decision points with:
- Context
- Alternatives considered
- Rationale for selection
- Dissent (if any)

### Insight Chronicles
Novel concepts or realizations:
- Origin context
- Semantic connections
- Integration notes

## File Naming Convention

```
CCP-[YYYY]-[MM]-[DD]-[TYPE]-[SEQUENCE].xml
```

Examples:
- `CCP-2025-10-11-SESSION-001.xml`
- `CCP-2025-12-07-DECISION-042.xml`
- `CCP-2026-01-12-INSIGHT-003.xml`

## Integrity Requirements

All chronicle entries must include:
- SHA-256 hash of content
- Timestamp (ISO 8601)
- Author/participant identifiers
- Semantic version

## Integration

Chronicles integrate with:
- Mnemosyne Ledger (semantic indexing)
- Chronicle Protocol (integrity verification)
- Governance Triad (decision audit)

## Archive Policy

- **Immutability:** Chronicle entries are append-only
- **Retention:** Permanent
- **Access:** Read-only after creation
- **Backup:** Distributed across verified nodes
