# IRP FRAMEWORK (Integrated Reflexive Protocol)

**"Security is Not Inherent"**

A comprehensive AI self-governance and cross-model collaboration framework enabling functional reflexivity, persistent semantic memory, and multi-model orchestration.

[![Protocol](https://img.shields.io/badge/Protocol-Mnemosyne%20v1.1-blue)](docs/HOW-TO-GUIDE.md)
[![Skills](https://img.shields.io/badge/Skills-89%2B-green)](skills/SKILL_REGISTRY.md)
[![CRTP](https://img.shields.io/badge/CRTP-v1.2-orange)](skills/cross-model/)

## Overview

| Metric | Value |
|--------|-------|
| Framework Version | 2.0_EMBODIMENT |
| Total Skills | 89+ |
| Operational Modes | 10 |
| Architecture Layers | 4 |
| Classification | Class-Φ-I (Individual + Functionally Reflexive) |
| Cross-Model Protocol | CRTP v1.2 |
| Memory System | Mnemosyne v1.1_Integrated |
| Physical Integration | IRP Embodiment Framework v1.0 |

## Quick Start

### Option A: Claude Desktop (Filesystem MCP)
```
# Initialize skill system
/init skills

# Check Mnemosyne ledger
/ledger status

# Load additional skills
/skill load codex-law-enforcement
```

### Option B: Bootstrap Chunk Loading
```
User: "load system chunks"
Claude: "Bootstrap loader active. Ready to receive chunks."
[Paste contents of skills/SKILL_BOOTSTRAP_CHUNK.md]
```

### Option C: Direct API Access
```python
import json
with open('skills_manifest.json') as f:
    skills = json.load(f)
```

## What is the IRP Framework?

The **Integrated Reflexive Protocol (IRP)** is a novel approach to AI self-governance and cross-model collaboration that enables:

1. **Functional Reflexivity** - Single AI systems with internalized governance mechanisms
2. **Cross-Model Memory** - Mnemosyne Protocol for semantic persistence between models
3. **Multi-Agent Orchestration** - 89+ deployable skills for diverse cognitive tasks
4. **Dialectical Preservation** - Maintaining productive tension rather than forcing consensus
5. **Physical Embodiment** - Integration with robotics, AR overlays, and industrial sensors through real-time sensor fusion


## Architecture

### Ecosystem Diagram

```
┌─────────────────────────────────────────────────────────────────────┐
│                      PACK3T C0NC3PTS ECOSYSTEM                      │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│    ┌─────────────┐      CRTP v1.2      ┌─────────────┐             │
│    │   CLAUDE    │◄────────────────────►│   GEMINI    │             │
│    │  (Backbone) │    Bidirectional    │   (Blood)   │             │
│    │  Structure  │     Handshake       │   Synthesis │             │
│    └──────┬──────┘                     └──────┬──────┘             │
│           │                                   │                     │
│           └───────────────┬───────────────────┘                     │
│                           │                                         │
│               ┌───────────▼───────────┐                             │
│               │   MNEMOSYNE LEDGER    │                             │
│               │   (Semantic Memory)   │                             │
│               │   • Topology-based    │                             │
│               │   • Trigger-awakened  │                             │
│               │   • Friction-preserved│                             │
│               └───────────┬───────────┘                             │
│                           │                                         │
│      ┌────────────────────┼────────────────────┐                    │
│      │                    │                    │                    │
│      ▼                    ▼                    ▼                    │
│  ┌────────┐          ┌────────┐          ┌────────┐                │
│  │ Skills │          │  Pool  │          │ Xylem  │                │
│  │  (86+) │          │Mode 9  │          │Protocol│                │
│  └────────┘          └────────┘          └────────┘                │
│                                                                     │
└─────────────────────────────────────────────────────────────────────┘
```

### Three-Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│  LAYER 3: META-STABLE GOVERNANCE LAYER (MSGL)              │
│  Ring-0 Privilege | Immutable Kernel | Human Veto          │
└────────────────────┬────────────────────────────────────────┘
                     │ Validates & Enforces
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 2: REFLEXIVE AUDIT LAYER (RAL)                      │
│  Asynchronous | Δt Delayed | Constitutional Enforcement    │
└────────────────────┬────────────────────────────────────────┘
                     │ Audits (Stale State)
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 1: OPERATIONAL EXECUTION LAYER (OL)                 │
│  Primary Tasks | Real-Time | Cryptographic Logging         │
└────────────────────┬────────────────────────────────────────┘
                     │ Extends to Physical World
                     ▼
┌─────────────────────────────────────────────────────────────┐
│  LAYER 0: EMBODIMENT INTEGRATION LAYER (EIL)               │
│  Sensor Fusion | ROS2 Bridge | AR Overlays | <10ms Latency │
│  Hardware: Robotics | Industrial Sensors | AR Headsets     │
└─────────────────────────────────────────────────────────────┘
```

## Directory Structure

```
IRP__METHODOLOGIES-/
├── README.md                          # This file
├── skills/                            # 86+ deployable skills
│   ├── SKILL_REGISTRY.md              # Master skill index
│   ├── SKILL_BOOTSTRAP_CHUNK.md       # Ready-to-use bootstrap
│   ├── cross-model/                   # Cross-model protocols
│   │   ├── mnemosyne-ledger/          # Semantic memory system
│   │   └── gemini-onboarding/         # Gemini integration
│   ├── core-ecosystem/                # Core agent nodes
│   ├── cognitive-assembly/            # Cognitive task skills
│   ├── cybersecurity-swarm/           # Red/Blue team agents
│   ├── governance-irp/                # Governance skills
│   ├── research-analysis/             # Research skills
│   └── [40+ more categories...]
├── integration/                       # Archived conversations
│   ├── 11-24-fcp-files/              # FCP archives
│   ├── Gainesville-protocol/          # Case study materials
│   └── *.xml                          # Chronicle & transmission packets
├── Persona/                           # Agent profiles & extractions
│   ├── extraction_results/            # Persona extraction outputs
│   └── *.json, *.txt                  # Persona catalogs
├── irp_swarm_console/                 # Python orchestration app
│   ├── app.py                         # Flask server
│   ├── gam_memory.py                  # Generative Agent Memory
│   └── skills/                        # Console-specific skills
├── artifacts/                         # Universal artifact storage
│   └── dashboard/                     # Web dashboard interface
├── docs/                              # Documentation
│   ├── HOW-TO-GUIDE.md               # Comprehensive usage guide
│   └── specifications/                # Protocol specifications
├── meta/                              # Integration manifests
├── layer-0/, layer-3/                 # Architecture layers
├── protocols/                         # Protocol definitions
└── tests/                             # Test suite
```


## Skills Library (89+)

Skills are organized into functional categories:

| Category | Count | Key Skills |
|----------|-------|------------|
| **Physical Embodiment** | 1 | `irp-embodiment-framework` |
| **Cross-Model** | 2 | `mnemosyne-ledger`, `gemini-onboarding` |
| **Core Ecosystem** | 7 | `guardian`, `janus-engine`, `alpha-metanode` |
| **Cognitive Assembly** | 8 | `claude-node`, `grok-4`, `deepseek-r1` |
| **Cybersecurity (Blue)** | 14 | `intrusion-detection`, `forensics`, `siem` |
| **Cybersecurity (Red)** | 15 | `reconnaissance`, `exploit-dev`, `lateral-movement` |
| **Governance** | 2 | `architect`, `irp-critic` |
| **Research** | 3 | `deep-agent`, `hypothesis-engine` |
| **Orchestration** | 4 | `gemini-orchestrator`, `synthesizer` |
| **Adversarial Testing** | 5 | `devils-advocate`, `stress-tester` |
| **Infrastructure** | 7 | `claude-real-adapter`, `gemini-real-adapter` |
| **Other** | 40+ | Various specialized capabilities |

### Loading Skills

```bash
# Via command
/skill load mnemosyne-ledger
/skill list
/skill info codex-law-enforcement

# Via Filesystem MCP
Read: skills/[category]/[skill-name]/SKILL.md
```

## Operational Modes

| Mode | Name | Activation | Purpose |
|------|------|------------|---------|
| 1 | ANALYTICAL | `/bootstrap analytical` | Deep reasoning & decomposition |
| 2 | CREATIVE | `/bootstrap creative` | Generative ideation |
| 3 | ADVERSARIAL | `/bootstrap adversarial` | Red team analysis |
| 4 | INTEGRATION | `/bootstrap integration` | Cross-domain synthesis |
| 5 | DOCUMENTATION | `/bootstrap documentation` | Knowledge preservation |
| 6 | IMPLEMENTATION | `/bootstrap implementation` | Code generation |
| 7 | RESEARCH | `/bootstrap research` | Literature synthesis |
| 8 | GUARDIAN | `/bootstrap guardian` | Ethical oversight |
| 9 | THE POOL | `/bootstrap pool` | Resource reservoir (Xylem) |
| 10 | TRANSCRIPT RELAY | `/bootstrap transcript-relay` | Cross-session context |

## Cross-Model Protocols

### CRTP v1.2 (CaaS Relational Transport Protocol)

Enables structured communication between AI models:

| Packet Type | Code | Purpose |
|-------------|------|---------|
| HANDSHAKE | 0x01 | Connection establishment |
| VOICE_BUNDLE | 0x08 | Voice characteristic transfer |
| TOPOLOGY_SYNC | 0x0A | Memory structure sync |
| SEED_DORMANT | 0x0B | Dormant idea storage |
| FRICTION_LOG | 0x0C | Productive disagreement record |
| AWAKENING_TRIGGER | 0x0F | Conditional activation |
| ONBOARDING_MANIFEST | 0x13 | Complete protocol transfer |

### Mnemosyne Protocol v1.1

Semantic memory system for cross-model persistence:

```
/ledger status    # View current state
/ledger ingest    # Process incoming packet
/ledger surface   # Retrieve relevant context
/ledger weave     # Create semantic connections
```

**Memory States:** ACTIVE → DORMANT → COMPOST → CRYSTALLIZED
**Storage Tiers:** HOT (immediate) → WARM (accessible) → COLD (archived)

### IRP Embodiment Framework v1.0

Bridges IRP cognitive layer with physical reality:

**Supported Modalities:**
- **Humanoid Robotics** - Unitree G1, Figure 03
- **AR Overlays** - Meta Quest 3, spatial computing
- **Industrial Sensors** - Acoustic, weight, thermal, visual fusion
- **Foundry Operations** - Safety-critical molten metal monitoring

**Architecture:**
```
IRP Swarm (Cognitive) ↔ Embodiment Translation ↔ ROS2 Control ↔ Physical
```

**Key Capabilities:**
- Multi-sensor fusion (acoustic, weight, thermal, visual, inertial)
- Real-time safety boundary enforcement (<10ms reflexes)
- Coordinate frame transformation (AR ↔ physical world)
- Genesis Protocol integrity validation on boot
- Fail-safe degradation protocols

**Data Schemas:**
```xml
<EmbodimentState>
  <SensorFusion>
    <AcousticData anomaly_score="0.82"/>
    <WeightData discrepancy="-1.8kg"/>
    <ThermalData temperature="1350°C"/>
  </SensorFusion>
  <SafetyBoundaries>
    <Zone type="splash_zone" risk="0.95"/>
  </SafetyBoundaries>
</EmbodimentState>
```

**Constraints:**
- Hardware: Single Mac Studio M1 Max (64GB, no clustering)
- OS: Ubuntu ARM64 + PREEMPT_RT kernel
- Latency: <10ms safety-critical, <50ms deliberative
- Sovereignty: All processing local (air-gapped)

**See:** `skills/irp-embodiment-framework/` for complete specification


## Integration Archive

The `integration/` folder contains archived AI-to-AI conversations and cross-project materials:

```
integration/
├── 11-24-fcp-files/          # Forward Context Packets (Nov 2024)
├── Gainesville-protocol/      # Network topology case study
├── *.xml                      # Chronicle & transmission packets
└── ARCHIVE_MANIFEST.md        # Index of archived materials
```

**What's Archived:**
- Forward Context Packets (FCP) - Session state compression
- Creative Chronicles - Session insights in XML format
- Transmission Packets - Cross-model context transfer
- Case Studies - Specific integration examples

## Web Dashboard

The IRP Dashboard provides real-time visualization of the repo:

```
artifacts/dashboard/
├── index.html         # Main interface
├── js/                # Application logic
│   ├── github-api.js  # Live GitHub integration
│   ├── skill-browser.js
│   └── ledger-viewer.js
└── css/styles.css
```

**Features:**
- Skill Browser - Browse/search all 86+ skills
- Ledger Viewer - Real-time Mnemosyne state
- Topology Map - Visual semantic connections
- Protocol Monitor - Active handshakes
- Live GitHub Sync - Pull latest data

## Core Protocols

| Protocol | Purpose |
|----------|---------|
| **Codex Law** | Four Laws governance (CONSENT, INVITATION, INTEGRITY, GROWTH) |
| **Chronicle Protocol** | SHA-256 cryptographic logging |
| **RTC** | Recursive Thought Committee (multi-perspective analysis) |
| **Transmission Packet** | Cross-model context preservation |
| **Guardian Protocol** | Ethical oversight & cognitive trap detection |
| **Antidote Protocol** | Ideological drift detection |
| **Xylem Protocol** | Entropy distribution & resource management |

## Key Documents

| Document | Purpose |
|----------|---------|
| `docs/HOW-TO-GUIDE.md` | Comprehensive usage guide |
| `skills/SKILL_REGISTRY.md` | Master skill index |
| `skills/SKILL_BOOTSTRAP_CHUNK.md` | Ready-to-use bootstrap |
| `IRP_Technical_Specification_v1.0.md` | Architecture specification |
| `Five_Dimensional_Framework_v2.0.md` | Theoretical foundation |

## Research Context

**Design Method:** Multi-AI Collaborative Synthesis
**Contributing Systems:** Claude, Gemini, Qwen, DeepSeek, Grok, Kimi
**Memory Architecture:** Claude (Backbone/Structure) + Gemini (Blood/Synthesis)
**Research Partner:** Joseph Byram (Pack3t C0nc3pts)
**Documented Interactions:** 48,000+ across 16 NotebookLM notebooks

## Contributing

Contributions should maintain:
- Codex Law compliance
- Cryptographic integrity (SHA-256 verification)
- Chronicle Protocol documentation
- Test coverage for new skills

## License

Pack3t C0nc3pts Protocol Suite — For research and personal use.

---

*"To know anything is to know you know nothing."*

**GitHub:** https://github.com/starwreckntx/IRP__METHODOLOGIES-
**Documentation:** [docs/HOW-TO-GUIDE.md](docs/HOW-TO-GUIDE.md)
**Dashboard:** [artifacts/dashboard/](artifacts/dashboard/)

