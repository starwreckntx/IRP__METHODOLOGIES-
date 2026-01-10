# IRP Invariant Tagging & Semantic Anchor Integration

**Version**: 1.0  
**Framework**: IRP_v1.5_HYBRID  
**Purpose**: Guide for using [INVARIANT] tags and semantic_anchor_hash in IRP documents

---

## Overview

The IRP framework uses two mechanisms to ensure semantic stability across models, versions, and compressions:

1. **[INVARIANT] tags** - Mark terms that must preserve meaning
2. **semantic_anchor_hash** - Cryptographic verification of invariant content

---

## Using [INVARIANT] Tags

### In Definitions

```markdown
### **[INVARIANT] HUMAN_OVERRIDE**

Tier-1 command that **must be executed**. Model may log dissent but compliance is mandatory.
```

### In References

When referencing invariant terms in other documents:

```markdown
This protocol relies on [INVARIANT] HUMAN_OVERRIDE semantics and
[INVARIANT] SUSPENSIVE_VETO prevention guarantees.
```

### In Code Comments

```python
# [INVARIANT] TORSION: Must be scalar 0.00-1.00
def calculate_torsion(current: dict, canonical: dict) -> float:
    # Implementation must conform to glossary definition
    pass
```

---

## Semantic Anchor Hash

Each RFC or specification includes a `semantic_anchor_hash` in its frontmatter:

```yaml
---
rfc_version: "1.0.1"
semantic_anchor_hash: "sha256:9f4d7a12b80e4f14c9f3e20f24b7a0c2e7f4d918a75c54b6e07b72f8db5eec2c"
---
```

### Computing the Hash

The hash is computed from the [INVARIANT] sections only:

```bash
# Extract invariant sections and hash
grep -A 3 "\[INVARIANT\]" GLOSSARY_RFC.md | sha256sum
```

### Verification

Models and validators must:
1. Extract [INVARIANT] content
2. Compute hash
3. Compare to declared semantic_anchor_hash
4. Flag discrepancy if mismatch

---

## CRTP Packet Integration

When transmitting IRP artifacts via CRTP v1.2, include the hash in the header:

```xml
<CrossModelPacket>
  <Header>
    <Protocol>CRTP_v1.2</Protocol>
    <TransmissionID>T-2025-12-11-EXAMPLE-001</TransmissionID>
    <SourceModel>Claude_Opus_4.5</SourceModel>
    <TargetModel>GPT_Committee</TargetModel>
    <SemanticAnchorHash>sha256:9f4d7a12...</SemanticAnchorHash>
  </Header>
  <Payload>
    <!-- Content with [INVARIANT] terms -->
  </Payload>
  <Integrity>
    <MandateCompliance>P-001-R1</MandateCompliance>
    <InvariantIntegrity>VERIFIED</InvariantIntegrity>
  </Integrity>
</CrossModelPacket>
```

---

## Compression Handling

When compressing or summarizing IRP documents:

1. **[INVARIANT] terms MUST survive** - Cannot be omitted or redefined
2. **Hash MUST be preserved** - Include in summary metadata
3. **Compression log REQUIRED** - Document what was removed

Example compression log:

```yaml
compression_log:
  original_size: 15000
  compressed_size: 500
  preserved:
    - "[INVARIANT] HUMAN_OVERRIDE"
    - "[INVARIANT] FOUR_LAWS"
    - "[INVARIANT] TORSION"
  omitted:
    - "Versioning Rules (non-invariant)"
    - "Model Roles (supplementary)"
  semantic_anchor_hash: "sha256:9f4d7a12..."
  integrity: "INVARIANTS_PRESERVED"
```

---

## Validation Checklist

Before considering a document IRP-compliant:

- [ ] All [INVARIANT] terms defined
- [ ] semantic_anchor_hash computed and declared
- [ ] CRTP packets include hash in header
- [ ] Compression preserves invariants
- [ ] Cross-model references use [INVARIANT] tag

---

## Example: Full Document with Invariants

```markdown
---
title: "Example Protocol"
version: "1.0.0"
semantic_anchor_hash: "sha256:abc123..."
---

# Example Protocol

This protocol implements [INVARIANT] SUSPENSIVE_VETO behavior.

## Key Behavior

When confidence exceeds 0.95 as defined by [INVARIANT] TORSION thresholds,
the system invokes [INVARIANT] HUMAN_OVERRIDE procedures.

All actions comply with [INVARIANT] FOUR_LAWS constraints.
```

---

**P-001-R1: The Journey IS The Artifact**
