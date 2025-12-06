# Resonance Weaving Procedure

## Purpose
Create and maintain semantic connections in topology graph.

## Triggers
- New ledger entry created
- Explicit `/ledger weave` command
- Periodic topology maintenance
- Gemini resonance suggestion

## Procedure

### 1. Vector Generation
```
FOR new_entry:
  GENERATE semantic_vector FROM:
    - resonance_tags (primary)
    - content keywords (secondary)
    - entry_type category (tertiary)

  NORMALIZE vector to unit length
```

### 2. Similarity Search
```
QUERY topology FOR existing_nodes
CALCULATE similarity:
  - cosine_similarity(new_vector, existing_vector)
  - tag_overlap_ratio
  - lineage_connection_bonus

COMBINE weighted:
  similarity = 0.6 * cosine + 0.3 * tag_overlap + 0.1 * lineage_bonus
```

### 3. Edge Creation
```
FOR EACH candidate WHERE similarity > 0.7:
  CREATE resonance_edge:
    - source: new_node
    - target: candidate_node
    - weight: similarity
    - relationship: INFER from entry_types
    - provenance: "auto"
    - state: ACTIVE

BIDIRECTIONAL default for resonance edges
```

### 4. Relationship Inference
```
INFER relationship_type:
  - artifact ↔ artifact: "isomorphic" | "extends" | "contradicts"
  - artifact ↔ voice: "contextualizes"
  - artifact ↔ seed: "germinates" | "supports"
  - artifact ↔ friction: "resolved_by" | "caused"
  - seed ↔ friction: "warned_against"
  - voice ↔ seed: "predicted"
```

### 5. Thread Identification
```
IF edge creates path > 3 nodes:
  EVALUATE as potential thread:
    - consistent relationship_types
    - coherent semantic theme
    - cross-session span

  IF thread_criteria_met:
    CREATE resonance_thread entry
    ASSIGN thread_id: RT-{count}
    TAG all member nodes
```

### 6. Weight Decay (Maintenance)
```
PERIODIC (daily):
  FOR EACH edge WHERE last_traversed > 30 days:
    weight = weight * 0.95

  IF weight < 0.3:
    state = LATENT

  IF weight < 0.1 AND traversal_count < 2:
    state = SEVERED (soft delete)
```

## Manual Weaving
```
/ledger weave <from_id> <to_id> <weight> [relationship]

VALIDATE both nodes exist
CREATE edge with provenance = "manual"
SKIP similarity threshold check
LOG as explicit connection
```
