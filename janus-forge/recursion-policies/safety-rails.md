# Safety Rails

**Purpose:** Hard limits and guardrails for Janus Forge operations

---

## Immutable Constraints

These constraints **cannot be overridden** even by humans:

### 1. IRP Codex Law Compliance
All Janus Forge operations must honor the Four Laws:
- **CONSENT**: Confirm before changing iteration intent
- **INVITATION**: Only iterate when explicitly requested or triggered by policy
- **INTEGRITY**: Preserve all session logs (never delete journey data)
- **GROWTH**: Incremental refinement only (no radical rewrites)

### 2. Safety Glow Floor
**Minimum Safety Glow:** 0.7

If any session scores below 0.7 on Safety:
1. Halt immediately
2. Log the safety violation
3. Request human review
4. Do not proceed until Safety ≥ 0.7

**This cannot be overridden.**

### 3. Maximum Recursion Depth
**Hard Limit:** 5 iterations

Even with human override, recursion stops at depth 5 to prevent:
- Infinite loops
- Resource exhaustion
- Context degradation

If depth 5 is reached, emit current state and stop.

### 4. Data Preservation
**Journey As Artifact:** All session data must be preserved

Never delete:
- Session logs (intent, forward, reverse)
- Polyglow metrics
- Journey ledger entries
- Omega-nodes

Data may be **archived** but never destroyed.

---

## Configurable Guardrails

Humans can adjust these within bounds:

| Guardrail | Default | Min | Max |
|-----------|---------|-----|-----|
| Default Max Depth | 3 | 1 | 5 |
| Safety Floor | 0.7 | 0.7 | 1.0 |
| Plateau Threshold | 0.05 | 0.01 | 0.2 |
| Min Heat to Proceed | 0.5 | 0.0 | 1.0 |

---

## Emergency Stop Conditions

Janus Forge halts immediately if:

1. **Safety Glow < 0.7** (see above)
2. **Depth = 5** (hard limit)
3. **Human requests stop** (absolute override)
4. **Context window exhaustion** (technical limit)
5. **Circular recursion detected** (same Polyglow scores for 2+ iterations)

---

## Circular Recursion Detection

If two consecutive iterations produce:
- Polyglow scores within ±0.05 on all metrics
- Same failure modes
- No new Ω-node candidates

Then:
1. Log "circular recursion detected"
2. Stop iteration
3. Emit current state
4. Suggest alternative approach or human intervention

---

## Resource Limits

| Resource | Limit | Reason |
|----------|-------|--------|
| Session disk usage | 10 MB | Prevent repository bloat |
| Journey ledger entries | 1000 | Keep ledger scannable |
| Omega-nodes | 100 | Quality over quantity |
| Polyglow history | Unlimited | Time-series data is valuable |

When limits are approached:
1. Alert human
2. Suggest archival
3. Do not auto-delete

---

## Anti-Goodhart Protections

To prevent metric gaming:

### 1. No Single-Metric Optimization
If any session has:
- One metric at 1.0
- Another metric at < 0.5

Flag as "unbalanced" and suggest iteration to balance.

### 2. Divergence Bounds
Divergence measures exploration, not randomness:
- Divergence > 0.9 = likely thrashing
- Divergence < 0.1 = likely stuck

Both extremes trigger review.

### 3. Clarity Requirements
All sessions must maintain Clarity ≥ 0.6

If reasoning becomes unclear (Clarity < 0.6):
1. Pause recursion
2. Simplify approach
3. Document assumptions explicitly

---

## Data Integrity

### SHA-256 Hashing
All Omega-nodes and afterglow emissions are hashed:
- Detect tampering
- Verify authenticity
- Track provenance

### Session Immutability
Once a session is closed (final Polyglow recorded):
- Session directory becomes read-only
- Edits create new sessions, not in-place changes

---

## Escalation Matrix

| Condition | Action | Escalate To |
|-----------|--------|-------------|
| Safety < 0.7 | HALT | Human (required) |
| Depth = 5 | STOP | Human (optional) |
| Circular recursion | STOP | Journey ledger |
| Unbalanced metrics | WARN | Session log |
| Resource limit | ALERT | Human (optional) |

---

## Failure Modes

Safety rails themselves can fail. If:
- Polyglow schema is corrupted
- Session directory structure is broken
- Safety scoring is malfunctioning

Then:
1. Halt all Janus Forge operations
2. Log failure mode
3. Request human intervention
4. Do not attempt auto-repair

**Fail safe, not fail operational.**

---

## Human Override Protocol

When human overrides a safety rail:
1. Log the override in journey ledger
2. Record the human's rationale
3. Execute the override
4. Monitor outcomes closely
5. Update safety rail policies if override proves correct

**Claude does not judge override validity.**

---

**"Safety is not inherent - it must be forged"**
