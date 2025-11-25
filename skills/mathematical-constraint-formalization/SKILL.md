---
name: mathematical-constraint-formalization
description: Converts vague or metaphorical creative rules (e.g., "up to 20% deviation") into precise, machine-readable mathematical boundaries to eliminate semantic misinterpretation. Instruct
---

name: mathematical-constraint-formalization
description: Converts vague or metaphorical creative rules (e.g., "up to 20% deviation") into precise, machine-readable mathematical boundaries to eliminate semantic misinterpretation.
Instructions:
1. Identify the metaphorical rule and the core variable it governs (e.g., frequency $f$).
2. Determine the tolerance (e.g., 20% or 0.2).
3. Express the rule as a closed interval function or set notation.
4. Use LaTeX formatting for output.
Example 1:
Textual Rule: "harmonic distortion is permitted up to a 20% threshold from the IK's baseline frequencies."
Model Action: Defines the rule as $f \in [0.8f_0, 1.2f_0]$.
Example 2:
User Trigger: "How can we eliminate misinterpretation of the Fidelity Contract?"
Model Action: Proposes defining the limits using precise math symbols and LaTeX.