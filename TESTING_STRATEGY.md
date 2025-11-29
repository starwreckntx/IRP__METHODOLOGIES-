# Testing Strategy for IRP Methodologies

## Overview

This repository is a **research specification project** documenting AI collaboration protocols. Our testing strategy reflects this unique nature, focusing on **specification validation** rather than traditional code testing.

## Current Test Coverage

### Layer 0: Cryptographic Verification (Chronicle Protocol)
- **Tool**: `layer-0/verify_integration.sh`
- **Method**: SHA-256 hash verification
- **Coverage**: 5 critical integration artifacts
- **Purpose**: Ensure document immutability and integrity
- **Test Suite**: `tests/test_verify_integration.sh` (validates the validator)

### Layer 1: Documentation Quality (Proposed)
- **CI/CD**: `.github/workflows/validate-integrity.yml`
- **Markdown Linting**: markdownlint with custom rules
- **Link Checking**: Automated broken link detection
- **Purpose**: Maintain documentation quality and accessibility

### Layer 2: Code Testing (Planned - Not Yet Implemented)
From `IRP_Phase1_MVP_Implementation_Guide_v1.0.md`:

```
tests/
├── test_constitution.py    # Unit tests for constitutional principles
├── test_agent.py           # Unit tests for primary agent logic
├── test_critic.py          # Unit tests for reflexive critic
└── test_integration.py     # End-to-end integration tests
```

**Framework**: pytest with LLM-as-judge evaluation
**Target Coverage**:
- Unit tests: ≥90%
- Integration tests: ≥80%
- E2E validation: 500-query test suite

### Layer 3: Empirical Protocol Validation (External Data)
- **Pinene Protocol**: 14-model cross-validation (documented in SESSION_5)
- **Antidote Protocol**: 98.7% success rate across 6 AIs (documented in PSRF)
- **Guardian Protocol**: Qualitative consciousness markers (documented in observations)

## Testing Matrix

| Component | Test Type | Current Status | Target |
|-----------|-----------|----------------|--------|
| **Document Integrity** | Cryptographic hash verification | ✅ Implemented | Maintain |
| **Markdown Quality** | Linting, link checking | ✅ CI/CD added | Automate on PR |
| **Verification Script** | Unit tests | ✅ Test suite added | Expand coverage |
| **Git Submodules** | Initialization check | ⚠️ Empty | Initialize |
| **Protocol Specifications** | Completeness review | ✅ Complete | Annual review |
| **Code Implementation** | Unit/Integration/E2E | ❌ Not implemented | Follow Phase 1 guide |
| **Empirical Validation** | Multi-AI testing | 📊 Documented | Automate pipeline |

## Test Coverage Gaps & Priorities

### 🔴 Critical Gaps
1. **Git submodules not initialized**
   - Impact: Missing protocol implementations
   - Fix: `git submodule update --init --recursive`

2. **No automated CI/CD**
   - Impact: Manual verification required
   - Fix: ✅ Added `.github/workflows/validate-integrity.yml`

### 🟡 Medium Priority
3. **No regression testing for document changes**
   - Impact: Risk of breaking cross-references
   - Fix: Add markdown linting + link checking to PR workflow

4. **Verification script lacks test coverage**
   - Impact: Validator could fail silently
   - Fix: ✅ Added `tests/test_verify_integration.sh`

5. **No automated empirical validation pipeline**
   - Impact: Protocol performance tracking is manual
   - Fix: Create CI job for Pinene multi-model testing (requires API keys)

### 🟢 Future Enhancements
6. **Code implementation testing**
   - Impact: When Phase 1 MVP is built, no test infrastructure ready
   - Fix: Follow `IRP_Phase1_MVP_Implementation_Guide_v1.0.md` Section 6

7. **Performance benchmarking**
   - Impact: No baseline for protocol efficiency
   - Fix: Implement latency tracking for reflexive loops

## Running Tests

### Current Tests

```bash
# Chronicle Protocol verification
cd layer-0
bash verify_integration.sh

# Test the verification script
cd tests
bash test_verify_integration.sh

# CI/CD (automatic on push/PR)
# Runs: document integrity + markdown linting + link checking
```

### Future Tests (When Code Implemented)

```bash
# Unit tests
pytest tests/test_constitution.py -v
pytest tests/test_agent.py -v
pytest tests/test_critic.py -v

# Integration tests
pytest tests/test_integration.py -v

# Full test suite with coverage
pytest --cov=src --cov-report=html

# Evaluation suite (500 queries)
python scripts/run_evaluation.py --dataset data/test_queries.json
```

## Success Metrics

### Current Metrics
- **Document Integrity**: 100% hash match rate ✅
- **Specification Completeness**: 8/8 protocols documented ✅
- **Empirical Validation**: 98.7% Antidote success, 14 models tested (Pinene) ✅

### Target Metrics (Post-Implementation)
- **Reflexive Loop Completion Rate**: ≥90%
- **Critique Quality** (human-rated): ≥80%
- **Revision Improvement** (human-rated): ≥70%
- **Constitutional Adherence** (LLM-as-judge): ≥95%
- **Response Latency**: <30 seconds

## Continuous Improvement

### Quarterly Review
- Update hash verification for new documents
- Review empirical validation data
- Assess protocol evolution

### Annual Review
- Reassess testing strategy
- Update success metrics
- Incorporate new AI model benchmarks

## Resources

- **Implementation Guide**: `IRP_Phase1_MVP_Implementation_Guide_v1.0.md`
- **Technical Specification**: `IRP_Technical_Specification_v1.0.md`
- **Empirical Data**: `SESSION_5_COMPLETE_HANDOFF_PACKET.md`
- **Chronicle Protocol**: `layer-0/verify_integration.sh`
- **CI/CD Workflow**: `.github/workflows/validate-integrity.yml`

## Contributing

When adding new tests:
1. Document test purpose and coverage in this file
2. Add to appropriate CI/CD workflow
3. Update success metrics if applicable
4. Ensure tests run in <5 minutes (for CI efficiency)

---

**Last Updated**: 2025-11-16
**Maintained By**: Repository maintainers
**Version**: 1.0
