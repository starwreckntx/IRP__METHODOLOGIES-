---
name: model-convergence-forecast
description: Predict multi-agent collaboration outcomes by calculating Diversity Score. Forecasts CONSENSUS_SINK (high probability of converging to first plausible solution) and lists critical risks (e.g., groupthink).
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Input Configuration:** Receive the task description and the participating agent configuration (e.g., agent types, roles).
2.  **Calculate Diversity:** Compute the agent diversity score. If the diversity score is below the danger threshold (e.g., 0.05), predict **CONSENSUS_SINK**.
3.  **Predict Metrics:** Forecast the probability, expected iterations (e.g., 6-11 cycles), and stability of the convergence.
4.  **Identify Critical Risks:** If CONSENSUS\_SINK is predicted, explicitly list the associated critical risks, such as Groupthink and converging to the first plausible solution rather than the best one.
5.  **Output Optimal Use Case:** Provide recommendations for when this configuration is optimally used (e.g., deadline-driven deliverables).

Examples:
- "Forecast the convergence outcome for a 3-agent SYNTHESIZER collaboration."
- "The diversity score is 0.044. Initiate Convergence Forecast."