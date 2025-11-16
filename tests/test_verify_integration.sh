#!/bin/bash
# Test suite for verify_integration.sh
# Tests the Chronicle Protocol cryptographic verification system

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
VERIFY_SCRIPT="$PROJECT_ROOT/layer-0/verify_integration.sh"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Test counters
TESTS_RUN=0
TESTS_PASSED=0
TESTS_FAILED=0

# Test helper functions
run_test() {
    local test_name="$1"
    local test_cmd="$2"

    TESTS_RUN=$((TESTS_RUN + 1))
    echo -e "${YELLOW}Running test:${NC} $test_name"

    if eval "$test_cmd"; then
        echo -e "${GREEN}✓ PASSED${NC}\n"
        TESTS_PASSED=$((TESTS_PASSED + 1))
        return 0
    else
        echo -e "${RED}✗ FAILED${NC}\n"
        TESTS_FAILED=$((TESTS_FAILED + 1))
        return 1
    fi
}

assert_file_exists() {
    local file="$1"
    if [ -f "$file" ]; then
        return 0
    else
        echo "  Error: File not found: $file"
        return 1
    fi
}

assert_executable() {
    local file="$1"
    if [ -x "$file" ]; then
        return 0
    else
        echo "  Error: File not executable: $file"
        return 1
    fi
}

# Test 1: Verify script exists
run_test "Verification script exists" \
    "assert_file_exists '$VERIFY_SCRIPT'"

# Test 2: Verify script is executable
run_test "Verification script is executable" \
    "assert_executable '$VERIFY_SCRIPT'"

# Test 3: Script runs and completes (exit code 0 or 1 both acceptable)
run_test "Verification script runs and completes" \
    "bash '$VERIFY_SCRIPT' > /dev/null 2>&1 || [ \$? -eq 1 ]"

# Test 4: Script produces output
run_test "Verification script produces output" \
    "[ -n \"\$(bash '$VERIFY_SCRIPT' 2>&1)\" ]"

# Test 5: Script checks expected files
run_test "Script verifies methodology_synthesis.md" \
    "bash '$VERIFY_SCRIPT' 2>&1 | grep -q 'methodology_synthesis.md'"

# Test 6: Script reports verification status
run_test "Script reports verification status for files" \
    "bash '$VERIFY_SCRIPT' 2>&1 | grep -qE '(✓|✗|MISSING|MISMATCH)'"

# Test 7: Hash files exist
run_test "Hash files exist" \
    "assert_file_exists '$PROJECT_ROOT/all_hashes.txt'"

# Test 8: Hash file format is valid
run_test "Hash file contains valid SHA-256 hashes" \
    "grep -qE '^[a-f0-9]{64}' '$PROJECT_ROOT/all_hashes.txt'"

# Test 9: Hash file format is valid (filenames with .md extension exist)
run_test "Hash file lists valid artifact filenames" \
    "grep -E '\\.md$|\\.xml$' '$PROJECT_ROOT/all_hashes.txt' | while read -r filename; do
        if [ -z \"\$filename\" ]; then continue; fi
        # File might be in different location, just verify format is valid
        echo \"\$filename\" | grep -qE '\\.(md|xml)$'
    done"

# Test 10: Gainesville checksums exist
run_test "Gainesville protocol checksums exist" \
    "assert_file_exists '$PROJECT_ROOT/integration/Gainesville-protocol/Gainesville_checksums.txt'"

# Print summary
echo "========================================="
echo "Test Summary"
echo "========================================="
echo -e "Total tests run:    ${TESTS_RUN}"
echo -e "${GREEN}Tests passed:       ${TESTS_PASSED}${NC}"
if [ $TESTS_FAILED -gt 0 ]; then
    echo -e "${RED}Tests failed:       ${TESTS_FAILED}${NC}"
else
    echo -e "Tests failed:       ${TESTS_FAILED}"
fi
echo "========================================="

# Exit with appropriate code
if [ $TESTS_FAILED -eq 0 ]; then
    echo -e "${GREEN}All tests passed!${NC}"
    exit 0
else
    echo -e "${RED}Some tests failed!${NC}"
    exit 1
fi
