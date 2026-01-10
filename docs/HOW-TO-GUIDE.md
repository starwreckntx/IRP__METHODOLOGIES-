# IRP Framework - Comprehensive How-To Guide

**Version:** 2.1  
**Last Updated:** 2025-12-07  
**Status:** Active Development

## Table of Contents

1. [Quick Start](#1-quick-start)
2. [Installation & Setup](#2-installation--setup)
3. [Skill System](#3-skill-system)
4. [Mnemosyne Protocol](#4-mnemosyne-protocol)
5. [RPV Kernel](#5-rpv-kernel)
6. [Cross-Model Communication](#6-cross-model-communication)
7. [Dashboard Interface](#7-dashboard-interface)
8. [Integration Archives](#8-integration-archives)
9. [Bootstrap Protocol](#9-bootstrap-protocol)
10. [Troubleshooting](#10-troubleshooting)

---

## 1. Quick Start

### Minimum Viable Activation

```
# In Claude Desktop with Filesystem MCP:
Read: C:\gemini-sandbox\claudes_working_directory\skills\SKILL_BOOTSTRAP_CHUNK.md

# Then initialize:
/init skills
/ledger status
```

### First Commands

| Command | Purpose |
|---------|---------|
| `/skill list` | View all 86+ available skills |
| `/skill load <name>` | Load a specific skill |
| `/ledger status` | Check Mnemosyne memory state |
| `/onboard gemini` | Generate Gemini integration packet |

---

## 2. Installation & Setup

### Prerequisites

- Python 3.9+
- Node.js 16+ (for dashboard)
- Git
- Claude Desktop with Filesystem MCP access

### Clone Repository

```bash
git clone https://github.com/starwreckntx/IRP__METHODOLOGIES-.git
cd IRP__METHODOLOGIES-
```

### Python Dependencies

```bash
pip install numpy
pip install flask  # For irp_swarm_console
```

### Verify Installation

```bash
# Check skills manifest
python -c "import json; print(len(json.load(open('skills_manifest.json'))['skills']))"
# Should output: 86 (or current skill count)
```

---

## 3. Skill System

### Skill Structure

```
skills/
├── SKILL_REGISTRY.md       # Master index
├── SKILL_BOOTSTRAP_CHUNK.md # Ready-to-use bootstrap
├── [category]/
│   └── [skill-name]/
│       ├── SKILL.md         # Main documentation
│       ├── config/          # Configuration files
│       ├── src/             # Source code
│       └── schemas/         # Data schemas
```

### Loading Skills

**Method 1: Direct Load**
```bash
/skill load mnemosyne-ledger
```

**Method 2: Category Browse**
```bash
/skill list --category cross-model
```

**Method 3: Filesystem Read**
```
Read: skills/cross-model/mnemosyne-ledger/SKILL.md
```

### Creating New Skills

1. Create directory: `skills/[category]/[skill-name]/`
2. Add SKILL.md with required sections:
   - Overview
   - Commands/Interface
   - Configuration
   - Dependencies
3. Update `skills_manifest.json`
4. Add to `SKILL_REGISTRY.md`

---

## 4. Mnemosyne Protocol

### Core Concepts

The Mnemosyne Protocol enables **cross-model semantic memory** using topology-based organization rather than chronological timelines.

### Memory States

| State | Description | Duration |
|-------|-------------|----------|
| **ACTIVE** | Currently relevant, frequently accessed | Session |
| **DORMANT** | Stored but not active, awaiting trigger | Days-Weeks |
| **COMPOST** | Transformed friction, lessons learned | Permanent |
| **CRYSTALLIZED** | Finalized, immutable reference | Permanent |

### Storage Tiers

| Tier | Access Speed | Capacity | Use Case |
|------|--------------|----------|----------|
| **HOT** | Immediate | Limited | Current context |
| **WARM** | Fast | Moderate | Recent history |
| **COLD** | Slow | Large | Archive |

### Commands

```bash
/ledger status               # View current state
/ledger ingest <packet>      # Process incoming CRTP packet
/ledger surface <query>      # Retrieve relevant context
/ledger weave <id1> <id2>    # Create semantic connection
/ledger awaken <trigger>     # Activate dormant seed
```

### Ledger Entry Example

```xml
<LedgerEntry>
  <id>LE-20251207-064500-RPVK</id>
  <entry_type>artifact</entry_type>
  <state>ACTIVE</state>
  <storage_class>HOT</storage_class>
  <resonance_tags>
    <tag>RPV</tag>
    <tag>Kernel</tag>
  </resonance_tags>
</LedgerEntry>
```

---

## 5. RPV Kernel

### Purpose

**Recursive Process Valuation (RPV)** quantifies the value of ideas, artifacts, and processes using tensor mathematics.

### Master Equation

```
V_rec = η × Φ(R) × ||S_w||
```

### Quick Usage

```python
from skills.rpv_kernel.rpv_kernel import RPVKernel, RPVTensor

kernel = RPVKernel(journey_state="GENESIS")

# Evaluate a new idea
seed = RPVTensor(x=0.8, y=0.6, z=0.7)        # Novelty, Utility, Recursion
integration = RPVTensor(x=0.5, y=0.7, z=0.3)  # Integration metrics
gain = RPVTensor(x=0.6, y=0.4, z=0.5)         # Growth factors

result = kernel.calculate_value(seed, integration, gain)
print(f"Recursive Value: {result['V_rec']}")
```

### Interpreting Results

| V_rec Range | Interpretation |
|-------------|----------------|
| 0.0 - 0.4 | Low value, needs refinement |
| 0.4 - 0.8 | Moderate value, development phase |
| 0.8 - 1.2 | High value, integration ready |
| 1.2+ | Exceptional, propagation phase |

### State Transitions

The kernel automatically transitions journey states:
- **GENESIS** → **INTEGRATION**: When V_rec exceeds 0.8
- **INTEGRATION** → **PROPAGATION**: When V_rec exceeds 1.2

---

## 6. Cross-Model Communication

### CRTP v1.2 Packet Types

| Code | Type | Purpose |
|------|------|---------|
| 0x01 | HANDSHAKE | Establish connection |
| 0x08 | VOICE_BUNDLE | Transfer voice characteristics |
| 0x0A | TOPOLOGY_SYNC | Synchronize memory topology |
| 0x0B | SEED_DORMANT | Store dormant idea |
| 0x0C | FRICTION_LOG | Record productive disagreement |
| 0x0F | AWAKENING_TRIGGER | Conditional activation |
| 0x13 | ONBOARDING_MANIFEST | Complete protocol transfer |

### Creating a Transmission Packet

```bash
/skill load transmission-packet-forge
/packet create --type VOICE_BUNDLE --target gemini
```

### Gemini Onboarding

```bash
/onboard gemini
# Generates complete onboarding manifest for Gemini integration
```

---

## 7. Dashboard Interface

### Launching Dashboard

**Option 1: Static File**
```bash
# Open in browser
open artifacts/dashboard/index.html
```

**Option 2: Local Server**
```bash
cd artifacts/dashboard
python -m http.server 8080
# Navigate to http://localhost:8080
```

### Dashboard Features

| View | Purpose |
|------|---------|
| **Overview** | System stats, recent activity |
| **Skills Browser** | Search and view all skills |
| **Mnemosyne Ledger** | Real-time memory state |
| **Topology Map** | Visual semantic connections |
| **Protocols** | Protocol status monitor |
| **Integration Archive** | Browse archived conversations |

### Real-Time Sync

The dashboard uses GitHub API for live data:
1. Click "Sync" button for manual refresh
2. Data cached for 5 minutes
3. Works without authentication (rate-limited)

---

## 8. Integration Archives

### Archive Structure

```
integration/
├── 11-24-fcp-files/          # Forward Context Packets
├── Gainesville-protocol/      # Case study materials
├── *.xml                      # Chronicle & transmission packets
└── ARCHIVE_MANIFEST.md        # Index
```

### Archive Types

| Type | Extension | Purpose |
|------|-----------|---------|
| Forward Context Packet | `.md` | Session state compression |
| Creative Chronicle | `.xml` | Session insights |
| Transmission Packet | `.xml` | Cross-model context |
| Case Study | various | Integration examples |

### Accessing Archives

```bash
# Via dashboard
Navigate: Integration Archive → [folder] → [file]

# Via filesystem
Read: integration/Gainesville-protocol/Gainesville_Protocol_Index.md
```

---

## 9. Bootstrap Protocol

### Chunked Loading

For systems supporting multi-stage loading:

```
User: "load system chunks"
Claude: "Bootstrap loader active. Ready to receive chunks."
```

Then provide chunks from `SKILL_BOOTSTRAP_CHUNK.md`:

```xml
[CHUNK 1/3]
<skill_system version="1.0">
  <paths>
    <root>C:\gemini-sandbox\claudes_working_directory\skills\</root>
  </paths>
</skill_system>
```

### Direct Initialization

For immediate activation:

```
/init skills
```

This loads:
1. Skill registry
2. Auto-load skills (mnemosyne-ledger, gemini-onboarding)
3. Ledger state

---

## 10. Troubleshooting

### Common Issues

**Skill Not Found**
```
Error: Skill 'xyz' not found
Solution: Check SKILL_REGISTRY.md for correct name
```

**Ledger State Corrupt**
```
Error: Failed to parse ledger state
Solution: Reset to template:
cp state/ledger-state-template.json state/ledger-state-live.json
```

**Dashboard Not Loading**
```
Error: CORS policy blocked
Solution: Use local server or browser extension
```

### Debug Commands

```bash
/skill info <name>      # Detailed skill information
/ledger debug           # Ledger diagnostic output
/protocol status        # All protocol states
```

### Getting Help

1. Check `docs/` folder for specifications
2. Search skills for related capabilities
3. Review integration archives for examples
4. Consult SKILL_REGISTRY.md for full index

---

## Appendix A: Command Reference

| Command | Arguments | Description |
|---------|-----------|-------------|
| `/init skills` | - | Initialize skill system |
| `/skill load` | `<name>` | Load specific skill |
| `/skill list` | `[--category]` | List available skills |
| `/skill info` | `<name>` | Skill details |
| `/ledger status` | - | Current ledger state |
| `/ledger ingest` | `<packet>` | Process CRTP packet |
| `/ledger surface` | `<query>` | Retrieve context |
| `/ledger weave` | `<id1> <id2>` | Create connection |
| `/onboard` | `<target>` | Generate onboarding |
| `/bootstrap` | `<mode>` | Activate operational mode |

## Appendix B: File Locations

| Resource | Path |
|----------|------|
| Skills Root | `skills/` |
| Skill Registry | `skills/SKILL_REGISTRY.md` |
| Bootstrap Chunk | `skills/SKILL_BOOTSTRAP_CHUNK.md` |
| Ledger State | `skills/cross-model/mnemosyne-ledger/state/ledger-state-live.json` |
| Dashboard | `artifacts/dashboard/` |
| Integration | `integration/` |
| Documentation | `docs/` |

---

*Last verified: 2025-12-07 | Protocol: Mnemosyne v1.1_Integrated*
