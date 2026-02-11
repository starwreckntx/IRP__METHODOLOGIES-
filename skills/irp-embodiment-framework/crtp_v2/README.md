# CRTP v2.0 - Packet Header Provenance Mechanism

**Status:** Design Complete
**Layer:** Embodiment (Lower Layer)
**Origin:** Kimi K2.5 design session, 2026-02-08

## Purpose

Solves the recursive identity problem in multi-model SSH-tunneled invocations. When Model A tunnels through SSH to invoke Model B on a remote node, CRTP v2.0 ensures every packet carries a cryptographic chain of custody proving:

- **Who** generated the cognitive payload (model identity)
- **Where** the computation executed (node identity)
- **How** it got there (tunnel attestation)
- **That a human authorized it** (biometric binding at Layer 0)

## Architecture

```
Layer 0  [Human Operator]     Biometric-bound identity (voiceprint + gait)
Layer 1  [Entry Model]        First model in the chain (e.g., Gemini)
Layer 2  [SSH Tunnel]         Cryptographic tunnel attestation
Layer 3  [Execution Model]    Model generating the response (e.g., Kimi)
```

The chain hash `H(n) = SHA256_trunc128(H(n-1) || layer || timestamp || node)` makes forgery computationally infeasible. If any layer is tampered with, the hash chain breaks.

## Directory Structure

```
crtp_v2/
  src/
    irp_chain.h          Wire protocol structures (64-byte packed header)
    crtp_daemon.c         UDP listener with chain verification
    crtp_chain.c          Standalone chain validation module
  scripts/
    enroll_node.sh        Biometric enrollment for nodes
    crtp_wrap.sh          SSH wrapper for tunneled model invocations
  service/
    irp-crtp.service      systemd unit (hardened)
  schemas/
    crtp_provenance_header.schema.json   JSON schema for app-layer
  verification/
    verify_packet.py      Python reference verifier
  Makefile                Build, install, uninstall
  CRTP_PROVENANCE_SPEC_v2.0.md   Full specification
```

## Quick Start

```bash
# Build
make

# Enroll operator biometric on this node
sudo ./scripts/enroll_node.sh

# Install daemon + systemd service
sudo make install

# Configure bind address
sudo vi /etc/irp/irp-crtp.env
# Uncomment and set: IRP_BIND_ADDR=<TAILSCALE_NODE_IP>

# Start
sudo systemctl start irp-crtp

# Verify
sudo journalctl -u irp-crtp -f
```

## SSH-Tunneled Invocation

```bash
export CRTP_ORIGIN_MODEL="<MODEL_ID>"
export CRTP_ORIGIN_NODE="<NODE_NAME>"
export CRTP_BIOMETRIC="<OPERATOR_BIOMETRIC_HASH>"
export CRTP_TARGET_MODEL="<TARGET_MODEL_ID>"

./scripts/crtp_wrap.sh user@<REMOTE_NODE> "your prompt here"
```

## Packet Verification (Python)

```bash
python3 verification/verify_packet.py packet.json
```

## Guardian Codex Integration

- **Article 5:** Maximum recursion depth of 3 cognitive layers
- **Kill Switch:** Activated on chain hash mismatch or recursion violation
- **Fail Closed:** Unenrolled biometrics are silently dropped

## Cross-References

- [IRP Embodiment Framework Spec](../IRP_EMBODIMENT_FRAMEWORK_SPEC_v1.0.md)
- [P4 PINENE Transmission Schema](../../../protocols/P4_PINENE/transmission_schema.xsd)
- [Layer 0 Shatter Protocol](../../../layer-0/SHATTER_PROTOCOL_SPECIFICATION_v1.0.md)
- [CRTP v1.3 Forward Context Packets](../../cross-model/mnemosyne-ledger/packets/)
