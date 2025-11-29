# Test Suite

## Overview

This directory contains tests for the IRP Methodologies repository. As a research specification project, our tests focus on **validating the validators** and ensuring document integrity.

## Test Files

### `test_verify_integration.sh`
Tests the Chronicle Protocol cryptographic verification system.

**What it tests:**
- Verification script exists and is executable
- Script runs without errors
- Expected files are being verified
- Hash files exist and are properly formatted
- All referenced files exist

**Running the tests:**
```bash
cd tests
bash test_verify_integration.sh
```

**Expected output:**
```
Running test: Verification script exists
✓ PASSED

Running test: Verification script is executable
✓ PASSED

[... more tests ...]

=========================================
Test Summary
=========================================
Total tests run:    10
Tests passed:       10
Tests failed:       0
=========================================
All tests passed!
```

## Adding New Tests

When the codebase evolves to include Python implementation (per `IRP_Phase1_MVP_Implementation_Guide_v1.0.md`), add:

```
tests/
├── test_verify_integration.sh    # ✅ Exists - Validator tests
├── test_constitution.py          # TODO - Constitutional principles
├── test_agent.py                 # TODO - Primary agent logic
├── test_critic.py                # TODO - Reflexive critic
├── test_integration.py           # TODO - End-to-end reflexive loop
└── conftest.py                   # TODO - pytest fixtures
```

## CI/CD Integration

Tests are automatically run via GitHub Actions:
- **Workflow**: `.github/workflows/validate-integrity.yml`
- **Triggers**: Push to main/claude/** branches, Pull Requests
- **Jobs**: Document integrity verification, markdown linting, link checking

## Test Coverage Philosophy

For this research repository:
1. **Cryptographic Validation** > Traditional code coverage
2. **Specification Completeness** > Implementation completeness
3. **Empirical Evidence** > Synthetic benchmarks

See `TESTING_STRATEGY.md` for detailed testing philosophy and roadmap.
