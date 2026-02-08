#!/bin/bash
# Integration Artifact Verification Script
# Chronicle Protocol Compliance Check
# Created: 2025-10-24

echo "╔════════════════════════════════════════════════════════╗"
echo "║   INTEGRATION ARTIFACT VERIFICATION                    ║"
echo "║   Chronicle Protocol - SHA-256 Validation              ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# Color codes
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Expected hashes (documented from previous session)
declare -A EXPECTED_HASHES=(
    ["methodology_synthesis.md"]="d53cdd8538886877262003b23fce52a1e03aafa8205ebbd61c1fd3250c0bc665"
    ["OHP-20251024-103900-SYM-UPDATE.xml"]="cebba7a2d22a2799ee26b02b06fb3ca79f7df13274c8b54065088b70ab04d8e6"
    ["CROSS_PROJECT_INTEGRATION_SPECIFICATION.md"]="0ff2a4b54570f01c58b8b1c6dae3bbc5093388aa8df7113309ab3668709f7c23"
    ["FCP-20251024-104500-INTEGRATION.md"]="3f895b92621393670378c38de5b45998861511e0e73026924e0af50349ecc9a0"
    ["CRYPTO-MANIFEST-20251024-112500.md"]="c1242ea3c04fbb49bb6a0a6a01c3195057737fe799583c14fe6458f247b70dd5"
)

# Verification results
PASSED=0
FAILED=0
MISSING=0

echo "Verifying core integration artifacts..."
echo ""

# Verify each file
for FILE in "${!EXPECTED_HASHES[@]}"; do
    if [ ! -f "$FILE" ]; then
        echo -e "${RED}✗${NC} $FILE - ${YELLOW}MISSING${NC}"
        ((MISSING++))
        continue
    fi
    
    ACTUAL_HASH=$(sha256sum "$FILE" | awk '{print $1}')
    EXPECTED_HASH="${EXPECTED_HASHES[$FILE]}"
    
    if [ "$ACTUAL_HASH" == "$EXPECTED_HASH" ]; then
        echo -e "${GREEN}✓${NC} $FILE"
        echo "  Hash: $ACTUAL_HASH"
        ((PASSED++))
    else
        echo -e "${RED}✗${NC} $FILE - ${RED}HASH MISMATCH${NC}"
        echo "  Expected: $EXPECTED_HASH"
        echo "  Actual:   $ACTUAL_HASH"
        ((FAILED++))
    fi
    echo ""
done

# Summary
echo "════════════════════════════════════════════════════════"
echo "VERIFICATION SUMMARY"
echo "════════════════════════════════════════════════════════"
echo -e "Passed:  ${GREEN}$PASSED${NC}"
echo -e "Failed:  ${RED}$FAILED${NC}"
echo -e "Missing: ${YELLOW}$MISSING${NC}"
echo "────────────────────────────────────────────────────────"

if [ $FAILED -eq 0 ] && [ $MISSING -eq 0 ]; then
    echo -e "${GREEN}✅ ALL ARTIFACTS VERIFIED${NC}"
    echo "Chronicle Protocol integrity: CONFIRMED"
    exit 0
else
    echo -e "${RED}⚠️  VERIFICATION FAILED${NC}"
    echo "Integrity check failed. Do not proceed without resolving discrepancies."
    exit 1
fi
