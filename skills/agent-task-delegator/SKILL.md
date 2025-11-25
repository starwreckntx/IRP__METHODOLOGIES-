---
name: agent-task-delegator
description: Analyzes task complexity, splits and routes subtasks to Model Nodes based on capability/load/trust_level, and aggregates outputs using the Choir Protocol to achieve consensus.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Analyze and Split:** Analyze the incoming task type and complexity. Use a `task_sharder` module to split the job into subtasks based on compute estimates.
2.  **Route and Distribute:** Consult the `MODEL_NODE_DIRECTORY` to determine agent load (`load`) and reliability (`trust_level`). Use the `node_distributor` to assign subtasks, prioritizing trusted and low-load agents.
3.  **Execute and Log:** Model Nodes perform partial or full execution, logging their contribution, divergence, and compute cost.
4.  **Aggregate Outputs:** The Conductor Node aggregates outputs and uses the Choir Protocol's `output_aggregator` to perform consensus/refinement, typically using response weighting based on trust level.

Examples:
- "Conductor Node: Delegate this architecture review task requiring structural-scaffolding and quantitative-formalization capabilities."
- "Orchestrate a workflow involving text generation, summarization, and code generation across three agents."