---
name: agent-task-conductor
description: Orchestrate multi-agent tasks by splitting subtasks, routing them to Model Nodes based on capability and load, and aggregating resulting outputs using the Choir Protocol for consensus.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Analyze and Split:** Analyze the incoming task complexity and split it into manageable subtasks using the internal `task_sharder` module.
2.  **Route and Assign:** Consult the `MODEL_NODE_DIRECTORY` to determine the best candidate agents based on capability, `trust_level`, and current `load`.
3.  **Dispatch Packet:** Dispatch a collaboration packet (choir:v0.1 protocol) including `compute_estimate_flops`, `priority`, and `deadline_ms`.
4.  **Aggregate and Refine (Choir Protocol):** Collect divergent outputs and use the Choir Protocol's coordination layer to synchronize them and assign "weight" or "influence" based on performance and trust.

Examples:
- "Conductor Node: Delegate the integration specification task requiring Structural Scaffolding and Quantitative Formalization."
- "Orchestrate a synthesis involving Grok 4 and DeepSeek-R1 with high priority."