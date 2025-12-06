# Context Surfacing Procedure

## Purpose
Deliver relevant context from ledger to active instance.

## Triggers
- Session initialization
- Trigger phrase detection
- Explicit `/ledger surface` command
- Semantic query match

## Procedure

### 1. Context Assessment
```
DETERMINE surfacing_reason:
  - session_init: Surface most recent HOT context
  - trigger_phrase: Surface specific seed bundle
  - explicit_query: Surface by semantic match
  - pattern_match: Surface anti-pattern alert
```

### 2. HOT Context Retrieval
```
IF session_init:
  QUERY ledger WHERE storage_class = HOT
  ORDER BY relevance_score DESC, created DESC
  LIMIT 3

  SELECT primary_voice = highest relevance
  SELECT supporting_voices = remainder
```

### 3. Trigger Checking
```
SCAN input FOR armed trigger phrases:
  - exact_match: phrase in input
  - fuzzy_match: levenshtein_distance < 2
  - semantic_match: embedding_similarity > 0.85

IF match_found:
  EXECUTE awakening_flow (see awaken procedure)
  INCLUDE awakened_seed in bundle
```

### 4. Topology Traversal
```
FROM current_context_vector:
  FIND nearby_nodes WHERE edge_weight > 0.6
  COLLECT artifacts, voices, seeds within 2 hops
  RANK by cumulative_weight * recency_factor
```

### 5. Anti-Pattern Scanning
```
EXTRACT intent_signature FROM current_context
QUERY Anti-Pattern Library for matching patterns
IF match_confidence > 0.7:
  INCLUDE friction in bundle
  SET alert_flag = true
```

### 6. Bundle Assembly
```
CREATE voice_bundle:
  - primary_voice: highest_relevance HOT content
  - supporting_voices: additional HOT content
  - active_artifacts: nearby topology nodes
  - armed_triggers: relevant to current context
  - relevant_friction: matching anti-patterns
  - topology_context: graph neighborhood

EMIT bundle to active instance
```

## Output
- Voice Bundle (XML)
- Optional: Anti-Pattern Alert (if triggered)
- Optional: Seed Awakening (if triggered)
