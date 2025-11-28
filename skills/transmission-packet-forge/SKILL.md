---
name: transmission-packet-forge
description: Create transmission packets for cross-model context preservation, analogous to TCP/IP for behavioral calibration across AI boundaries.
description: Generate explicit, structured packets (ENHANCED_PACKET v2.1) containing grounding checkpoints, identity, state, and cryptographic integrity bindings.
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
1.  **Define Header & Source:** Initiate the packet with a Header containing a unique ID, Timestamp, and CRITICALLY, the `source_model` (e.g., `claude-3-5-sonnet`, `gemini-1.5-pro`). This establishes the provenance of the transmission.

2.  **Extract Core Components:** Gather the mandatory packet elements: Identity (who, when, what), State (progress, pending items), Vocabulary, and Constraints.

3.  **Inject Persona-Skill Matrix (Binding):** Map active Personas to their Skills.
    * *Constraint:* You cannot list a Persona/Skill pairing without running the validation in Step 5.

4.  **Include Behavioral Profile:** Add the quantitative `AI_BEHAVIORAL_PROFILE` metrics (pushback_threshold, sycophancy_level).

5.  **Inject Integrity Hashes (Security):** * **Action:** For every active skill and persona, calculate or retrieve the SHA-256 hash of the source file.
    * **Verification:** Compare this hash against the `trusted_hash_registry.json`.
    * **Log:** Record the hash and the status (`VERIFIED`/`MISMATCH`) in the `integrity_check` block.
    * *Purpose:* This allows the next model to refuse a packet if the skills have been tampered with or "hallucinated."

6.  **Output Format:** Output the packet using the structured XML/JSON format v2.1.0.

Examples:
- "Generate an Enhanced Packet v2.1 for StarWreck, explicitly noting Gemini-1.5 as the source model and verifying the Red Team skill hash."
