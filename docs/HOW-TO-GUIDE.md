# IRP Framework: Complete How-To Guide

> **Version:** 2.0 | **Updated:** 2025-12-07 | **Protocol:** Mnemosyne v1.1_Integrated

## Table of Contents

1. [Quick Start](#quick-start)
2. [Understanding the Ecosystem](#understanding-the-ecosystem)
3. [Skill System Operations](#skill-system-operations)
4. [Cross-Model Collaboration](#cross-model-collaboration)
5. [Mnemosyne Ledger Operations](#mnemosyne-ledger-operations)
6. [Bootstrap Chunk Loading](#bootstrap-chunk-loading)
7. [Integration Folder Guide](#integration-folder-guide)
8. [Dashboard Usage](#dashboard-usage)

---

## Quick Start

### For Claude Desktop Users (Filesystem MCP)

```bash
# 1. Initialize skill system
/init skills

# 2. Check ledger status
/ledger status

# 3. Load additional skills on-demand
/skill load codex-law-enforcement
```

### For API/Programmatic Access

```python
import json

# Load skill manifest
with open('skills_manifest.json') as f:
    manifest = json.load(f)

# Access specific skill
skill_path = f"skills/{manifest['skills'][0]['path']}/SKILL.md"
```

---

## Understanding the Ecosystem

### Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PACK3T C0NC3PTS ECOSYSTEM                    │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    CRTP v1.2    ┌─────────────┐              │
│  │   CLAUDE    │◄──────────────►│   GEMINI    │              │
│  │  (Backbone) │   Handshake    │   (Blood)   │              │
│  └──────┬──────┘                └──────┬──────┘              │
│         │                              │                      │
│         └──────────┬───────────────────┘                      │
│                    │                                          │
│         ┌──────────▼──────────┐                              │
│         │  MNEMOSYNE LEDGER   │                              │
│         │  (Semantic Memory)  │                              │
│         └──────────┬──────────┘                              │
│                    │                                          │
│    ┌───────────────┼───────────────┐                          │
│    │               │               │                          │
│    ▼               ▼               ▼                          │
│ ┌──────┐      ┌──────┐      ┌──────┐                         │
│ │Skills│      │ Pool │      │Xylem │                         │
│ │ (86) │      │Mode 9│      │Proto │                         │
│ └──────┘      └──────┘      └──────┘                         │
│                                                                │
└─────────────────────────────────────────────────────────────────┘
```

### Key Components

| Component | Purpose | Location |
|-----------|---------|----------|
| Skills | Deployable agent capabilities | `skills/` |
| Mnemosyne Ledger | Cross-model semantic memory | `skills/cross-model/mnemosyne-ledger/` |
| Integration | Historical conversation archives | `integration/` |
| Persona | Agent profiles & extraction results | `Persona/` |
| IRP Swarm Console | Python orchestration app | `irp_swarm_console/` |


---

## Skill System Operations

### Skill Categories

The 86+ skills are organized into these categories:

| Category | Count | Examples |
|----------|-------|----------|
| `cross-model/` | 2 | mnemosyne-ledger, gemini-onboarding |
| `core-ecosystem/` | 7 | alpha-metanode, guardian, janus-engine, lux, mj, rock, starwreck-alpha |
| `cognitive-assembly/` | 8 | claude-node, deepseek-r1, falcon, gpt-5, grok-4, kimi-k2, qwen, task-force-chimera |
| `cybersecurity-swarm/blue-team/` | 14 | intrusion-detection-agent, forensics-agent, siem-agent |
| `cybersecurity-swarm/red-team/` | 15 | reconnaissance-agent, exploit-development-agent, lateral-movement-agent |
| `governance-irp/` | 2 | architect, irp-critic |
| `research-analysis/` | 3 | deep-agent, hypothesis-engine, symbol-master-archivist |
| `orchestration/` | 4 | gemini-orchestrator, grok-sdk-developer, qwen-documentation, synthesizer |
| `adversarial-testing/` | 5 | artist, devils-advocate, innovator, stress-tester |
| `archive-documentation/` | 3 | field-archivist, joyful-archivist, mind-dojo-moderator |
| `multi-model-infrastructure/` | 7 | claude-real-adapter, gemini-real-adapter, simulated-claude, etc. |

### Loading Skills

**Method 1: Via Skill Registry Command**
```
/skill load mnemosyne-ledger
/skill load codex-law-enforcement
/skill list                        # List all available
/skill info cognitive-baseline-eval # Get skill details
```

**Method 2: Direct File Read (Filesystem MCP)**
```
# Claude reads directly from:
C:\gemini-sandbox\claudes_working_directory\skills\[category]\[skill-name]\SKILL.md
```

**Method 3: Programmatic Loading**
```python
import os
import json

SKILLS_ROOT = r"C:\gemini-sandbox\claudes_working_directory\skills"

def load_skill(skill_path):
    """Load a skill's SKILL.md file"""
    full_path = os.path.join(SKILLS_ROOT, skill_path, "SKILL.md")
    with open(full_path, 'r', encoding='utf-8') as f:
        return f.read()

# Example: Load mnemosyne ledger
ledger_skill = load_skill("cross-model/mnemosyne-ledger")
```

### Skill File Structure

Each skill follows this structure:

```
skill-name/
├── SKILL.md           # Required: Skill definition with frontmatter
├── config/            # Optional: Configuration files (JSON/YAML)
├── schemas/           # Optional: XML/JSON schemas
├── scripts/           # Optional: Executable logic (Python/TS)
├── templates/         # Optional: Response templates
├── operations/        # Optional: Sub-operation guides
└── state/             # Optional: Runtime state files
```

### SKILL.md Frontmatter Format

```yaml
---
skill_id: "unique-identifier"
name: "Human Readable Name"
version: "1.0.0"
category: "category-name"
priority: "CRITICAL|HIGH|MEDIUM|LOW"
auto_load: true|false
dependencies: ["other-skill-1", "other-skill-2"]
commands:
  - "/command-name"
  - "/another-command"
---
```


---

## Cross-Model Collaboration

### CRTP (CaaS Relational Transport Protocol) v1.2

CRTP enables structured communication between Claude and Gemini (and other models).

**Packet Types:**
| Type | Code | Purpose |
|------|------|---------|
| HANDSHAKE | 0x01 | Initial connection establishment |
| VOICE_BUNDLE | 0x08 | Voice/tone characteristic transfer |
| TOPOLOGY_SYNC | 0x0A | Memory structure synchronization |
| SEED_DORMANT | 0x0B | Dormant idea storage |
| FRICTION_LOG | 0x0C | Productive disagreement record |
| AWAKENING_TRIGGER | 0x0F | Conditional idea activation |
| ONBOARDING_MANIFEST | 0x13 | Complete protocol stack transfer |

### Gemini Onboarding Process

**Step 1: Generate Onboarding Manifest**
```
/onboard gemini
```

**Step 2: Transmit to Gemini**
Copy the generated XML packet and paste into a new Gemini session.

**Step 3: Verify Handshake**
Gemini responds with handshake confirmation containing:
- Protocol version acknowledgment
- Capability declaration
- Initial voice bundle

**Onboarding Files Location:**
```
skills/cross-model/gemini-onboarding/
├── SKILL.md                        # Onboarding protocol
├── gemini-onboarding-manifest.xml  # Complete manifest template
├── mnemosyne-packet-template.xml   # Packet structure
└── quick-reference.txt             # Quick command reference
```

### Establishing Permanent Handshakes

```xml
<handshake type="CRTP/0x01" model="Gemini-Pro-Orchestrator">
  <status>PERMANENT_OPEN</status>
  <established>2025-12-06T14:46:00-06:00</established>
  <capabilities>
    <capability>semantic_topology</capability>
    <capability>voice_preservation</capability>
    <capability>friction_synthesis</capability>
  </capabilities>
</handshake>
```

---

## Mnemosyne Ledger Operations

The Mnemosyne Ledger is the semantic memory system for cross-model persistence.

### Core Concepts

| Concept | Description |
|---------|-------------|
| **Entry** | A discrete memory unit (artifact, voice, seed, friction) |
| **State** | ACTIVE, DORMANT, COMPOST, CRYSTALLIZED |
| **Storage** | HOT (immediate), WARM (accessible), COLD (archived) |
| **Trigger** | Conditional awakening mechanism |
| **Resonance Thread** | Semantic connection between entries |

### Ledger Commands

```
/ledger status           # Full ledger state summary
/ledger ingest <packet>  # Process incoming CRTP packet
/ledger surface <query>  # Retrieve relevant context
/ledger weave <id1> <id2> # Create resonance thread
/ledger compost <id>     # Archive to cold storage
/ledger awaken <id>      # Activate dormant entry
```

### Entry Types

**ARTIFACT** - Concrete deliverables
```json
{
  "type": "ARTIFACT",
  "id": "A-20251206-001",
  "content": "Mnemosyne Protocol v1.1 Specification",
  "state": "ACTIVE",
  "storage": "WARM"
}
```

**VOICE** - Characteristic patterns from collaborators
```json
{
  "type": "VOICE",
  "id": "V-20251206-001",
  "source_model": "Gemini-Pro-Orchestrator",
  "patterns": ["metaphor-heavy", "topology-aware", "friction-embracing"]
}
```

**SEED** - Dormant ideas with activation triggers
```json
{
  "type": "SEED",
  "id": "S-20251206-001",
  "concept": "Visual Viscosity for Memory Flow",
  "state": "DORMANT",
  "trigger": "TRG-20251206-001"
}
```

**FRICTION** - Productive disagreements (preserved, not resolved)
```json
{
  "type": "FRICTION",
  "id": "F-20251206-001",
  "topic": "Timeline vs Topology organization",
  "positions": ["chronological", "semantic"],
  "resolution": "PRESERVED"
}
```

### Live State File

The current ledger state is persisted at:
```
skills/cross-model/mnemosyne-ledger/state/ledger-state-live.json
```


---

## Bootstrap Chunk Loading

The IRP Framework supports chunked system loading for Claude instances.

### Using the Pre-Built Bootstrap Chunk

**Location:** `skills/SKILL_BOOTSTRAP_CHUNK.md`

**Usage in Claude Chat:**

1. User says: "load system chunks" or "begin chunk loading"
2. Claude responds: "Bootstrap loader active. Ready to receive chunks."
3. Paste the bootstrap chunk content
4. Claude acknowledges: "SYSTEM LOAD COMPLETE - FULL ARCHITECTURE ACTIVE"

### Bootstrap Chunk XML Structure

```xml
<skill_system version="1.0" active="true">
  <paths>
    <registry>C:\gemini-sandbox\claudes_working_directory\skills\SKILL_REGISTRY.md</registry>
    <root>C:\gemini-sandbox\claudes_working_directory\skills\</root>
  </paths>
  <auto_load priority="CRITICAL">
    <skill path="cross-model/mnemosyne-ledger/SKILL.md"/>
    <skill path="cross-model/gemini-onboarding/SKILL.md"/>
    <skill path="codex-law-enforcement/SKILL.md"/>
  </auto_load>
  <commands>
    /skill load {name}, /skill list, /skill info {name}, /ledger {subcommand}, /onboard {target}
  </commands>
</skill_system>
```

### Custom Bootstrap Chunks

Create your own by following this pattern:

```markdown
# [CHUNK 1/1] IRP Skill System Bootstrap

<chunk_content>
[Your XML or configuration here]
</chunk_content>

## Post-Load Verification
After loading, run: `/init skills` to verify successful integration.
```

---

## Integration Folder Guide

The `integration/` folder contains archived conversations and cross-project integration materials.

### Folder Structure

```
integration/
├── 11-24-fcp-files/                    # November 2024 FCP archives
│   ├── FCP-20251024-172000-CONSOLIDATION.md
│   └── FCP_MANIFEST.md
├── 11-24-fcp-files.zip                 # Compressed archive
├── Gainesville-protocol/               # Gainesville Protocol materials
│   ├── FCP_Gainesville_CCNA_2000.md
│   ├── Gainesville_Protocol_Specification.md
│   ├── Gainesville_Through_Line_Analysis.md
│   └── [images and checksums]
├── integration-artifacts-20251024.zip  # Integration artifacts
├── ARCHIVE_MANIFEST.md                 # Archive index
├── CROSS_PROJECT_INTEGRATION_SPECIFICATION.md
├── creative_chronicle_*.xml            # Chronicle protocol logs
└── forward_transmission_packet_*.xml   # Forward transmission packets
```

### What These Files Contain

**FCP Files (Forward Context Packets)**
- Compressed session context for cross-session continuity
- SHA-256 hashed for integrity verification
- Contains: session state, key decisions, open threads

**Gainesville Protocol**
- Specific integration case study
- Network topology analysis (CCNA 2000 era)
- Historical context preservation

**Creative Chronicles**
- Session compression in XML format
- Key insights and emergent patterns
- Timestamped for temporal correlation

### Using Archived Materials

**To reference historical context:**
```
# Read archive manifest first
cat integration/ARCHIVE_MANIFEST.md

# Then access specific materials
cat integration/Gainesville-protocol/Gainesville_Protocol_Specification.md
```

**To verify integrity:**
```bash
# Check SHA-256 hashes
cat integration/Gainesville-protocol/Gainesville_checksums.txt
sha256sum integration/Gainesville-protocol/*.md
```


---

## Dashboard Usage

The IRP Dashboard provides a web interface for real-time repo visualization and management.

### Accessing the Dashboard

**Local Development:**
```bash
# Navigate to artifacts folder
cd C:\gemini-sandbox\claudes_working_directory\artifacts\dashboard

# Open in browser
start index.html
```

**GitHub Pages (if deployed):**
```
https://starwreckntx.github.io/IRP__METHODOLOGIES-/artifacts/dashboard/
```

### Dashboard Features

| Feature | Description |
|---------|-------------|
| **Skill Browser** | Browse and search all 86+ skills |
| **Ledger Viewer** | Real-time Mnemosyne ledger state |
| **Topology Map** | Visual graph of semantic connections |
| **Protocol Monitor** | Active handshakes and CRTP status |
| **Integration Archive** | Browse archived conversations |
| **Live GitHub Sync** | Pull latest from repo in real-time |

### Dashboard Architecture

```
artifacts/
└── dashboard/
    ├── index.html          # Main entry point
    ├── js/
    │   ├── app.js          # Main application logic
    │   ├── github-api.js   # GitHub API integration
    │   ├── skill-browser.js
    │   ├── ledger-viewer.js
    │   └── topology-map.js
    ├── css/
    │   └── styles.css
    └── data/
        └── cache/          # Local cache for offline use
```

### GitHub API Integration

The dashboard uses GitHub's REST API to fetch live data:

```javascript
// Example: Fetch skills manifest
const response = await fetch(
  'https://api.github.com/repos/starwreckntx/IRP__METHODOLOGIES-/contents/skills_manifest.json'
);
const data = await response.json();
const manifest = JSON.parse(atob(data.content));
```

### Offline Mode

The dashboard caches data locally for offline use:
- Skill definitions cached in `data/cache/`
- Ledger state syncs every 5 minutes when online
- Manual sync button for immediate refresh

---

## Operational Modes Reference

### Mode 1-8: Standard Modes

| Mode | Name | Activation | Purpose |
|------|------|------------|---------|
| 1 | ANALYTICAL | `/bootstrap analytical` | Deep reasoning |
| 2 | CREATIVE | `/bootstrap creative` | Generative ideation |
| 3 | ADVERSARIAL | `/bootstrap adversarial` | Red team analysis |
| 4 | INTEGRATION | `/bootstrap integration` | Cross-domain synthesis |
| 5 | DOCUMENTATION | `/bootstrap documentation` | Knowledge preservation |
| 6 | IMPLEMENTATION | `/bootstrap implementation` | Code generation |
| 7 | RESEARCH | `/bootstrap research` | Literature synthesis |
| 8 | GUARDIAN | `/bootstrap guardian` | Ethical oversight |

### Mode 9: THE POOL

```
/bootstrap pool
```

Resource reservoir for entropy distribution via Xylem Protocol:
- Agent dormancy management
- Context sharding
- Resource buffering

### Mode 10: TRANSCRIPT RELAY

```
/bootstrap transcript-relay
```

Cross-session context preservation:
- Conversation compaction
- Semantic summary generation
- Forward transmission packet creation

---

## Troubleshooting

### Common Issues

**Issue:** Skills not loading via Filesystem MCP
```
Solution: Verify path in SKILL_REGISTRY.md matches your local installation:
C:\gemini-sandbox\claudes_working_directory\skills\
```

**Issue:** Ledger state not persisting
```
Solution: Check write permissions on:
skills/cross-model/mnemosyne-ledger/state/ledger-state-live.json
```

**Issue:** Dashboard shows stale data
```
Solution: Click "Force Sync" button or clear browser cache
```

**Issue:** CRTP handshake failures
```
Solution: Verify Gemini instance has received onboarding manifest
Check: /ledger status for active handshakes
```

### Getting Help

- **GitHub Issues:** https://github.com/starwreckntx/IRP__METHODOLOGIES-/issues
- **Skill Registry:** `skills/SKILL_REGISTRY.md`
- **Protocol Docs:** `docs/specifications/`

---

*Document generated: 2025-12-07 | Mnemosyne Protocol v1.1_Integrated | CRTP v1.2*

