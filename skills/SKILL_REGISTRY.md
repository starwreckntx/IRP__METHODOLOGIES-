# IRP Skill Registry
## Version: 1.0
## Last Updated: 2025-12-06

---

## Location
**Skills Root:** `C:\gemini-sandbox\claudes_working_directory\skills\`

---

## Auto-Load Skills (HIGH PRIORITY)
These skills should be loaded at session initialization:

| Skill | Path | Purpose |
|-------|------|---------|
| mnemosyne-ledger | `cross-model/mnemosyne-ledger/` | Claude backbone memory system |
| gemini-onboarding | `cross-model/gemini-onboarding/` | Spec for Gemini collaboration |
| codex-law-enforcement | `codex-law-enforcement/` | CONSENT, INVITATION, INTEGRITY, GROWTH |

---

## Skill Loading Protocol

### Session Initialization
```
1. Read SKILL_REGISTRY.md
2. Load auto-load skills via Filesystem:read_file
3. Acknowledge loaded skills
4. Arm any awakening triggers from loaded skills
```

### On-Demand Loading
When user invokes `/skill load <name>`:
```
1. Filesystem:read_file(skills_root/<name>/SKILL.md)
2. If schemas/ exists: load relevant schemas
3. If config/ exists: load configuration
4. If operations/ exists: summarize available procedures
5. Acknowledge skill with capability summary
```

### Skill Discovery
When user invokes `/skill list`:
```
1. Filesystem:directory_tree(skills_root)
2. Return formatted skill categories and names
```

---

## Command Reference

### Mnemosyne Ledger Commands
```
/ledger status          - Current ledger state summary
/ledger ingest <packet> - Process Mnemosyne packet
/ledger surface <query> - Surface relevant context
/ledger query <search>  - Semantic topology search
/ledger arm <trigger>   - Arm awakening trigger
/ledger awaken <seed>   - Manually awaken dormant seed
/ledger compost <id>    - Move to anti-pattern library
/ledger weave <a> <b>   - Create resonance edge
/ledger topology        - Visualize graph structure
/ledger hot             - List HOT context
/ledger triggers        - List armed triggers
/ledger seeds           - List dormant seeds
```

### Gemini Onboarding Commands
```
/onboard gemini         - Emit full CRTP/0x13 manifest
/onboard gemini --template  - Emit Mnemosyne packet template
/onboard gemini --quick     - Emit ASCII quick reference
```

### General Skill Commands
```
/skill load <name>      - Load skill into session
/skill list             - List available skills
/skill info <name>      - Show skill summary
/skill unload <name>    - Remove from active context
```

---

## Skill Categories

### Cross-Model (`cross-model/`)
- `mnemosyne-ledger` - Claude memory backbone
- `gemini-onboarding` - Gemini collaboration spec

### Core Ecosystem (`core-ecosystem/`)
- `alpha-metanode` - Central coordination
- `guardian` - Safety oversight
- `janus-engine` - Dialectical processing
- `lux` - Illumination/insight
- `mj` - Creative synthesis
- `rock` - Stability/grounding
- `starwreck-alpha` - Primary persona

### Cognitive Assembly (`cognitive-assembly/`)
- Model-specific nodes (claude-node, deepseek-r1, falcon, gpt-5, grok-4, kimi-k2, qwen)
- `task-force-chimera` - Multi-model coordination

### Cybersecurity Swarm (`cybersecurity-swarm/`)
- `blue-team/` - 14 defensive agents
- `red-team/` - 15 offensive agents

### Governance (`governance-irp/`)
- `architect` - System design
- `irp-critic` - Critical evaluation

### Research Analysis (`research-analysis/`)
- `deep-agent` - Deep research
- `hypothesis-engine` - Theory generation
- `symbol-master-archivist` - Symbol system management

---

## File Structure Convention
```
skill-name/
├── SKILL.md           # Required: Main skill definition
├── schemas/           # Optional: XML/JSON schemas
├── config/            # Optional: Configuration files
├── operations/        # Optional: Procedure documentation
├── templates/         # Optional: Output templates
├── src/               # Optional: Source code
└── data/              # Optional: Data files
```

---

## Integration Points

### IRP Framework Modes
- **Mode 9 (Pool):** Xylem entropy distribution
- **Mode 10 (Transcript Relay):** Mnemosyne packet ingestion

### Protocols
- **CRTP:** Cross-model packet transmission
- **Mnemosyne:** Memory persistence
- **Xylem:** Resource distribution
- **Muon:** Session evaluation

---

## Notes for Claude Instances

1. **Skills live on user's Windows machine** - Use Filesystem MCP to read
2. **Auto-load critical skills** at session start
3. **Honor skill commands** when user invokes them
4. **Persist state** via ledger-state.json when possible
5. **Emit packets** per protocol specifications

---

## Bootstrap Integration

Add to chunked loading protocol:
```xml
[CHUNK N/M] SKILL SYSTEM
<skill_system active="true">
  <registry>C:\gemini-sandbox\claudes_working_directory\skills\SKILL_REGISTRY.md</registry>
  <root>C:\gemini-sandbox\claudes_working_directory\skills\</root>
  <auto_load>mnemosyne-ledger,gemini-onboarding</auto_load>
</skill_system>
```
