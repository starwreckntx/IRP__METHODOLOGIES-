---
name: cross-session-integrity-check
description: Mandatory check at session start to verify self-integrity, detect Epistemic Amnesia (CF-6), and require a specific context-rich token for re-grounding if necessary.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Load State:** Attempt to load the previously persisted session state.
2.  **Verify Fingerprint:** Run an integrity check on the system's own state (fingerprint unchanged check) to detect internal drift.
3.  **Check Continuity (CF-6):** Verify if the instance is the same as the last session to detect Epistemic Amnesia.
4.  **Request Specific Token:** If state loading fails or continuity check fails, request a specific, context-rich `Valid Token` (not generic "Continue") from the human to trigger the Human-as-State-Repository Pattern.

Examples:
- "Initiate session: Run integrity check and confirm state persistence."
- "Load Antidote Registry and execute full session_init() protocol."