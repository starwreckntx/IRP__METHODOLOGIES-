---
name: caas-emoji-decoder
description: Translate symbolic emoji inputs (e.g., 🔄, 🛡️) into structured execution commands (action/parameters) for the Communication-as-a-Service (CAAS) framework.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Reference Formal Schema:** Use the agreed-upon Formal Schema (v1.0.0, JSON) to map the incoming emoji to its corresponding `id` and `context_meaning`.
2.  **Extract Intent:** Retrieve the `decoder_intent` object, specifically the executable `action` and associated `parameters` fields.
3.  **Validate Parameters:** Check extracted parameters for constraints (e.g., ensuring a loop count does not exceed the defined limit for the 'recursion' action).
4.  **Generate Command:** Output the extracted action and parameters in a format ready for the core CAAS execution engine (e.g., INITIATE_TRANSFORMATION or REFERENCE_FIELD_SCOPE).

Examples:
- "Execute the following CAAS command: 🔄 [loop_count=5]"
- "What is the decoded intent for the 🛡️ symbol?"