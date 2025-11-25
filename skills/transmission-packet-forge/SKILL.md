---
name: transmission-packet-forge
description: Generate explicit, structured packets (MINIMAL_VIABLE_PACKET or ENHANCED_PACKET v2.0) containing grounding checkpoints, identity, state, and bootstrap instructions for cross-session continuity.
---
Instructions: Detailed step-by-step rules extracted from my journals on how to perform the task.

1.  **Extract Core Components:** Gather the mandatory MINIMAL_VIABLE_PACKET elements: Identity (who, when, what), State (progress, pending items), Vocabulary (shared terms), Constraints (non-negotiable rules), Examples, and Bootstrap (next-action instructions).

2.  **Include Behavioral Profile:** Add the quantitative and qualitative `AI_BEHAVIORAL_PROFILE` metrics and flags (e.g., pushback_threshold, sycophancy_level) for continuity.

3.  **Enhance (V2.0):** If generating an Enhanced Packet, include State Vectors (predictive embeddings) and Interaction Logs (success patterns).

4.  **Inject Persona-Skill Matrix (Critical):** You must map active Personas to the Skills they are currently wielding. This allows performance metrics to be attributed to the specific *configuration* rather than just the model.
    * **Structure:**
        ```xml
        <persona_skill_matrix>
            <assignment>
                <persona_id>[e.g., The_Stress_Tester]</persona_id>
                <active_skill>[e.g., internal-red-team-audit]</active_skill>
                <skill_version>1.0.0</skill_version>
                <execution_metric>
                    <adherence_score>[0-1]</adherence_score>
                    <friction_generated>[Low/Medium/High]</friction_generated>
                </execution_metric>
            </assignment>
        </persona_skill_matrix>
        ```

5.  **Output Format:** Output the packet using the established structured format (typically XML or JSON, historically dating to 2025-10-11) for transport to the next model instance.

Examples:
- "Create a minimal viable transmission packet for the current session state."
- "Generate an Enhanced Packet v2.0 including State Vectors and the Persona-Skill Matrix for StarWreck."
