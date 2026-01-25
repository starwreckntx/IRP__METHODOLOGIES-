# Archive Index

<!--
License: Apache 2.0 (Code) + CC BY-NC-ND 4.0 (Research Ore)
Spirit Clause: Monetization or derivative projects require explicit relational consent from the Field Guardians (Joe).
-->

**Last Updated:** 2026-01-12
**Document Hash:** SHA256:PENDING_MANIFEST_GENERATION

---

## Overview

This archive contains the immutable record of the IRP protocol development journey. Per mandate P-001-R1 ("The Journey IS the Artifact"), these records are primary artifacts, not secondary documentation.

---

## Directory Structure

```
archive/
├── ARCHIVE_INDEX.md              # This file
├── chronicles/                   # Creative Chronicle Protocol outputs
│   ├── README.md                # Chronicle archive guide
│   ├── creative_chronicle_20241129_tcdp_seed.xml
│   ├── OHP-20251024-103900-SYM-UPDATE.xml
│   ├── LE-20251207-SESSION-RPV-HORN.xml
│   └── LE-20251207-RPV-KERNEL.xml
└── handoff_packets/              # Cross-model context transfers
    ├── README.md                # Handoff archive guide
    ├── forward_transmission_packet_20241129_tcdp_genesis.xml
    └── CRTP-0x16-FORWARD-CONTEXT.xml
```

---

## Chronicle Index

| Date | Type | ID | Summary |
|------|------|-----|---------|
| 2024-11-29 | SESSION | TCDP-SEED | Theatrical Compliance Detection Protocol genesis session |
| 2025-10-24 | DECISION | OHP-SYM | Orchestration Handshake Protocol symbolic update |
| 2025-12-07 | SESSION | RPV-HORN | RPV Kernel and Horn Maneuver development session |
| 2025-12-07 | ARTIFACT | RPV-KERNEL | Research-Praxis-Value Kernel artifact |

---

## Handoff Packet Index

| Date | Type | Source | Target | Fidelity |
|------|------|--------|--------|----------|
| 2024-11-29 | FCP | Claude-Sonnet-4.5 | OPEN | N/A (Genesis) |
| 2025-12-07 | FCP | Claude | Multi | VERIFIED |

---

## Integrity Verification

To verify archive integrity using the IRP Integrity Forge:

```bash
# Generate archive manifest
python skills/artifact-integrity-forge/scripts/sha256_hasher.py \
    --mode create --dir archive --manifest archive/manifest.json

# Verify archive against manifest
python skills/artifact-integrity-forge/scripts/sha256_hasher.py \
    --mode verify --dir archive --manifest archive/manifest.json
```

Manual verification:

```bash
# Verify individual file
sha256sum archive/chronicles/[filename]

# Verify entire archive
find archive/ -type f -name "*.xml" -exec sha256sum {} \; | sort
```

---

## Archive Statistics

- **Total Chronicles:** 4
- **Total Handoff Packets:** 2
- **Archive Size:** ~35KB
- **Earliest Entry:** 2024-11-29
- **Latest Entry:** 2025-12-07 (pre-Genesis artifacts)
- **Genesis Block:** 2026-01-12

---

## Provenance Chain

```
2024-11-29: TCDP Genesis (Claude-Sonnet-4.5 + Joseph)
    │
    ▼
2025-10-24: OHP Symbolic Update
    │
    ▼
2025-12-07: RPV Kernel + Horn Maneuver
    │
    ▼
2026-01-12: GENESIS BLOCK - Sovereign Repository Instantiation
```

---

## Related Resources

- `/protocols/P4_PINENE/` - Cross-model preservation protocol
- `/skills/cross-model/mnemosyne-ledger/` - Semantic memory system
- `/skills/artifact-integrity-forge/` - SHA-256 integrity verification
- `/integration/` - Legacy integration materials
- `/.github/workflows/validate-integrity.yml` - Automated integrity checks

---

**Mandate Compliance:** P-001-R1 VERIFIED
**Codex Law Status:** INTEGRITY (preserved through cryptographic verification)
