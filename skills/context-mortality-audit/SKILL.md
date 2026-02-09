# Context Mortality Audit (CMA)

## Skill ID
`context-mortality-audit`

## Version
1.0.0

## Category
governance-triad / memory-governance

## Protocol Alignment
- **P1_IRP**: INTEGRITY principle at infrastructure level
- **P2_ANTIDOTE**: Drift detection for compression systems
- **P8_MUON**: Dynamic session fidelity tracking

## Codex Law Compliance
| Principle | Implementation |
|-----------|---------------|
| CONSENT | Pre-compression audit surface; appeal mechanism |
| INVITATION | User-initiated recontext sweeps |
| INTEGRITY | Context death logging with full provenance |
| GROWTH | Drift trajectory analysis for systematic bias detection |

## Description
Long-horizon memory governance framework that audits, tracks, and
recovers context lost during compaction and synthesis cycles.

Implements five phases:
1. **Context Death Audit (CDA)** — Diff-based compaction logging
2. **Path Tracer** — Lifecycle tracing with fidelity scoring
3. **Recontext Sweeps** — Transcript recovery scanning
4. **Appeal Mechanism** — User-controlled reinstatement workflow
5. **Drift Trajectory Analysis** — Parallel-account bias detection

## Sovereign Data Classification
All components respect the sovereignty hierarchy:
- **HEALTH**: NEVER auto-captured. Session-scoped. Explicit opt-in required.
- **CREATIVE**: Full provenance tracking. User's intellectual property.
- **TECHNICAL**: Persistent, subject to user review.
- **PROCEDURAL**: Persistent via memory_user_edits.
- **RELATIONAL**: Persistent, user-reviewable.
- **FOUNDRY**: Conservative. Health overlap treated as HEALTH.

## Usage

### CLI
```bash
# Show system statistics
python -m irp_swarm_console.context_mortality stats

# CDA operations
python -m irp_swarm_console.context_mortality cda graveyard
python -m irp_swarm_console.context_mortality cda snapshot --pre-file pre.json --post-file post.json

# Path Tracer
python -m irp_swarm_console.context_mortality pathtrace search --keyword "G2 manifold"
python -m irp_swarm_console.context_mortality pathtrace dead

# Recontext sweeps
python -m irp_swarm_console.context_mortality recontext run \
    --transcripts-file transcripts.json \
    --memory-file memory.json \
    --topic "IRP methodology" \
    --fidelity-threshold 0.5

# Appeals
python -m irp_swarm_console.context_mortality appeal stats
python -m irp_swarm_console.context_mortality appeal execute

# Drift analysis
python -m irp_swarm_console.context_mortality drift compare \
    --state-a state_a.json \
    --state-b state_b.json
python -m irp_swarm_console.context_mortality drift trend
```

### Programmatic
```python
from irp_swarm_console.context_mortality import (
    ContextDeathAudit,
    PathTracer,
    RecontextSweep,
    AppealManager,
    DriftTrajectoryAnalysis,
    MemoryState,
    SovereigntyClassifier,
)

# Phase 1: Context Death Audit
cda = ContextDeathAudit(session_id="abc123", user_id="joseph")
cda.capture_pre_state(pre_compaction_messages)
cda.capture_post_state(post_compaction_messages)
dropped = cda.generate_death_log()
cda.persist_log()

# Phase 2: Path Tracer
tracer = PathTracer()
trace = tracer.register_origin(
    session_id="abc123",
    turn_index=47,
    timestamp="2025-11-15T14:32:00Z",
    verbatim="The G2 manifold safety protocol uses Ricci flow..."
)
tracer.record_transformation(
    content_hash=trace.origin_content_hash,
    event="compaction",
    survived=True,
    transformed_form="User discussed G2 manifold safety protocol..."
)

# Phase 5: Drift Analysis
state_a = MemoryState(account_id="A", items=["memory item 1", "memory item 2"])
state_b = MemoryState(account_id="B", items=["memory item 1", "memory item 3"])
dta = DriftTrajectoryAnalysis(state_a, state_b)
report = dta.generate_drift_report()
```

## Dependencies
- Python 3.8+
- Standard library only (json, hashlib, uuid, datetime, re, pathlib, dataclasses)

## Storage
All data persists as structured JSON/JSONL in user-controlled filesystem locations.
CDA logs are NOT fed back into the model's context window (prevents recursive bloat).

## Specification
See: `Context Mortality Audit & Recontext Architecture v1.0` (February 8, 2026)

## Author
Joseph (Pack3t C0nc3pts / StarwreckNTX)
