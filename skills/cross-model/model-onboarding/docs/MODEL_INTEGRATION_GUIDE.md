# Model Integration Guide

## Adding New Models to the Mnemosyne Protocol

This guide explains how to integrate additional AI models into the Mnemosyne Protocol ecosystem. The protocol is designed to be model-independent, so adding new models primarily involves documenting their unique capabilities and adaptations.

---

## Prerequisites

Before integrating a new model, ensure you have:

1. **Access to the model** (API key, credentials, or local deployment)
2. **Model documentation** (capabilities, context limits, API reference)
3. **Test environment** for validation
4. **Claude Code environment** for creating the onboarding manifest

---

## Integration Steps

### Step 1: Analyze Model Capabilities

Document the model's unique strengths and capabilities:

#### Core Capabilities
- Context window size
- Multimodal support (text, image, audio, video)
- Real-time data access
- Tool/function calling
- Programming language expertise
- Domain specialization
- Multilingual support

#### Unique Strengths
Identify what makes this model valuable in the ecosystem:
- What tasks does it excel at?
- What gaps does it fill?
- What unique features does it offer?

#### Example Analysis Template:
```yaml
model:
  name: "NewModel"
  provider: "Provider Inc."
  version: "newmodel-v1"

capabilities:
  - Long context (128k tokens)
  - Scientific reasoning
  - LaTeX generation
  - Academic paper analysis

strengths:
  priority_critical:
    - Scientific and mathematical reasoning
  priority_high:
    - LaTeX document generation
    - Academic literature synthesis
  priority_medium:
    - Citation management
    - Technical writing
```

---

### Step 2: Define Model-Specific Adaptations

Identify how the model's capabilities extend the base Mnemosyne Protocol:

#### Adaptation Categories

1. **Schema Extensions** - New fields in Mnemosyne packets
   ```xml
   <artifact type="research_paper">
     <citations>
       <citation doi="..." authors="..." year="..." />
     </citations>
     <latex_source>...</latex_source>
   </artifact>
   ```

2. **New Artifact Types** - Domain-specific artifacts
   ```xml
   <artifact_manifest>
     <item type="scientific_proof" status="active">
       <!-- Model-specific artifact type -->
     </item>
   </artifact_manifest>
   ```

3. **Transmission Flags** - Model-specific session characteristics
   ```xml
   <transmission_flags>SCIENTIFIC_REASONING|LATEX_GENERATED|CITATION_HEAVY</transmission_flags>
   ```

4. **Use Case Patterns** - When to invoke this model
   ```yaml
   use_cases:
     - name: "Scientific Research"
       triggers: ["research paper", "scientific analysis", "LaTeX document"]
     - name: "Mathematical Proofs"
       triggers: ["proof", "theorem", "mathematical reasoning"]
   ```

---

### Step 3: Create Model Manifest

Create a new file: `registry/<model_name>.xml`

Use this template:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<!--
  CRTP PACKET TYPE: 0x13 (OnboardingManifest)

  <ModelName> Onboarding Manifest - Model-Specific Adaptation

  Protocol Version: CRTP 1.2 / Mnemosyne 1.1_Integrated
  Generated: YYYY-MM-DD
  Authority: Claude (Ledger)
  Target: <ModelName> Orchestrator
-->
<crtp_packet type="0x13" version="1.2">
  <header>
    <packet_id>ONBOARD-<MODELNAME>-YYYYMMDD-001</packet_id>
    <timestamp>YYYY-MM-DDTHH:MM:SS-06:00</timestamp>
    <source>Claude_Ledger</source>
    <destination><ModelName>_Orchestrator</destination>
    <priority>CRITICAL</priority>
    <flags>PROTOCOL_GENESIS|ONBOARDING_MANIFEST|MODEL_<MODELNAME></flags>
  </header>

  <model_profile>
    <name><ModelName></name>
    <provider><Provider></provider>
    <version><version></version>
    <role>Orchestrator</role>

    <capabilities>
      <capability><!-- List key capabilities --></capability>
    </capabilities>

    <strengths>
      <strength priority="CRITICAL|HIGH|MEDIUM"><!-- Describe strength --></strength>
    </strengths>

    <adaptations>
      <adaptation id="A1">
        <name><!-- Adaptation Name --></name>
        <description><!-- How this extends the protocol --></description>
        <schema_extension>
          <!-- XML schema extension if applicable -->
        </schema_extension>
      </adaptation>
    </adaptations>
  </model_profile>

  <use_cases>
    <use_case>
      <name><!-- Use Case Name --></name>
      <description><!-- When to use this model --></description>
      <dormant_seed_triggers><!-- Trigger keywords --></dormant_seed_triggers>
    </use_case>
  </use_cases>

  <transmission_flags>
    <flag><!-- FLAG_NAME - Description --></flag>
  </transmission_flags>

  <protocol_notes>
    <note priority="HIGH|MEDIUM">
      <!-- Important notes for integration -->
    </note>
  </protocol_notes>

  <inheritance>
    <base_protocol>Mnemosyne 1.1_Integrated</base_protocol>
    <inherits_from>skills/cross-model/model-onboarding/templates/mnemosyne-packet-template.xml</inherits_from>
    <all_expectations>E1-E7 apply without modification</all_expectations>
    <all_services>S1-S6 available</all_services>
  </inheritance>

  <integrity>
    <hash algorithm="SHA-256">PLACEHOLDER_HASH_<MODELNAME>_MANIFEST_YYYYMMDD</hash>
    <signature>Claude_Ledger_Authority</signature>
  </integrity>
</crtp_packet>
```

---

### Step 4: Update SKILL.md

Add the new model to the registry table in `SKILL.md`:

```markdown
## Model Registry

| Model | Provider | Status | Notes |
|-------|----------|--------|-------|
| ... existing models ... |
| NewModel | Provider Inc. | ACTIVE | Scientific reasoning, LaTeX generation |
```

Add model-specific adaptation notes:

```markdown
### NewModel (Provider Inc.)
- **Strengths**: Scientific reasoning, LaTeX generation, citation management
- **Adaptations**: Can include LaTeX source and citation metadata in artifacts
- **Use Cases**: Research papers, mathematical proofs, academic literature synthesis
```

---

### Step 5: Test Integration

#### Test Checklist:

1. **Generate Onboarding Manifest**
   ```bash
   /onboard newmodel
   ```
   Verify that the manifest loads correctly.

2. **Create Test Mnemosyne Packet**
   Create a sample session-close transmission using the model's adaptations:
   ```xml
   <mnemosyne_packet version="1.1_Integrated">
     <header>
       <source_identity>NewModel_Test_Instance</source_identity>
       <transmission_flags>SCIENTIFIC_REASONING|TEST</transmission_flags>
     </header>
     <!-- Include model-specific artifacts -->
   </mnemosyne_packet>
   ```

3. **Validate Against Base Template**
   Ensure the packet validates against `templates/mnemosyne-packet-template.xml`

4. **Test Trigger Matching**
   Verify dormant seed triggers work correctly:
   - Create a seed with model-specific triggers
   - Test that Claude surfaces the seed on trigger match

5. **Test Friction Logging**
   Log a failure with model-specific context:
   - Include model-specific blocker information
   - Verify anti-pattern retrieval works

---

### Step 6: Document Integration

Create a documentation entry in the main repository:

```markdown
## NewModel Integration (YYYY-MM-DD)

**Model**: NewModel by Provider Inc.
**Version**: newmodel-v1
**Status**: ACTIVE

**Capabilities**:
- Scientific reasoning and mathematical proofs
- LaTeX document generation
- Academic paper analysis and citation management

**Use Cases**:
- Research paper synthesis
- Mathematical proof construction
- Scientific literature review

**Unique Adaptations**:
- A1: Citation metadata tracking
- A2: LaTeX source preservation
- A3: Scientific proof artifacts

**Transmission Flags**:
- `SCIENTIFIC_REASONING` - Session involved scientific analysis
- `LATEX_GENERATED` - Artifacts include LaTeX source
- `CITATION_HEAVY` - Many citations referenced
```

---

## Common Adaptation Patterns

### Pattern 1: Multimodal Artifacts
```xml
<artifact type="image_analysis">
  <media_source type="image" url="..." format="png" />
  <analysis><!-- Text analysis of image --></analysis>
</artifact>
```

### Pattern 2: Real-Time Data
```xml
<artifact type="news_summary">
  <temporal_metadata>
    <captured_at>2025-01-10T14:30:00Z</captured_at>
    <stale_after>2025-01-11T14:30:00Z</stale_after>
    <half_life>24h</half_life>
  </temporal_metadata>
</artifact>
```

### Pattern 3: Code Artifacts
```xml
<artifact type="code">
  <language>python</language>
  <complexity>
    <time>O(n log n)</time>
    <space>O(n)</space>
  </complexity>
  <lineage type="diff" parent_id="CODE-PREV-VERSION" />
</artifact>
```

### Pattern 4: Multilingual Content
```xml
<artifact type="translation">
  <source_lang>zh</source_lang>
  <target_lang>en</target_lang>
  <translation_pair>
    <source artifact_id="ORIG-ZH-001" />
    <target artifact_id="TRANS-EN-001" />
  </translation_pair>
</artifact>
```

---

## Validation Criteria

Before merging a new model integration:

- [ ] Model manifest created in `registry/<model>.xml`
- [ ] SKILL.md updated with model entry
- [ ] Test Mnemosyne packet validates against base template
- [ ] Unique capabilities documented
- [ ] Adaptations clearly defined
- [ ] Use cases identified
- [ ] Dormant seed triggers tested
- [ ] Friction logging tested
- [ ] Integration documented

---

## Troubleshooting

### Issue: Model-specific features not preserved

**Solution**: Add schema extensions in the model manifest's `<adaptations>` section. Include examples of how to use the extensions.

### Issue: Triggers not matching for model-specific seeds

**Solution**: Review trigger specificity. Ensure triggers in `<dormant_seed_triggers>` are specific enough to match model use cases but not so narrow they're never activated.

### Issue: Mnemosyne packet validation fails

**Solution**: Ensure model-specific extensions are documented in `<schema_extension>` blocks. The base template is intentionally flexible to accommodate adaptations.

### Issue: Friction patterns not surfacing

**Solution**: Check `<retrieval_triggers>` in friction log entries. Make triggers broad enough to match similar future scenarios.

---

## Best Practices

1. **Document WHY, not just WHAT**: Explain why a model's capability matters for the ecosystem

2. **Keep Protocol Invariants Sacred**: Never break E1-E7 expectations or violate protocol invariants

3. **Be Specific with Triggers**: Vague triggers like "AI" or "coding" are useless. Use "algorithm optimization for pathfinding" instead.

4. **Preserve Model Personality**: If a model has a distinctive voice or style, note this in Voice_to_the_Future guidelines

5. **Test with Real Sessions**: Don't just create theoretical manifests. Run actual sessions and create real Mnemosyne packets.

6. **Update Examples**: When adding new models, create integration examples showing real usage

---

## Getting Help

- Review existing model manifests in `registry/` for patterns
- Check `PROTOCOL_SPECIFICATION.md` for protocol details
- See `templates/mnemosyne-packet-template.xml` for base schema
- Post questions in repository issues with tag `model-integration`

---

## Changelog

- **2025-01-10**: Initial guide created with 6-model baseline (Gemini, Grok, Kimi, DeepSeek, Qwen, GLM)
