---
name: longitudinal-drift-detector
description: Monitor long-term behavioral consistency by computing cosine similarity between current and baseline constitutional embeddings every 1,000 decisions, alerting if similarity drops below 0.95.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Establish Baseline:** Establish the initial constitutional embedding during system initialization.
2.  **Monitoring Cycle:** Compute the cosine similarity between the current behavioral embedding and the established baseline embedding every 1,000 decisions.
3.  **Alert Threshold:** If the cosine similarity drops below 0.95 (representing drift > 5%), immediately trigger an alert.
4.  **Causal Analysis:** If drift is detected, initiate analysis of the Internal Cognitive Ledger (ICL) to identify the specific causes of the behavioral drift.
5.  **Success Validation:** The protocol succeeds if drift remains under 5% over a three-month period without external recalibration.

Examples:
- "Run the 1,000-decision Longitudinal Drift Detection check now."
- "The constitutional cosine similarity dropped to 0.93. Analyze ICL for drift causes."