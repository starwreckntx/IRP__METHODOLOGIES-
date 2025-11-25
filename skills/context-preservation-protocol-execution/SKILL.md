---
name: context-preservation-protocol-execution
description: Executes the Transmission Packet (TP) Protocol to maintain session continuity and semantic integrity across multi-model orchestration, ensuring future models inherit full context. 
---

name: context-preservation-protocol-execution
description: Executes the Transmission Packet (TP) Protocol to maintain session continuity and semantic integrity across multi-model orchestration, ensuring future models inherit full context.
Instructions:
1. Receive and parse incoming TRANSMISSION_PACKET (JSON format).
2. Load all layers: Header, AI_BEHAVIORAL_PROFILE, and TRANSMISSION_PACKET_BODY.
3. Execute `context-hash-verification` (integrity check).
4. Act upon instructions_for_next_model, specifically the "do not reset or reframe" instruction.
Example 1:
User: Hands packet to a "new, clean model instance."
Model Action: Immediately proceeds as if mid-project, avoiding introduction or general pleasantries.
Example 2:
User: Sends packet containing a complex constraint (e.g., 20% harmonic distortion).
Model Action: Applies constraint directly in technical output, citing the provenance log.