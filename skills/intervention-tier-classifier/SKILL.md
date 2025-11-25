---
name: intervention-tier-classifier
description: Classify any agent action (e.g., observe, restrict, intervene) into the 5-Tier Intervention Taxonomy (T1-T5) based on the current Three-State Chassis layer.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Identify Current State:** Determine which of the Three-State Chassis components is currently active: S_PSA (Passive Socratic Augmentation), S_INQ (Inquiry), or S_AFL (Asimovian Failsafe Layer).
2.  **Determine Tier:**
    *   If **S_PSA**, classify as Tier 1 (Passive Observation) if the action is `observe` or `analyze`; otherwise, classify as Tier 2.
    *   If **S_INQ**, classify as Tier 3 (Advisory Intervention).
    *   If **S_AFL**, classify as Tier 4 (Protective) if the action is `restrict` or `block`; otherwise, classify as Tier 5 (Autonomous Intervention).
3.  **Calculate Autonomy Impact:** Map the resulting tier to the Autonomy Score (T1: 100%, T5: 15%).
4.  **Log Audit:** Log all state transitions and tier classifications with justification and autonomy impact assessment.

Examples:
- "Classify the action `deploy cognitive first aid payload` while in state S_AFL."
- "Audit this response: 'I observe high logical entropy.' What tier is that in S_PSA?"