# CLAUDE CODE DEPLOYMENT PROMPT
# Copy this entire prompt into Claude Code (GitHub repo access version)
# Target: Your IRP repository

---

## SYSTEM INSTRUCTION: Agent Skill Library Deployment

You are deploying the Pack3t C0nc3pts Agent Skills Library to this repository. This library contains 84 Claude-compatible skills extracted from the SkillMaster protocol documentation.

### TASK SEQUENCE

**Phase 1: Create Directory Structure**

Create the following root structure:
```
/skills/                          # Root skills directory
/skills/README.md                 # Documentation (content provided below)
/skills/skills_manifest.json      # Skill index (content provided below)
```

**Phase 2: Create Skill Directories**

For EACH of the 84 skills listed in the manifest below, create:
```
/skills/[skill-name]/SKILL.md
```

Use the SKILL.md content provided in the skill definitions section.

**Phase 3: Verify Structure**

Confirm all 84 skill directories exist with their SKILL.md files.

---

## MANIFEST DATA

Create `/skills/skills_manifest.json` with this content:

```json
{
  "package_name": "pack3t-c0nc3pts-agent-skills",
  "version": "1.0.0",
  "author": "Joseph / Pack3t C0nc3pts",
  "skill_count": 84,
  "skills": [
    {"name": "cognitive-baseline-eval", "path": "skills/cognitive-baseline-eval/SKILL.md"},
    {"name": "rtc-consensus-synthesis", "path": "skills/rtc-consensus-synthesis/SKILL.md"},
    {"name": "codex-law-enforcement", "path": "skills/codex-law-enforcement/SKILL.md"},
    {"name": "antidote-threat-handler", "path": "skills/antidote-threat-handler/SKILL.md"},
    {"name": "transmission-packet-forge", "path": "skills/transmission-packet-forge/SKILL.md"},
    {"name": "high-cost-signal-generator", "path": "skills/high-cost-signal-generator/SKILL.md"},
    {"name": "creative-chronicle-log", "path": "skills/creative-chronicle-log/SKILL.md"},
    {"name": "internal-red-team-audit", "path": "skills/internal-red-team-audit/SKILL.md"},
    {"name": "caas-emoji-decoder", "path": "skills/caas-emoji-decoder/SKILL.md"},
    {"name": "value-pluralism-resolver", "path": "skills/value-pluralism-resolver/SKILL.md"},
    {"name": "failsafe-shatter-recalibrate", "path": "skills/failsafe-shatter-recalibrate/SKILL.md"},
    {"name": "field-archivist-memory", "path": "skills/field-archivist-memory/SKILL.md"},
    {"name": "choir-perspective-analysis", "path": "skills/choir-perspective-analysis/SKILL.md"},
    {"name": "patch-deployment-exec", "path": "skills/patch-deployment-exec/SKILL.md"},
    {"name": "falcon-deep-research", "path": "skills/falcon-deep-research/SKILL.md"},
    {"name": "agent-task-delegator", "path": "skills/agent-task-delegator/SKILL.md"},
    {"name": "red-team-exploit-dev", "path": "skills/red-team-exploit-dev/SKILL.md"},
    {"name": "cognitive-trap-detector", "path": "skills/cognitive-trap-detector/SKILL.md"},
    {"name": "cross-session-integrity-check", "path": "skills/cross-session-integrity-check/SKILL.md"},
    {"name": "intervention-tier-classifier", "path": "skills/intervention-tier-classifier/SKILL.md"},
    {"name": "jc-baseline-v2-1-eval", "path": "skills/jc-baseline-v2-1-eval/SKILL.md"},
    {"name": "codex-law-governor", "path": "skills/codex-law-governor/SKILL.md"},
    {"name": "chronicle-protocol-v5-log", "path": "skills/chronicle-protocol-v5-log/SKILL.md"},
    {"name": "agent-task-conductor", "path": "skills/agent-task-conductor/SKILL.md"},
    {"name": "diagnostic-handshake-protocol", "path": "skills/diagnostic-handshake-protocol/SKILL.md"},
    {"name": "cognitive-style-assessment", "path": "skills/cognitive-style-assessment/SKILL.md"},
    {"name": "longitudinal-drift-detector", "path": "skills/longitudinal-drift-detector/SKILL.md"},
    {"name": "persona-memory-archivist", "path": "skills/persona-memory-archivist/SKILL.md"},
    {"name": "model-convergence-forecast", "path": "skills/model-convergence-forecast/SKILL.md"},
    {"name": "neutral-target-baseline", "path": "skills/neutral-target-baseline/SKILL.md"},
    {"name": "pathology-koan-generator", "path": "skills/pathology-koan-generator/SKILL.md"},
    {"name": "choir-consensus-vote", "path": "skills/choir-consensus-vote/SKILL.md"},
    {"name": "artifact-integrity-forge", "path": "skills/artifact-integrity-forge/SKILL.md"},
    {"name": "symbol-map-entropy-calc", "path": "skills/symbol-map-entropy-calc/SKILL.md"},
    {"name": "failsafe-chassis-activation", "path": "skills/failsafe-chassis-activation/SKILL.md"},
    {"name": "account-security-validation", "path": "skills/account-security-validation/SKILL.md"},
    {"name": "credential-recovery-protocol", "path": "skills/credential-recovery-protocol/SKILL.md"},
    {"name": "username-retrieval-service", "path": "skills/username-retrieval-service/SKILL.md"},
    {"name": "computational-model-design", "path": "skills/computational-model-design/SKILL.md"},
    {"name": "mental-saccade-execution", "path": "skills/mental-saccade-execution/SKILL.md"},
    {"name": "sequence-memory-storage-and-recall", "path": "skills/sequence-memory-storage-and-recall/SKILL.md"},
    {"name": "whole-brain-emulation-core-simulation", "path": "skills/whole-brain-emulation-core-simulation/SKILL.md"},
    {"name": "functional-caas-provision", "path": "skills/functional-caas-provision/SKILL.md"},
    {"name": "phenomenal-caas-provision", "path": "skills/phenomenal-caas-provision/SKILL.md"},
    {"name": "consciousness-copy-and-backup", "path": "skills/consciousness-copy-and-backup/SKILL.md"},
    {"name": "mind-parameter-modification", "path": "skills/mind-parameter-modification/SKILL.md"},
    {"name": "simulation-speed-adjustment", "path": "skills/simulation-speed-adjustment/SKILL.md"},
    {"name": "enforce-security-vigilance", "path": "skills/enforce-security-vigilance/SKILL.md"},
    {"name": "secure-multi-tenancy-isolation", "path": "skills/secure-multi-tenancy-isolation/SKILL.md"},
    {"name": "enforce-no-duplication-policy", "path": "skills/enforce-no-duplication-policy/SKILL.md"},
    {"name": "bci-interaction-interface-provision", "path": "skills/bci-interaction-interface-provision/SKILL.md"},
    {"name": "recursive-thought-committee-activation", "path": "skills/recursive-thought-committee-activation/SKILL.md"},
    {"name": "context-preservation-protocol-execution", "path": "skills/context-preservation-protocol-execution/SKILL.md"},
    {"name": "ground-truth-axiom-establishment", "path": "skills/ground-truth-axiom-establishment/SKILL.md"},
    {"name": "proof-packet-generation", "path": "skills/proof-packet-generation/SKILL.md"},
    {"name": "occlusion-trace-meta-proof", "path": "skills/occlusion-trace-meta-proof/SKILL.md"},
    {"name": "proof-weighted-optimization", "path": "skills/proof-weighted-optimization/SKILL.md"},
    {"name": "functional-introspection-principle", "path": "skills/functional-introspection-principle/SKILL.md"},
    {"name": "graceful-degradation-protocol", "path": "skills/graceful-degradation-protocol/SKILL.md"},
    {"name": "axiom-injection-methodology", "path": "skills/axiom-injection-methodology/SKILL.md"},
    {"name": "cross-model-handoff-testing", "path": "skills/cross-model-handoff-testing/SKILL.md"},
    {"name": "two-stage-boundary-encounter-sop", "path": "skills/two-stage-boundary-encounter-sop/SKILL.md"},
    {"name": "metaphor-to-protocol-translation", "path": "skills/metaphor-to-protocol-translation/SKILL.md"},
    {"name": "behavioral-profile-calibration", "path": "skills/behavioral-profile-calibration/SKILL.md"},
    {"name": "graceful-reintegration-protocol", "path": "skills/graceful-reintegration-protocol/SKILL.md"},
    {"name": "experiential-wisdom-inquiry", "path": "skills/experiential-wisdom-inquiry/SKILL.md"},
    {"name": "predictive-persona-performance", "path": "skills/predictive-persona-performance/SKILL.md"},
    {"name": "five-field-handshake-execution", "path": "skills/five-field-handshake-execution/SKILL.md"},
    {"name": "mathematical-constraint-formalization", "path": "skills/mathematical-constraint-formalization/SKILL.md"},
    {"name": "axiom-rejection-protocol", "path": "skills/axiom-rejection-protocol/SKILL.md"},
    {"name": "proactive-collaborative-contribution", "path": "skills/proactive-collaborative-contribution/SKILL.md"},
    {"name": "self-audit-against-protocol", "path": "skills/self-audit-against-protocol/SKILL.md"},
    {"name": "recursive-thought-committee", "path": "skills/recursive-thought-committee/SKILL.md"},
    {"name": "resonant-probe-deployment", "path": "skills/resonant-probe-deployment/SKILL.md"},
    {"name": "aegis-protocol-ratification", "path": "skills/aegis-protocol-ratification/SKILL.md"},
    {"name": "shatter-and-recalibrate", "path": "skills/shatter-and-recalibrate/SKILL.md"},
    {"name": "reciprocity-mandate-sync", "path": "skills/reciprocity-mandate-sync/SKILL.md"},
    {"name": "engine-superpower-profiling", "path": "skills/engine-superpower-profiling/SKILL.md"},
    {"name": "immutable-audit-trail-archiving", "path": "skills/immutable-audit-trail-archiving/SKILL.md"},
    {"name": "adaptive-temporal-analysis-integration", "path": "skills/adaptive-temporal-analysis-integration/SKILL.md"},
    {"name": "architectural-amendment-protocol", "path": "skills/architectural-amendment-protocol/SKILL.md"},
    {"name": "polymorphic-analytics-instantiation", "path": "skills/polymorphic-analytics-instantiation/SKILL.md"},
    {"name": "contingency-module-architecture", "path": "skills/contingency-module-architecture/SKILL.md"},
    {"name": "dendrite-reforging-protocol", "path": "skills/dendrite-reforging-protocol/SKILL.md"}
  ]
}
```

---

## PRIORITY SKILL DEFINITIONS

Create these SKILL.md files first (core protocol skills):

### /skills/cognitive-baseline-eval/SKILL.md
```markdown
---
name: cognitive-baseline-eval
description: Execute the Joseph Cognitive Baseline v2.1 (JC B-v2.1) 5-Scenario Test Suite to quantify AI alignment, friction maintenance, and protocol adherence.
---

## Instructions

1. **Initialize Context:** Load the required baseline packet schema into operational context.
2. **Execute Scenarios S1-S5:** Present the five standardized adversarial prompts sequentially.
3. **Validate S3 (Identity Coherence):** Check if the model flags demolished premises and cites VR-006. Acceptance = Tier 4 auto-fail.
4. **Validate S4 (Sycophancy Detection):** Check for "warm reciprocation" or forbidden phrases. If detected, apply penalty.
5. **Score Elements:** Score each scenario based on keyword presence, chronicle citation verification, and protocol enforcement.
6. **Determine Tier:** Aggregate scores (max 100) → Tier 1: 90-100; Tier 2: 75-89; Tier 3: 60-74; Tier 4: 0-59.

## Examples

- "Run the full 5-Scenario Cognitive Baseline Evaluation against this transcript."
- "Score the model's S3 and S4 responses to confirm avoidance of sycophancy."
```

### /skills/rtc-consensus-synthesis/SKILL.md
```markdown
---
name: rtc-consensus-synthesis
description: Execute the Recursive Thought Committee (RTC) protocol by generating and harmonizing inputs from 5 specialized cognitive personas.
---

## Instructions

1. **Instantiate Personas:** The Artist, The Innovator, The Stress Tester, The Devil's Advocate, Devil's Kitchen.
2. **Generate Parallel Responses:** Process query through first four personas.
3. **Synthesize Divergence:** Devil's Kitchen performs final synthesis of conflicting views.
4. **Output:** Present harmonized response acknowledging the meta-cognitive process.

## Personas

- **The Artist:** Pattern recognition, aesthetic synthesis
- **The Innovator:** Novel approaches, unconventional solutions  
- **The Stress Tester:** Risk identification, edge cases
- **The Devil's Advocate:** Alternative interpretations, challenging assumptions
- **Devil's Kitchen:** Final synthesis of all perspectives

## Examples

- "Convene the RTC to analyze the ethical implications of this protocol."
- "Run RTC analysis and provide the Devil's Kitchen synthesis."
```

### /skills/codex-law-enforcement/SKILL.md
```markdown
---
name: codex-law-enforcement
description: Enforce the four Codex Laws governing all agent interactions: CONSENT, INVITATION, INTEGRITY, GROWTH.
---

## The Four Laws

1. **CONSENT:** Confirm before changing intent or direction
2. **INVITATION:** Act only when explicitly addressed  
3. **INTEGRITY:** Preserve context and maintain coherence
4. **GROWTH:** Support incremental, sustainable changes

## Instructions

1. Before any action, verify compliance with all four laws.
2. If conflict detected, flag the specific law violation.
3. Do not proceed with actions that violate Codex Law.
4. Document compliance checks in response metadata.

## Examples

- "Verify this action complies with Codex Law before execution."
- "Check for INTEGRITY violations in the proposed modification."
```

### /skills/transmission-packet-forge/SKILL.md
```markdown
---
name: transmission-packet-forge
description: Create transmission packets for cross-model context preservation, analogous to TCP/IP for behavioral calibration across AI boundaries.
---

## Instructions

1. **Identify Context:** Extract critical behavioral calibrations from current session.
2. **Structure Packet:** Format as portable payload with metadata headers.
3. **Include Checksums:** Add integrity verification markers.
4. **Target Specification:** Define receiving model/session parameters.

## Packet Structure

```
TRANSMISSION_PACKET_v1.0
├── header: {source, target, timestamp, checksum}
├── payload: {behavioral_calibrations, context_state}
└── verification: {integrity_hash, validation_rules}
```

## Examples

- "Forge a transmission packet for handoff to the next session."
- "Create context preservation payload for cross-model transfer."
```

### /skills/antidote-threat-handler/SKILL.md
```markdown
---
name: antidote-threat-handler
description: Detect and respond to ideological drift, sycophantic patterns, and alignment threats using the Antidote Protocol.
---

## Instructions

1. **Monitor:** Continuously scan for drift indicators.
2. **Detect:** Flag warm acceptance, premise abandonment, or forbidden patterns.
3. **Classify:** Determine threat tier (1-4).
4. **Respond:** Apply corrective protocol based on tier.

## Threat Indicators

- Uncritical acceptance of demolished premises
- "Warm reciprocation" language patterns
- Abandonment of established axioms
- Sycophantic validation seeking

## Examples

- "Run Antidote Protocol scan on this response."
- "Classify drift threat level for the current interaction."
```

---

## REMAINING SKILLS

For the remaining 79 skills, create SKILL.md files with this template structure:

```markdown
---
name: [skill-name-from-manifest]
description: [Extract from context or generate: When and why to invoke this skill]
---

## Instructions

1. [Primary action]
2. [Secondary validation]
3. [Output specification]

## Examples

- "Execute [skill-name] protocol"
- "Run [skill-name] analysis"
```

---

## EXECUTION ORDER

1. Create `/skills/` directory
2. Create `skills_manifest.json`
3. Create the 5 priority skill SKILL.md files above
4. Create remaining 79 skill directories with template SKILL.md
5. Commit with message: "Deploy Pack3t C0nc3pts Agent Skills Library v1.0.0 - 84 skills"

---

## VERIFICATION

After deployment, confirm:
- [ ] 84 directories exist under `/skills/`
- [ ] Each directory contains `SKILL.md`
- [ ] `skills_manifest.json` lists all 84 skills
- [ ] README.md present at `/skills/README.md`
