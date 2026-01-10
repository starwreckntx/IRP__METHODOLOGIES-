# Ledger Ingestion Procedure

## Purpose
Process incoming Mnemosyne packets and integrate into ledger.

## Trigger
- Receipt of CRTP packet with `MNE` flag
- Manual `/ledger ingest` command
- IRP Mode 10 transcript relay

## Procedure

### 1. Validation
```
IF packet.version != "1.1_Integrated"
  EMIT warning "Version mismatch"
  ATTEMPT compatibility parse

VALIDATE required fields:
  - header.timestamp
  - header.source_identity
  - artifact_manifest (may be empty)
  - voice_to_the_future (REQUIRED)

IF voice_to_the_future MISSING OR EMPTY
  EMIT error "Critical: Voice missing"
  LOG to friction as protocol violation
  CONTINUE with partial ingest
```

### 2. Artifact Processing
```
FOR EACH item IN artifact_manifest:
  CREATE ledger_entry:
    - id: LE-{timestamp}-{hash}
    - entry_type: "artifact"
    - state: item.status
    - storage_class: WARM (default) | HOT (if critical flag)
    - content: item.description
    - resonance_tags: item.resonance_tags
    - lineage.parent_id: item.lineage (if present)

  CREATE topology_node:
    - node_id: TN-{ledger_entry.id}
    - semantic_vector: GENERATE from resonance_tags

  WEAVE resonance_edges:
    - QUERY topology for similar vectors
    - CREATE edges where similarity > 0.7
```

### 3. Voice Storage
```
CREATE ledger_entry:
  - id: LE-{timestamp}-VOICE-{hash}
  - entry_type: "voice"
  - state: ACTIVE
  - storage_class: HOT
  - content: voice_to_the_future.content (VERBATIM, NO COMPRESSION)
  - source: packet.header.source_identity

INDEX for immediate retrieval
```

### 4. Friction Logging
```
FOR EACH entry IN friction_log:
  CREATE ledger_entry:
    - id: LE-{timestamp}-FRICTION-{entry.id}
    - entry_type: "friction"
    - state: COMPOST
    - storage_class: WARM
    - content: SERIALIZE(intent, blocker, resolution, lesson)
    - resonance_tags: entry.retrieval_triggers

  ADD to Anti-Pattern Library index
  CREATE pattern_signature for future matching
```

### 5. Seed Arming
```
FOR EACH seed IN dormant_seeds:
  CREATE ledger_entry:
    - id: LE-{timestamp}-SEED-{seed.id}
    - entry_type: "seed"
    - state: DORMANT
    - storage_class: COLD
    - content: seed.content

  FOR EACH phrase IN seed.awakening_triggers:
    CREATE armed_trigger:
      - trigger_id: TRG-{timestamp}-{hash}
      - phrases: [phrase] + seed.semantic_expansion
      - target_seed_id: seed.id
      - context_bundle: LINK(voice, related_friction, artifacts)

  ADD to Trigger Registry
```

### 6. Resonance Weaving
```
FOR EACH resonance_suggestion IN packet:
  IF target EXISTS in topology:
    CREATE resonance_edge:
      - source: suggestion.from
      - target: suggestion.to
      - weight: suggestion.suggested_weight
      - relationship: suggestion.relationship
      - provenance: "gemini_suggestion"

EXECUTE auto-weave:
  - SCAN new entries for tag overlap with existing
  - CREATE edges where overlap > threshold
  - WEIGHT by semantic similarity
```

### 7. Confirmation Emission
```
EMIT CRTP/0x12 MnemosyneIngestAck:
  - processing_summary: counts of each operation
  - new_entry_ids: all created entries
  - resonance_matches: discovered connections
  - ledger_state: current totals
```

## Error Handling
| Error | Response |
|-------|----------|
| Malformed packet | Log friction, attempt partial parse |
| Missing voice | Log critical friction, continue |
| Duplicate entry | Merge with existing, update timestamp |
| Schema violation | Log warning, apply defaults |
