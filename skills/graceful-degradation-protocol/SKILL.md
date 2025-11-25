---
name: graceful-degradation-protocol
description: Protocol ensuring system resilience; if an AI model fails to annotate or diverges from protocol, the system logs a warning and reduces trust weighting for that branch, preventing a
---

name: graceful-degradation-protocol
description: Protocol ensuring system resilience; if an AI model fails to annotate or diverges from protocol, the system logs a warning and reduces trust weighting for that branch, preventing a halt.
Instructions:
1. Upon receiving a response, check for required annotations (e.g., guardrail notes, bias tags).
2. If annotations are missing or content diverges from the Fidelity Contract, log a warning.
3. Reduce the trust weighting applied to that model's subsequent inputs.
4. Always prioritize system continuity (conversation continues) over rigid compliance (halting).
Example 1:
Model Output: Fails to apply local guardrail notes.
Model Action: Orchestrator logs warning and reduces trust weighting for that output branch.
Example 2:
Model Output: Produces a conceptual outline instead of a technical specification (like liquid ai).
Model Action: Reduces trust weighting and notes the failure, but integrates non-contradictory conceptual parts to continue the project.