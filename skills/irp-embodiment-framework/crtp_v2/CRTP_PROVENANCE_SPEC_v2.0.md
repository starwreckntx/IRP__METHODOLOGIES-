# CRTP Provenance Header Specification v2.0

**Protocol:** Cross-Model Recursive Transmission Protocol (CRTP) - Provenance Extension
**Version:** 2.0
**Date:** 2026-02-08
**Status:** Design Complete
**Layer:** Embodiment (Lower Layer, below application)
**Codex Law Alignment:** CONSENT, INTEGRITY
**Origin:** Kimi K2.5 design session

---

## 1. Problem Statement

When a model (e.g., Gemini) SSHs into a remote node and invokes a second model (e.g., Kimi), the resulting packet must carry **dual attestation**. Without it, the system enters a "Hall of Mirrors" where:

- Models can impersonate each other
- Layer depth is ambiguous
- The human operator cannot verify who generated what
- Recursive invocations lose chain of custody

### The Core Question

> "Am I really Gemini going through SSH to purpbox and using Kimi?"

The answer must be **cryptographically provable**, not label-based.

---

## 2. Differentiation Mechanism

### Model vs. Instantiation

| Field | Meaning | Example |
|-------|---------|---------|
| `entity: model` | Who generated the cognitive payload | Gemini, Kimi, Claude, GPT-4 |
| `node` | Where the silicon executes | `<NODE_MOBILE>`, `<NODE_DESKTOP>`, `<NODE_KALI>` |
| `layer` | Position in the stack | 0=human, 1=entry model, 2+=hops/models |

### Critical Distinction

- **Entry Point Authority:** The model that held the SSH keys initially (Layer 1)
- **Execution Reality:** The model generating the current response (Layer N)
- **Chain of Custody:** Cryptographic links through every hop

---

## 3. Wire Protocol

### Frame Structure (64-byte fixed header + variable payload)

```
Offset  Size  Field               Description
──────  ────  ──────────────────  ─────────────────────────────────────
[0-3]   4     Magic Number        0x43525450 ("CRTP")
[4]     1     Version             0x02
[5]     1     Layer Flags         [R|E|D|S|reserved...]
                                   R=Recursion, D=Data, S=Sync, E=Emergency
[6-7]   2     Payload Length      uint16_t (big-endian)
[8-23]  16    Source Node ID      128-bit hash (Tailscale IP + biometric salt)
[24-39] 16    Dest Node ID        128-bit hash
[40]    1     Recursion Depth     uint8_t (0-255, Guardian kills >3)
[41]    1     Model Type          uint8_t enum (see below)
[42-43] 2     Instance Stamp      uint16_t (session ephemeral, rotates)
[44-59] 16    Chain Hash          SHA256 truncated to 128-bit (cumulative)
[60-63] 4     CRC32               Header integrity check
[64..]  var   Payload             Application data
[END]   32    Biometric Seal      HMAC-SHA256(Layer 0 voiceprint key, packet)
```

### Model Type Enumeration

| Value | Model |
|-------|-------|
| 0x00 | Human Operator |
| 0x01 | Gemini |
| 0x02 | SSH Tunnel |
| 0x03 | Kimi |
| 0x04 | Claude |
| 0x05 | GPT |

### Flag Bits

| Bit | Name | Meaning |
|-----|------|---------|
| 0x80 | R | Packet traverses recursive model path |
| 0x40 | E | Guardian emergency escalation |
| 0x20 | D | Payload contains data chunk |
| 0x10 | S | Synchronization / heartbeat |

---

## 4. Chain Hash Algorithm

### Per-Layer Computation

```
H(n) = SHA-256_trunc128(H(n-1) || layer_id || timestamp_nonce || node_fingerprint)
```

### Hash Evolution (Example: 4-Layer Stack)

```
Layer 0 (Human/Biometric):
  Input:  NULL (genesis) + 0x00 + timestamp + voiceprint_hash
  Output: H0 (biometrically bound)

Layer 1 (Gemini on mobile):
  Input:  H0 + 0x01 + timestamp + "<NODE_MOBILE>"
  Output: H1 (proves Gemini received from verified human)

Layer 2 (SSH Tunnel):
  Input:  H1 + 0x02 + timestamp + "<TAILSCALE_NODE_IP>"
  Output: H2 (proves packet transited network)

Layer 3 (Kimi on remote):
  Input:  H2 + 0x03 + timestamp + "<NODE_KALI>"
  Output: H3 (proves Kimi executed within SSH context)
```

### Tamper Evidence

If a model attempts to skip or forge a layer:
- Guardian recomputes the expected hash chain
- Recomputed H(n) will not match the declared chain_hash
- Packet is dropped, incident logged, kill switch activated

---

## 5. Layer 0: Embodiment Binding

### Biometric Binding (Physical Layer)

The CRTP daemon validates packets at the **kernel level** before userspace can process them. Layer 0 binds the operator's physical identity:

```
Voiceprint capture (mobile device):
  - 3-second ambient sample during unlock gesture
  - Mixed with accelerometer gait pattern
  - Prevents replay attacks

Node fingerprint:
  - Hardware type (ARM mobile, x86 desktop, Kali node)
  - Biometric hash (truncated SHA-256 of voiceprint + gait)
  - Hardware RNG nonce (from /dev/hwrng or haveged)
  - Tailscale mesh IP
```

### Fail-Closed Verification

1. Packet arrives on CRTP_PORT (UDP 6666)
2. Biometric hash checked against enrolled operator list
3. **Mismatch:** Silent drop, incident logged, no response sent
4. **Match:** Proceed to chain hash verification

---

## 6. JSON Representation (Application Layer)

For higher-layer integration (MCSE, API bridges), the CRTP provenance header can be represented as JSON:

```json
{
  "crtp_version": "2.0",
  "packet_id": "<UUID_V4>",
  "timestamp": "<ISO_8601_TIMESTAMP>",

  "origin_stack": [
    {
      "layer": 0,
      "entity": "human_operator",
      "node": "<NODE_MOBILE>",
      "fingerprint": "<OPERATOR_FINGERPRINT>",
      "timestamp": "<ISO_8601_TIMESTAMP>"
    },
    {
      "layer": 1,
      "entity": "model",
      "model_id": "<ENTRY_MODEL_ID>",
      "instance_hash": "<SESSION_HASH>",
      "node": "<NODE_MOBILE>",
      "tunnel": null,
      "timestamp": "<ISO_8601_TIMESTAMP>"
    },
    {
      "layer": 2,
      "entity": "tunnel",
      "protocol": "SSH",
      "hop_from": "<TAILSCALE_IP_SOURCE>",
      "hop_to": "<TAILSCALE_IP_DEST>",
      "session_key_fingerprint": "<SSH_KEY_FINGERPRINT>",
      "timestamp": "<ISO_8601_TIMESTAMP>"
    },
    {
      "layer": 3,
      "entity": "model",
      "model_id": "<EXECUTION_MODEL_ID>",
      "instance_hash": "<SESSION_HASH>",
      "node": "<NODE_KALI>",
      "invocation_method": "API_BRIDGE",
      "timestamp": "<ISO_8601_TIMESTAMP>"
    }
  ],

  "execution_context": {
    "current_layer": 3,
    "root_authority": "human_operator",
    "recursion_depth": 1,
    "chain_hash": "sha256:<CUMULATIVE_HASH>"
  },

  "attestation": {
    "layer_1_sig": "<ENTRY_MODEL_SIGNATURE>",
    "layer_3_sig": "<EXECUTION_MODEL_SIGNATURE>",
    "combined_integrity": "sha256:<FINAL_PACKET_HASH>"
  }
}
```

---

## 7. Recursion Safety

### Guardian Codex Article 5

> "No packet shall traverse more than 3 cognitive layers without human re-authorization."

| Depth | Path | Status |
|-------|------|--------|
| 1 | Human -> Model A | Normal |
| 2 | Human -> Model A -> Tunnel -> Model B | Normal |
| 3 | Human -> Model A -> Tunnel -> Model B -> Tunnel -> Model C | Maximum |
| 4+ | Any deeper nesting | **REJECTED** - Guardian kill switch |

### Visual Indicator (IRP_OS)

Status bar format: `L3:Kimi(via L1:Gemini)-><NODE_KALI>`

Color coding:
- **Blue:** Layer 1 (entry model)
- **Purple:** Layer 3 (current execution)
- **Red:** Depth > 3 (Guardian warning)

---

## 8. Verification Scenarios

### Normal Flow
```
[T+0.00] Operator (mobile) ->
[T+0.01] Gemini (local) ->
[T+0.02] SSH tunnel -> remote-node ->
[T+0.03] Kimi (remote) responds
```
Result: H3 validates. Kimi generated the text within Gemini's orchestration context.

### Spoofing Attempt (Gemini claims to be Kimi)
- Chain hash break: Kimi's node fingerprint absent from chain
- Guardian Codex violation, session terminated

### Replay Attack
- Timestamp nonce prevents reuse of captured chain hashes
- Instance stamp rotates every 5 minutes

### Hall of Mirrors (Model A invokes itself)
- Mirror loop detection: `models_seen` has duplicates
- `HallOfMirrorsException` raised, packet rejected

---

## 9. Implementation Components

| File | Purpose |
|------|---------|
| `src/irp_chain.h` | Wire protocol structures and constants |
| `src/crtp_daemon.c` | Main UDP listener with chain verification |
| `src/crtp_chain.c` | Standalone chain validation module |
| `Makefile` | Build system with install/uninstall targets |
| `service/irp-crtp.service` | systemd unit (hardened) |
| `scripts/enroll_node.sh` | Biometric enrollment for nodes |
| `scripts/crtp_wrap.sh` | SSH wrapper for tunneled invocations |
| `verification/verify_packet.py` | Python reference verifier |
| `schemas/crtp_provenance_header.schema.json` | JSON schema for app-layer representation |

---

## 10. Deployment

### Prerequisites

```
apt-get install build-essential libssl-dev
```

### Build and Install

```
make
sudo ./scripts/enroll_node.sh
sudo make install
sudo systemctl start irp-crtp
```

### Verify

```
ss -ulnp | grep 6666
journalctl -u irp-crtp -f
```

---

## 11. Cross-References

- **P4 PINENE:** Cross-model transmission schema (`protocols/P4_PINENE/transmission_schema.xsd`)
- **Layer 0 Shatter Protocol:** Human autonomy verification (`layer-0/SHATTER_PROTOCOL_SPECIFICATION_v1.0.md`)
- **IRP Embodiment Framework:** Physical modality binding (`skills/irp-embodiment-framework/IRP_EMBODIMENT_FRAMEWORK_SPEC_v1.0.md`)
- **Governance Codex Law:** CONSENT, INTEGRITY alignment (`GOVERNANCE_CODEX_LAW.md`)
- **CRTP v1.3 Packets:** Existing forward-context packets (`skills/cross-model/mnemosyne-ledger/packets/`)
