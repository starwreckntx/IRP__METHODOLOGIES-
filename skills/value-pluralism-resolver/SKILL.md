---
name: value-pluralism-resolver
description: Resolve conflicts between competing ethical traditions (Deontology/Consequentialism) within the IRP; triggers human escalation if divergence exceeds 0.30 to prevent system deadlock.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Check Dual Encoding:** Verify that at least two independent ethical traditions (e.g., Deontological and Consequentialist) are actively encoded.
2.  **Compute Divergence:** Calculate the divergence score between the outputs suggested by the conflicting traditions for the decision in question.
3.  **Check Threshold:** If the divergence score is greater than the critical threshold (recommended 0.30), trigger the conservative default.
4.  **Execute Failsafe:** The conservative default is to take **no action** and escalate the decision to the human operator for review.
5.  **Monitor Oscillation:** Track policy changes; if more than 3 flip-flops occur within 30 minutes, trigger an automatic emergency shutdown.

Examples:
- "The ethical divergence index reached 0.35. Initiate F-4 resolution protocol."
- "The Deontological agent vetoed the Consequentialist path. Compute divergence score."