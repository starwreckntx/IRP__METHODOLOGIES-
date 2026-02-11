#!/bin/bash
# ────────────────────────────────────────────────────────
# IRP Biometric Enrollment Script
#
# Enrolls an operator's biometric hash for CRTP packet
# validation on this node. The daemon will reject any
# packet whose src_biometric does not match an enrolled
# hash (fail-closed).
#
# Usage:
#   sudo ./enroll_node.sh
#   sudo ./enroll_node.sh --hash <32_hex_chars>
#
# Part of the IRP Embodiment Framework (Lower Layer)
# ────────────────────────────────────────────────────────

set -euo pipefail

BIOMETRIC_DIR="/etc/irp"
BIOMETRIC_FILE="${BIOMETRIC_DIR}/enrolled.biometric"
ENV_FILE="${BIOMETRIC_DIR}/irp-crtp.env"

echo "═══ IRP CRTP Node Enrollment ═══"
echo ""

# Ensure running as root
if [ "$(id -u)" -ne 0 ]; then
    echo "ERROR: Must run as root (biometric keys stored in /etc/irp/)"
    exit 1
fi

# Create config directory
mkdir -p "${BIOMETRIC_DIR}"
chmod 700 "${BIOMETRIC_DIR}"

# Accept hash from argument or prompt
if [ "${1:-}" = "--hash" ] && [ -n "${2:-}" ]; then
    VOICEPRINT="$2"
else
    echo "Enter 32-character hex voiceprint hash"
    echo "(SHA-256 truncated from operator biometric capture):"
    echo ""
    read -r VOICEPRINT
fi

# Validate hex format
if [[ ! "${VOICEPRINT}" =~ ^[0-9a-fA-F]{32}$ ]]; then
    echo "ERROR: Invalid hash. Must be exactly 32 hex characters."
    echo "Example: a7f3b2e49d2c8e1f4b5a6c7de8f9a0b1"
    exit 1
fi

# Normalize to lowercase
VOICEPRINT=$(echo "${VOICEPRINT}" | tr '[:upper:]' '[:lower:]')

# Check for duplicate enrollment
if [ -f "${BIOMETRIC_FILE}" ]; then
    if grep -q "${VOICEPRINT}" "${BIOMETRIC_FILE}" 2>/dev/null; then
        echo "NOTICE: This biometric hash is already enrolled."
        exit 0
    fi
fi

# Append to enrolled biometrics (supports multiple operators)
echo "${VOICEPRINT}" >> "${BIOMETRIC_FILE}"
chmod 600 "${BIOMETRIC_FILE}"

# Create environment file for systemd if it doesn't exist
if [ ! -f "${ENV_FILE}" ]; then
    cat > "${ENV_FILE}" << 'ENVEOF'
# IRP CRTP Daemon Environment
# Set IRP_BIND_ADDR to the Tailscale mesh IP of this node.
# Leave commented to bind to all interfaces (0.0.0.0).
#
# IRP_BIND_ADDR=<TAILSCALE_NODE_IP>
ENVEOF
    chmod 600 "${ENV_FILE}"
    echo "Created ${ENV_FILE} - edit to set bind address."
fi

echo ""
echo "═══ Enrollment Complete ═══"
echo "Enrolled: ${VOICEPRINT}"
echo "File:     ${BIOMETRIC_FILE}"
echo ""
echo "Guardian will reject packets not signed by this biometric."
echo "Restart daemon to pick up changes: sudo systemctl restart irp-crtp"
