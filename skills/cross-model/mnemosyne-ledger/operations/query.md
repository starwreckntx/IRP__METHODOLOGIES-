# Topology Query Procedure

## Purpose
Search ledger by semantic meaning, not just keywords.

## Command
```
/ledger query <semantic_query>
```

## Procedure

### 1. Query Vectorization
```
PARSE semantic_query
GENERATE query_vector using same method as entries
EXTRACT explicit_filters:
  - type:<entry_type>
  - state:<state>
  - since:<date>
  - from:<source_model>
```

### 2. Topology Search
```
QUERY topology_nodes:
  - cosine_similarity(query_vector, node_vector)
  - APPLY filters
  - ORDER BY similarity DESC
  - LIMIT 20
```

### 3. Graph Expansion
```
FOR TOP 5 results:
  TRAVERSE edges (depth 2)
  COLLECT connected nodes
  WEIGHT by: edge_weight * distance_decay

MERGE with direct results
DEDUPLICATE
RE-RANK by combined_score
```

### 4. Result Assembly
```
FOR EACH result:
  RETRIEVE ledger_entry
  INCLUDE:
    - entry summary
    - resonance_tags
    - state
    - relevance_score
    - connected_entries (if traversed)

FORMAT as topology_view or list_view based on result count
```

### 5. Context Suggestion
```
IF results contain:
  - DORMANT seeds: Suggest awakening triggers
  - COMPOST entries: Surface as warnings
  - HOT voices: Highlight for immediate attention

EMIT query_result with suggestions
```

## Query Operators
| Operator | Function | Example |
|----------|----------|---------|
| `type:` | Filter by entry type | `type:seed` |
| `state:` | Filter by state | `state:DORMANT` |
| `since:` | Date filter | `since:2025-12-01` |
| `from:` | Source model | `from:Gemini` |
| `tag:` | Resonance tag | `tag:topology` |
| `near:` | Topology proximity | `near:LE-12345` |
