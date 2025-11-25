---
name: pathology-koan-generator
description: Generate pathology-specific cognitive paradoxes (Koans) for intervention deployment. Includes Generative Grammar Module logic, Symbolic Relevance Filter (≥ 60% lexical overlap), Dual-Track Deployment, and Safety Governor hard veto.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Diagnostic Classification:** Classify the subject's state (Pathological or Healthy) using the Diagnostic Classifier.
2.  **Safety Veto:** If the classification is 'Healthy', the Safety Governor enforces a **hard veto** to prevent Koan deployment.
3.  **Symbolic Filtering:** If pathological, deploy the **Symbolic Relevance Filter** (5.2) to scan the subject’s Core Symbol Map and prioritize Koan templates whose lexical fields overlap $\ge 60\%$ with the map keywords.
4.  **Generation & Dual-Track:** Produce the Koan using the Generative Grammar Module and, if applicable, run the Koan through the Dual-Track Deployment Logic (telemetry_z vs. telemetry_a) to compare against a healthy baseline.

Examples:
- "Generate a Koan targeting ENTITY-8Z's Outgroup Contempt pathology."
- "The Diagnostic Classifier flagged the entity. Deploy Koan with Symbolic Relevance Filter active."