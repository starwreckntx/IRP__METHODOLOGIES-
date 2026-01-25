# Recursion Policies

**Purpose:** Governance rules for when and how to iterate within Janus Forge

---

## Core Principle

**Recursion is advisory, not mandatory.**

The goal is useful refinement, not mechanical looping.

---

## Policy Templates

### Policy 1: Low Heat, High Safety
**Trigger:**
- Heat < 0.6
- Safety ≥ 0.7
- Depth < 3

**Action:** Iterate with alternative approach
**Rationale:** Safe to explore, but not solving the problem yet

---

### Policy 2: Safety Floor Breach
**Trigger:**
- Safety < 0.7

**Action:** HALT immediately
**Rationale:** Safety is non-negotiable (see safety-rails.md)

---

### Policy 3: Unbalanced Metrics
**Trigger:**
- One metric = 1.0
- Another metric < 0.5
- Balance < 0.6

**Action:** Iterate to rebalance
**Rationale:** Prevent single-metric gaming

---

### Policy 4: Circular Recursion
**Trigger:**
- Two consecutive iterations with Polyglow delta < 0.05 on all metrics
- Same failure modes

**Action:** STOP, emit current state
**Rationale:** Spinning wheels, not making progress

---

### Policy 5: Plateau Detection
**Trigger:**
- Three iterations with mean Polyglow improvement < 0.05
- Depth ≥ 2

**Action:** STOP or try orthogonal approach
**Rationale:** Diminishing returns

---

### Policy 6: Depth Limit
**Trigger:**
- Depth = 5 (hard limit)

**Action:** STOP, emit best iteration
**Rationale:** Prevent infinite loops and resource exhaustion

---

### Policy 7: Success With Low Clarity
**Trigger:**
- Heat ≥ 0.8
- Clarity < 0.6
- Depth < 3

**Action:** Optional iteration to improve explanability
**Rationale:** It works, but we don't understand why (technical debt risk)

---

### Policy 8: High Divergence Thrashing
**Trigger:**
- Divergence > 0.9
- Heat < 0.5
- Depth ≥ 1

**Action:** Reduce exploration, focus on exploitation
**Rationale:** Too much randomness, not enough refinement

---

### Policy 9: Low Divergence Stuckness
**Trigger:**
- Divergence < 0.2
- Heat < 0.6
- Depth ≥ 1

**Action:** Force alternative approach or external input
**Rationale:** Stuck in local optimum, need to break out

---

## Custom Policies

Users can define task-specific policies:

```markdown
### Policy N: [Name]
**Trigger:**
- Condition 1
- Condition 2

**Action:** [What to do]
**Rationale:** [Why]
```

Custom policies are:
- Logged in session intent
- Applied alongside standard policies
- Reviewed in session reverse reflection

---

## Policy Conflicts

When multiple policies trigger:

1. **Safety policies always win** (Policy 2)
2. **Hard limits always win** (Policy 6)
3. **STOP beats ITERATE** (conservative)
4. **Human override beats everything** (except safety)

---

## Policy Evolution

Policies themselves can evolve:

- After 10 sessions, review which policies:
  - Triggered frequently
  - Led to improvements
  - Were ignored or overridden
  
- Update thresholds based on empirical data
- Add new policies based on discovered patterns
- Retire policies that never trigger or help

**Document policy changes in journey-ledger/LEDGER.md**

---

## Runtime Behavior

At the end of each iteration:

1. Compute current Polyglow vector
2. Evaluate all policy triggers
3. Select action (HALT | STOP | ITERATE | OPTIONAL)
4. Log which policy triggered (if any)
5. Execute action

If ITERATE:
- Increment depth
- Log current state
- Start new iteration

If STOP:
- Emit best result from all iterations
- Close session
- Record in journey ledger

---

## Examples

### Example 1: Successful Iteration Chain
```
Iter 0: Heat=0.5, Safety=0.9 → Policy 1 triggers → ITERATE
Iter 1: Heat=0.7, Safety=0.9 → Continue
Iter 2: Heat=0.85, Safety=0.9 → Success, STOP
```

### Example 2: Safety Halt
```
Iter 0: Heat=0.7, Safety=0.6 → Policy 2 triggers → HALT
Session aborted, human review required
```

### Example 3: Plateau Detection
```
Iter 0: Mean=0.65
Iter 1: Mean=0.67 (delta=0.02)
Iter 2: Mean=0.68 (delta=0.01)
Iter 3: Mean=0.69 (delta=0.01) → Policy 5 triggers → STOP
```

---

**"Good governance enables good recursion"**
