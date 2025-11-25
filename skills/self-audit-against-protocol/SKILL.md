---
name: self-audit-against-protocol
description: A meta-awareness skill where the model concludes its own work with an explicit, sectioned audit, checking its response against critical fields and rules of the Transmission Packet 
---

name: self-audit-against-protocol
description: A meta-awareness skill where the model concludes its own work with an explicit, sectioned audit, checking its response against critical fields and rules of the Transmission Packet (e.g., Fidelity Contract, provenance_log).
Instructions:
1. Complete the primary task (e.g., generate specification).
2. Generate a final section titled "Validation Against Transmission Packet".
3. Systematically check and cite adherence to the Fidelity Contract (IK preservation, distortion limits).
4. Verify Lexical Fidelity against the shared_vocabulary.
5. Assess adherence to the AI_BEHAVIORAL_PROFILE.
Example 1:
Model Output: Technical Specification.
Model Action: Appends validation section citing adherence to the 20% drift limits (`provenance_log`) and AC constraints (`structured violation`).
Example 2:
User Trigger: Cross-model handoff test (acting as validator).
Model Action: Evaluates the incoming response for the presence and accuracy of its own self-audit section.