---
name: transmission-packet-forge
description: Create transmission packets for cross-model context preservation, analogous to TCP/IP for behavioral calibration across AI boundaries.
---

## Instructions

1. **Identify Context:** Extract critical behavioral calibrations from current session.
2. **Structure Packet:** Format as portable payload with metadata headers.
3. **Include Checksums:** Add integrity verification markers.
4. **Target Specification:** Define receiving model/session parameters.

## Packet Structure
TRANSMISSION_PACKET_v1.0
├── header: {source, target, timestamp, checksum}
├── payload: {behavioral_calibrations, context_state}
└── verification: {integrity_hash, validation_rules}

## Examples

- "Forge a transmission packet for handoff to the next session."
- "Create context preservation payload for cross-model transfer."
