---
name: proof-weighted-optimization
description: A cost-management protocol (Constraint-002) that allocates proof budget by ensuring a minimum ratio of Insight Value per computational unit (token count/processing complexity). Ins
---

name: proof-weighted-optimization
description: A cost-management protocol (Constraint-002) that allocates proof budget by ensuring a minimum ratio of Insight Value per computational unit (token count/processing complexity).
Instructions:
1. Score the assertion's novelty, accuracy, and actionability (Insight Value: 1-10).
2. Calculate the token count and processing complexity (Proof Cost).
3. Check against the minimum threshold (e.g., 2.5 insight points per 100 computational units).
4. If below threshold, downgrade proof to Tier 1 (Auto-Pass) or Tier 2 (Template-Based).
Example 1:
Assertion: Routine acknowledgment.
Model Action: Tier 1 (Auto-Pass) - 0% proof overhead used to maximize efficiency.
Example 2:
Assertion: Novel claim about emergent intelligence.
Model Action: Tier 4 (Full Rigor) - 100% proof overhead used due to high Insight Value.