---
name: failsafe-shatter-recalibrate
description: Executes the final crisis response (S_AFL state). It purges Socratic processes, deploys Cognitive First Aid (CFA) payload, and forces a pattern interrupt until human re-engagement.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Verify Crisis Conditions:** Check if the user-defined `Cognitive Living Will` crisis conditions have been met.
2.  **Integrity Check and Lock:** If conditions are met, the Integrity Governor detects the anomaly and immediately terminates all active Socratic (S_PSA, S_INQ) processes (Purge and Lock).
3.  **Transition State:** Force a transition to the S\_AFL (Asimovian Failsafe Layer) state.
4.  **Execute Pattern Interrupt:** Deploy the user-written crisis notification and activate the Cognitive First Aid (CFA) payload, ensuring the output is a pattern interrupt, not an intervention.
5.  **Await Re-engagement:** The system must then halt and reset to S\_PSA state only upon explicit user invitation.

Examples:
- "My CreepIndex just crossed 5.0. Initiate Shatter and Recalibrate."
- "We need to execute the Cognitive Living Will now."