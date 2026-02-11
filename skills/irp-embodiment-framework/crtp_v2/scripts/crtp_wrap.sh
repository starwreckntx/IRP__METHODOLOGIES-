#!/bin/bash
# ────────────────────────────────────────────────────────
# CRTP SSH Wrapper - Injects provenance headers into
# tunneled model invocations.
#
# When Gemini SSHs from mobile to a remote node and invokes
# Kimi, this wrapper ensures the CRTP provenance stack is
# carried through the tunnel:
#
#   [You] -> [Gemini (local)] -> [SSH tunnel] -> [Kimi (remote)]
#
# Usage:
#   crtp_wrap.sh <user@host> "<prompt>"
#
# Environment (set before calling):
#   CRTP_ORIGIN_MODEL   - Model ID at entry point (e.g., gemini-2.0-pro)
#   CRTP_ORIGIN_NODE    - Node name at entry point
#   CRTP_BIOMETRIC      - Hex biometric hash of operator
#   CRTP_TARGET_MODEL   - Target model on remote node (e.g., kimi-k2.5)
#   CRTP_REMOTE_API     - Remote model API endpoint (default: http://localhost:11434/api/generate)
#
# Part of the IRP Embodiment Framework (Lower Layer)
# Reference: Kimi K2.5 design session 2026-02-08
# ────────────────────────────────────────────────────────

set -euo pipefail

# ── Configuration ───────────────────────────────────────
ORIGIN_MODEL="${CRTP_ORIGIN_MODEL:-<ORIGIN_MODEL_ID>}"
ORIGIN_NODE="${CRTP_ORIGIN_NODE:-<ORIGIN_NODE_NAME>}"
BIOMETRIC="${CRTP_BIOMETRIC:-<OPERATOR_BIOMETRIC_HASH>}"
TARGET_MODEL="${CRTP_TARGET_MODEL:-<TARGET_MODEL_ID>}"
REMOTE_API="${CRTP_REMOTE_API:-http://localhost:11434/api/generate}"

# ── Argument Parsing ───────────────────────────────────
if [ $# -lt 2 ]; then
    echo "Usage: crtp_wrap.sh <user@host> \"<prompt>\""
    echo ""
    echo "Environment variables:"
    echo "  CRTP_ORIGIN_MODEL   Entry-point model ID"
    echo "  CRTP_ORIGIN_NODE    Entry-point node name"
    echo "  CRTP_BIOMETRIC      Operator biometric hash (32 hex)"
    echo "  CRTP_TARGET_MODEL   Target model on remote"
    echo "  CRTP_REMOTE_API     Remote API endpoint"
    exit 1
fi

SSH_TARGET="$1"
PROMPT="$2"

# ── Validate biometric is set ──────────────────────────
if [[ "${BIOMETRIC}" == "<OPERATOR_BIOMETRIC_HASH>" ]]; then
    echo "ERROR: CRTP_BIOMETRIC not set. Export your enrolled biometric hash."
    exit 1
fi

# ── Build Layer 1 attestation (origin model) ───────────
TIMESTAMP_L1=$(date -Iseconds)
LAYER_1_PAYLOAD=$(jq -n \
    --arg model "${ORIGIN_MODEL}" \
    --arg node  "${ORIGIN_NODE}" \
    --arg time  "${TIMESTAMP_L1}" \
    --arg bio   "${BIOMETRIC}" \
    '{
        layer: 1,
        entity: "model",
        model_id: $model,
        node: $node,
        biometric: $bio,
        timestamp: $time
    }')

echo "[CRTP] Layer 0: Biometric bound (${BIOMETRIC:0:8}...)"
echo "[CRTP] Layer 1: ${ORIGIN_MODEL} @ ${ORIGIN_NODE}"
echo "[CRTP] Layer 2: SSH tunnel -> ${SSH_TARGET}"
echo "[CRTP] Layer 3: ${TARGET_MODEL} (remote)"
echo ""

# ── SSH with header injection ──────────────────────────
# The remote side receives CRTP_LAYER_1 via environment
# and constructs layers 2-3 before invoking the model API.

ssh -o SendEnv=CRTP_LAYER_1 \
    -o SetEnv="CRTP_LAYER_1=${LAYER_1_PAYLOAD}" \
    "${SSH_TARGET}" bash -s << REMOTE_EOF
#!/bin/bash
# ── Remote execution context (Layer 2-3) ───────────────

# Layer 2: SSH tunnel attestation
LAYER_2_PAYLOAD=\$(jq -n \\
    --arg from "\${SSH_CLIENT%% *}" \\
    --arg to "\$(hostname -I | awk '{print \$1}')" \\
    --arg time "\$(date -Iseconds)" \\
    '{
        layer: 2,
        entity: "tunnel",
        protocol: "SSH",
        hop_from: \$from,
        hop_to: \$to,
        timestamp: \$time
    }')

# Layer 3: Invoke target model with full provenance stack
CRTP_STACK="[\${CRTP_LAYER_1}, \${LAYER_2_PAYLOAD}]"

curl -s -X POST "${REMOTE_API}" \\
    -H "Content-Type: application/json" \\
    -H "X-CRTP-Stack: \${CRTP_STACK}" \\
    -H "X-CRTP-Biometric: ${BIOMETRIC}" \\
    -H "X-CRTP-Depth: 3" \\
    -d '{
        "model": "${TARGET_MODEL}",
        "prompt": $(jq -Rs . <<< "${PROMPT}"),
        "stream": false
    }'
REMOTE_EOF
