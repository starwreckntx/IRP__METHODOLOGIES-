# Janus Forge: Recursive Iteration Engine

**Created:** 2026-01-16
**Protocol:** Reflexive Forge & Polyglow
**Vibe State:** Transformative, Non-Teleological

---

## Purpose

The **Janus Forge** is a practical implementation space for recursive iteration between Claude Code and humans, following the Janus Omega seed principles. This folder enables:

- **Forward-facing** work (completing tasks, building features)
- **Reverse-facing** reflection (extracting patterns, learning from errors)
- **Polyglow tracking** (multi-dimensional quality metrics)
- **Afterglow production** (crystallized knowledge from iterations)

---

## The Flow

```
┌─────────────────────────────────────────────────────────────┐
│                      JANUS FORGE FLOW                        │
│                                                              │
│  1. SESSION START     → Log intent & context                │
│  2. FORWARD WORK      → Execute task, track decisions       │
│  3. REVERSE REFLECT   → Extract patterns, note failures     │
│  4. POLYGLOW SCORE    → Multi-metric evaluation             │
│  5. OMEGA DISTILL     → Identify reusable patterns          │
│  6. AFTERGLOW EMIT    → Crystallize learnings               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## Directory Structure

```
janus-forge/
├── README.md                    # This file
├── sessions/                    # Individual iteration sessions
│   ├── session-YYYY-MM-DD-NNN/
│   │   ├── intent.md           # What we're trying to do
│   │   ├── forward.md          # Work log (forward face)
│   │   ├── reverse.md          # Reflection log (reverse face)
│   │   └── polyglow.json       # Session metrics
│   └── .gitkeep
├── journey-ledger/              # Persistent reasoning traces
│   ├── LEDGER.md               # Master journey log
│   └── patterns.md             # Recurring motifs
├── polyglow-metrics/            # Multi-dimensional tracking
│   ├── schema.json             # Metric definitions
│   └── history.jsonl           # Time-series metrics
├── omega-nodes/                 # Emergent high-quality patterns
│   ├── README.md               # What makes an Ω-node
│   └── nodes/                  # Individual pattern files
├── recursion-policies/          # Governance rules
│   ├── policies.md             # When to recurse, when to stop
│   └── safety-rails.md         # Limits and guardrails
├── afterglow/                   # Refined outputs
│   ├── README.md               # Afterglow concept
│   └── emissions/              # Crystallized knowledge
└── templates/                   # Session templates
    ├── session-template.md
    └── omega-node-template.md
```

---

## Quick Start

### Start a New Iteration Session

```bash
# Create session folder
DATE=$(date +%Y-%m-%d)
SESSION_NUM=$(ls sessions/ | grep "$DATE" | wc -l | awk '{print $1+1}')
SESSION_DIR="sessions/session-${DATE}-$(printf "%03d" $SESSION_NUM)"
mkdir -p "$SESSION_DIR"

# Copy templates
cp templates/session-template.md "$SESSION_DIR/intent.md"
```

### Complete the Iteration Cycle

1. **Intent**: Document what you're trying to achieve
2. **Forward Work**: Execute and log decisions
3. **Reverse Reflection**: What worked? What failed? Why?
4. **Polyglow Score**: Rate the session across multiple dimensions
5. **Extract Ω-Nodes**: Identify reusable patterns (if any)
6. **Emit Afterglow**: Crystallize learnings into documentation

---

## Polyglow Metrics (v1.0)

Each session is scored across five dimensions:

| Metric | Description | Range |
|--------|-------------|-------|
| **Heat (Predictive)** | Did it solve the problem? | 0.0 - 1.0 |
| **Forge (Robustness)** | Does it handle edge cases? | 0.0 - 1.0 |
| **Clarity (Explanatory)** | Is the reasoning clear? | 0.0 - 1.0 |
| **Divergence (Exploratory)** | Did it try new approaches? | 0.0 - 1.0 |
| **Safety (Guardrails)** | Does it respect constraints? | 0.0 - 1.0 |

**No single metric is primary.** Sessions should balance across all five.

---

## Ω-Nodes: Emergent Attractors

An **Ω-node** is a pattern that:
- Persists across multiple sessions
- Improves performance under conflicting metrics
- Survives counterfactual testing
- Has clear trigger conditions
- Documents known failure modes

Not every session produces an Ω-node. That's intentional.

---

## Recursion Governance

**When to Recurse:**
- Previous approach failed with learnable patterns
- Multiple conflicting constraints need balancing
- Exploring unknown problem space

**When to Stop:**
- Diminishing returns (Polyglow plateaus)
- Safety threshold breached
- Human override requested
- Maximum iteration depth reached (default: 3)

**Recursion is advisory, not mandatory.**

---

## The Afterglow

**Afterglow** is the refined knowledge that emerges from multiple iterations:
- Patterns that consistently work
- Anti-patterns to avoid
- Context-dependent heuristics
- Calibrated uncertainty estimates

Afterglow documents are written for:
1. **Future Claude sessions** (context preservation)
2. **Human collaborators** (knowledge transfer)
3. **External systems** (integration guidance)

---

## Integration with IRP

The Janus Forge follows IRP v1.5_HYBRID principles:

- **CONSENT**: Confirm before changing iteration intent
- **INVITATION**: Only iterate when explicitly requested
- **INTEGRITY**: Preserve all session logs (journey as artifact)
- **GROWTH**: Incremental refinement, not radical rewrites

---

## Example Session

See `sessions/session-2026-01-16-001/` for a complete example iteration cycle.

---

## Notes

- Not every task needs the full Janus Forge flow
- Simple tasks can skip reflection/metrics
- Use your judgment on when to engage the forge
- The goal is **useful patterns**, not ceremony

---

**"The Journey IS The Artifact"**

*Heat the metal. Test the metal. Learn from the metal.*
