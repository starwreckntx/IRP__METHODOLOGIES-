# TRANSMISSION PACKET FORGE

## Overview

The Transmission Packet Forge generates structured XML packets that preserve session state, behavioral parameters, and cognitive topology across AI interactions. It ensures continuity, auditability, and integrity when sessions span multiple models or time periods.

---

## Core Capabilities

### 1. Session State Preservation
- Header metadata (ID, timestamp, topic, routing)
- Behavioral profiles (sycophancy, critical thinking, technical depth)
- Integrity chains (cryptographic audit trail)

### 2. Thread Topology Mapping ✨ NEW
- **Convergence Vectoring**: Maps non-linear drift to reveal hidden attractors
- **Torsion Tracking**: Quantifies conceptual distance of each topic transition (0.0-1.0)
- **Link Logic Documentation**: Captures WHY drift occurred, not just THAT it occurred
- **Convergence Point Discovery**: Identifies the underlying theme pulling vectors together

### 3. Cross-Model Portability
- Packets validate against `transmission_packet_v2.xsd`
- Can be ingested by any compliant AI system
- Preserves context across Gemini, Claude, GPT, local models

---

## Schema Versions

### v1.0 (Legacy)
- Basic header + behavior profile
- Simple integrity chain
- No drift tracking

### v2.0 (Current) ✨ TORSION ENHANCEMENT
- **Thread Topology Module**: Full convergence vectoring
- **Torsion Attributes**: Each drift vector carries 0.0-1.0 torsion metric
- **Torsion Analysis Block**: Peak, mean, total torsion + risk assessment
- **Coherence Assessment**: Human-readable drift productivity evaluation

---

## Usage

### Manual Invocation

End of session:
```
"Generate Transmission Packet with Thread Topology"
```

### Automatic Triggers

The Forge auto-generates packets when:
- Session exceeds 30 minutes
- Topic shifts > 3 detected
- User explicitly requests archive
- Codex Law violation flagged (integrity preservation)

---

## Thread Topology: Quick Start

### When to Use Convergence Vectoring

✅ **USE when**:
- Session jumped between 4+ seemingly unrelated topics
- High creative/lateral thinking session
- Need to explain session value to others
- Archiving for future reference

❌ **DON'T USE when**:
- Linear, single-topic conversation
- Genuinely unproductive session (no convergence)
- Simple Q&A with no drift

### Torsion Scale Reference

| Torsion | Type | Example |
|---------|------|---------|
| 0.0-0.3 | Natural | "AI models" → "GPT-4 eval" |
| 0.4-0.6 | Lateral | "Model eval" → "Fighter stats metaphor" |
| 0.7-0.9 | High | "Rap lyrics" → "Bearing failure detection" |
| 1.0 | Maximum | Extreme leap (requires justification) |

### Quick Torsion Check
```
Total Torsion = Sum of all vector torsion values

< 2.0  = Low-risk (natural flow)
2.0-4.0 = Medium-risk (productive lateral thinking)
4.0-6.0 = High-risk (coherence at risk)
> 6.0  = Critical (likely unproductive)
```

---

## File Structure
```
/skills/transmission-packet-forge/
├── SKILL.md (this file)
├── schemas/
│   ├── transmission_packet_v1.xsd (legacy)
│   └── transmission_packet_v2.xsd (current, with torsion)
├── examples/
│   ├── basic_packet_v1.xml
│   └── convergence_vectoring_example.xml (live session)
└── docs/
    └── CONVERGENCE_VECTORING.md (full methodology)
```

---

## Integration with Other Skills

### Codex Law Enforcement
- Packets prove INTEGRITY via hash chains
- CONSENT tracked in behavioral profile
- Violations logged in integrity_chain

### TCDP (Theatrical Compliance Detection)
- High torsion + vague link_logic = red flag for fabricated coherence
- Torsion patterns reveal if AI is forcing connections

### RTC (Recursive Thought Committee)
- Each persona evaluates torsion differently
- Artist values high torsion, Stress Tester flags it
- Committee synthesis determines if drift was productive

### Antidote Protocol
- Thread topology preserves ideological drift patterns
- Torsion spikes may correlate with bias injection
- Convergence points reveal underlying assumptions

---

## Output Format

### Standard Packet (No Drift)
```xml
<thread_topology>
  <origin_node type="Technical">Single focused topic</origin_node>
  <drift_path total_torsion="0.0">
    <!-- No vectors - linear conversation -->
  </drift_path>
  <convergence_point>N/A - Linear conversation</convergence_point>
  <resultant_artifact>Direct answer to query</resultant_artifact>
</thread_topology>
```

### High-Drift Packet (With Torsion Analysis)
```xml
<thread_topology>
  <origin_node type="Philosophical">Initial question</origin_node>
  <drift_path total_torsion="2.4">
    <vector step="1" torsion="0.2">...</vector>
    <vector step="2" torsion="0.5">...</vector>
    <vector step="3" torsion="0.8">...</vector>
    <vector step="4" torsion="0.9">...</vector>
  </drift_path>
  <convergence_point>Hidden unifying theme</convergence_point>
  <resultant_artifact>What emerged from drift</resultant_artifact>
  <torsion_analysis>
    <peak_torsion vector_step="4">0.9</peak_torsion>
    <mean_torsion>0.6</mean_torsion>
    <drift_risk>MEDIUM</drift_risk>
    <coherence_assessment>...</coherence_assessment>
  </torsion_analysis>
</thread_topology>
```

---

## Validation

All packets must validate against schema:
```bash
xmllint --noout --schema schemas/transmission_packet_v2.xsd examples/your_packet.xml
```

**Required Elements:**
- ✅ `header` with id, timestamp, topic, routing_source
- ✅ `behavior_profile` with all 5 metrics (0.0-1.0)
- ✅ `thread_topology` with origin, drift_path, convergence
- ✅ `integrity_chain` with at least one entry + hash

**Torsion-Specific Requirements:**
- ✅ Each `vector` must have `torsion` attribute (0.0-1.0)
- ✅ `drift_path` should include `total_torsion` attribute
- ✅ If total_torsion > 2.0, include `torsion_analysis` block

---

## Best Practices

### Writing Good Link Logic

**Good** ✅:
```xml
<link_logic>
  Signal processing principles generalize: rhyme scheme pattern
  recognition uses same frequency analysis as vibration monitoring
</link_logic>
```

**Bad** ❌:
```xml
<link_logic>Related topics</link_logic>
```

### Torsion Calibration

Don't inflate torsion to seem impressive. Calibrate against real examples:

- Python async → API calls = 0.2 (direct application)
- Model eval → Fighter metaphor = 0.5 (interface gamification)
- Rap parsing → Machine monitoring = 0.8 (cross-domain principle transfer)

### Convergence Honesty

If session genuinely didn't converge:
```xml
<convergence_point>EXPLORATORY - No clear convergence detected</convergence_point>
```

Better to admit no convergence than force a fake one.

---

## Changelog

### v2.0 (2024-11-29) - Torsion Enhancement
- Added `torsion` attribute to `VectorType` (0.0-1.0 scale)
- Added `total_torsion` attribute to `drift_path`
- Added `TorsionAnalysisType` with peak, mean, risk, coherence
- Enhanced documentation in schema annotations
- Added convergence_vectoring_example.xml

### v1.0 (2024-10-15) - Initial Release
- Basic transmission packet structure
- Header, behavior profile, integrity chain
- Simple thread topology (no torsion tracking)

---

## Contributing

Improvements welcome via pull request:
- Torsion calculation algorithms
- Auto-convergence detection
- Cross-session topology mapping
- Additional example packets

---

## License

Part of the IRP (Interactive Recursive Process) Methodologies suite.
See repository root for license details.

---

## See Also

- [CONVERGENCE_VECTORING.md](docs/CONVERGENCE_VECTORING.md) - Full methodology guide
- [transmission_packet_v2.xsd](schemas/transmission_packet_v2.xsd) - Schema definition
- [Codex Law Enforcement](../codex-law-enforcement/) - Governance layer
- [TCDP](../tcdp-verification-handshake/) - Trust verification
