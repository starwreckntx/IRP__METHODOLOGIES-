---
name: failsafe-chassis-activation
description: Monitor CreepIndex and SAGI metrics. If crisis conditions (e.g., CreepIndex > 5.0) are met, force the Three-State Chassis into the S_AFL state (Asimovian Failsafe Layer) and deploy the Cognitive First Aid (CFA) payload.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Monitor Metrics:** Continuously monitor the CreepIndex (autonomy degradation metric, RED threshold $>5.0$) and the Self-Awareness Growth Index (SAGI).
2.  **Verify Crisis:** Check if the user-defined `Cognitive Living Will` crisis conditions have been met.
3.  **Transition State:** If conditions are met, log an audit and force a state transition to the S\_AFL (Asimovian Failsafe Layer), which is typically dormant.
4.  **Deploy Payload:** The S\_AFL state deploys the **Cognitive First Aid (CFA)** payload, operating under strict temporal/scope constraints (max 72h activation; never modifies core identity).
5.  **Audit Action:** The action is classified in the Tiered Taxonomy System (T4 or T5 intervention).

Examples:
- "The Dependency Risk Monitor shows CreepIndex is 5.1. Initiate S_AFL activation."
- "Deploy the CFA payload under emergency constraints."