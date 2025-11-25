# Pack3t C0nc3pts Agent Skills Library

**"Security is Not Inherent"**

A comprehensive library of 84 deployable AI agent skills extracted from the Pack3t C0nc3pts protocol suite. These skills are designed for use with Claude's skill system (`/mnt/skills/`) or similar agent architectures.

## Overview

| Metric | Value |
|--------|-------|
| Total Skills | 84 |
| Version | 1.0.0 |
| Origin | SkillMaster v1 Audit |
| Architecture | Claude Skills Compatible |

## Skill Categories

### Core Protocol Skills
- `cognitive-baseline-eval` — JC Baseline v2.1 5-Scenario Test Suite
- `rtc-consensus-synthesis` — Recursive Thought Committee execution
- `codex-law-enforcement` — Codex Law (CONSENT, INVITATION, INTEGRITY, GROWTH)
- `transmission-packet-forge` — Cross-model context preservation
- `creative-chronicle-log` — CCP v5.0 logging

### Alignment & Integrity
- `antidote-threat-handler` — Ideological drift detection
- `longitudinal-drift-detector` — Constitutional embedding monitoring
- `cognitive-trap-detector` — Guardian Protocol trap taxonomy
- `failsafe-shatter-recalibrate` — Premise rejection and reconstruction

### Multi-Agent Orchestration
- `agent-task-conductor` — Model node orchestration
- `choir-perspective-analysis` — CHOIR protocol execution
- `choir-consensus-vote` — Multi-perspective voting synthesis
- `falcon-deep-research` — Deep research integration

### Meta-Cognitive
- `persona-memory-archivist` — Cross-session persona persistence
- `artifact-integrity-forge` — SHA-256 verification pipeline
- `symbol-map-entropy-calc` — Entropy analysis metrics
- `pathology-koan-generator` — Adversarial prompt generation

## Directory Structure

```
skills/
├── [skill-name]/
│   ├── SKILL.md          # Skill definition with frontmatter
│   ├── config/           # Configuration files (if applicable)
│   ├── schemas/          # JSON/XML schemas (if applicable)
│   └── scripts/          # Executable logic (if applicable)
└── ...
```

## SKILL.md Format

Each skill follows the Claude Skills specification:

```markdown
---
name: skill-name
description: When and why to invoke this skill (<200 chars)
---

## Instructions
Step-by-step execution rules.

## Examples
- "User trigger phrase 1"
- "User trigger phrase 2"
```

## Deployment

### Option 1: Claude Skills Directory
Copy to `/mnt/skills/user/` for Claude Desktop/Code integration.

### Option 2: Custom Agent Framework
Import `skills_manifest.json` and load skills dynamically.

### Option 3: Claude Code GitHub Integration
Use the provided deployment prompt with Claude Code's GitHub repo access.

## Manifest

See `skills_manifest.json` for the complete skill index with paths and descriptions.

## Origin

Extracted from 15,000 lines of protocol documentation via systematic audit. Gemini 3 CLI initially extracted 20 skills (anchoring to schema header); this package represents the complete 84-skill extraction.

## License

Pack3t C0nc3pts Protocol Suite — For research and personal use.

---

*"To know anything is to know you know nothing."*
