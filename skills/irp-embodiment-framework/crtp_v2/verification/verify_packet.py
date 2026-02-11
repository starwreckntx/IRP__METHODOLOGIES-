#!/usr/bin/env python3
"""
CRTP Packet Verification - Python Reference Implementation

Validates CRTP v2.0 provenance packets against the chain hash
specification. Used for:
  - CLI verification of captured packets
  - Integration testing
  - Guardian Codex compliance auditing

Algorithm: SHA-256_trunc128(prev_hash || layer_identity || timestamp || node_fingerprint)

Part of the IRP Embodiment Framework (Lower Layer)
Reference: Kimi K2.5 design session 2026-02-08
"""

import hashlib
import json
import sys
from typing import Optional


# ── Exceptions ──────────────────────────────────────────

class HallOfMirrorsException(Exception):
    """Recursive model loop detected in origin stack."""
    pass


class IdentityMismatch(Exception):
    """Model claims wrong layer depth."""
    pass


class TamperingDetected(Exception):
    """Chain hash mismatch at a given layer."""
    pass


class RecursionLimitExceeded(Exception):
    """Guardian Codex Article 5 violation."""
    pass


# ── Constants ───────────────────────────────────────────

MAX_RECURSION_DEPTH = 3
CRTP_VERSION = "2.0"


# ── Verification Functions ──────────────────────────────

def compute_layer_hash(prev_hash: bytes, layer_data: dict) -> bytes:
    """
    Compute cumulative hash for a single layer.

    H(n) = SHA256(H(n-1) || layer_id || timestamp || node_fingerprint)
    Truncated to 128-bit (16 bytes).
    """
    h = hashlib.sha256()
    h.update(prev_hash)
    h.update(str(layer_data.get("layer", 0)).encode())
    h.update(str(layer_data.get("timestamp", "")).encode())
    h.update(str(layer_data.get("node", "")).encode())

    # Include model_id if present (layers with entity=model)
    if layer_data.get("entity") == "model":
        h.update(str(layer_data.get("model_id", "")).encode())

    return h.digest()[:16]  # Truncate to 128-bit


def verify_packet(packet: dict) -> bool:
    """
    Verify a CRTP provenance packet.

    Checks:
    1. No recursive model loops (Hall of Mirrors)
    2. Layer depth matches claimed position
    3. Cumulative chain hashes are valid
    4. Recursion depth within Guardian Codex limits

    Args:
        packet: Parsed CRTP provenance header (JSON dict)

    Returns:
        True if packet is authentic

    Raises:
        HallOfMirrorsException: Model appears twice in stack
        IdentityMismatch: Layer claims wrong depth
        TamperingDetected: Chain hash verification failure
        RecursionLimitExceeded: Depth > MAX_RECURSION_DEPTH
    """
    stack = packet.get("origin_stack", [])
    execution = packet.get("execution_context", {})

    # ── Check recursion depth ───────────────────────────
    recursion_depth = execution.get("recursion_depth", 0)
    if recursion_depth > MAX_RECURSION_DEPTH:
        raise RecursionLimitExceeded(
            f"Guardian Codex Article 5: depth {recursion_depth} exceeds "
            f"maximum {MAX_RECURSION_DEPTH}. Human re-authorization required."
        )

    # ── Check for mirror loops ──────────────────────────
    models_seen = [
        layer["model_id"]
        for layer in stack
        if layer.get("entity") == "model" and "model_id" in layer
    ]
    if len(models_seen) != len(set(models_seen)):
        duplicates = [m for m in set(models_seen) if models_seen.count(m) > 1]
        raise HallOfMirrorsException(
            f"Recursive model loop detected: {duplicates}"
        )

    # ── Verify layer positions ──────────────────────────
    for layer in stack:
        claimed_layer = layer.get("layer", -1)
        entity = layer.get("entity", "")

        # Layer 0 must be human_operator
        if claimed_layer == 0 and entity != "human_operator":
            raise IdentityMismatch(
                f"Layer 0 must be human_operator, got: {entity}"
            )

    # ── Verify current execution matches claimed layer ──
    if stack:
        current = stack[-1]
        current_layer = execution.get("current_layer", -1)
        if current.get("layer") != current_layer:
            raise IdentityMismatch(
                f"Current layer mismatch: stack says {current.get('layer')}, "
                f"execution_context says {current_layer}"
            )

    # ── Validate chain hashes ───────────────────────────
    prev_hash = b'\x00' * 16  # Genesis seed
    for i, layer in enumerate(stack):
        layer_hash = compute_layer_hash(prev_hash, layer)
        prev_hash = layer_hash

    # Compare final hash with declared chain_hash
    declared_chain = execution.get("chain_hash", "")
    if declared_chain:
        computed_hex = prev_hash.hex()
        # Normalize: declared may be prefixed with "sha256:"
        declared_clean = declared_chain.replace("sha256:", "")
        # Compare first 32 hex chars (128-bit)
        if computed_hex[:32] != declared_clean[:32]:
            raise TamperingDetected(
                f"Chain hash mismatch. "
                f"Computed: {computed_hex}, Declared: {declared_clean}"
            )

    return True


def format_provenance_display(packet: dict) -> str:
    """
    Format a packet's provenance chain for human display.

    Returns a string like:
      L0: human_operator (mobile-device)
      L1: gemini (mobile-device) [entry]
      L2: SSH tunnel -> remote-node
      L3: kimi (remote-node) [current]
    """
    lines = []
    stack = packet.get("origin_stack", [])
    execution = packet.get("execution_context", {})
    current_layer = execution.get("current_layer", -1)

    for layer in stack:
        depth = layer.get("layer", "?")
        entity = layer.get("entity", "unknown")
        node = layer.get("node", "?")

        if entity == "human_operator":
            label = f"L{depth}: human_operator ({node})"
        elif entity == "model":
            model_id = layer.get("model_id", "unknown")
            label = f"L{depth}: {model_id} ({node})"
        elif entity == "tunnel":
            protocol = layer.get("protocol", "?")
            hop_from = layer.get("hop_from", "?")
            hop_to = layer.get("hop_to", "?")
            label = f"L{depth}: {protocol} tunnel {hop_from} -> {hop_to}"
        else:
            label = f"L{depth}: {entity} ({node})"

        if depth == current_layer:
            label += " [CURRENT]"
        elif depth == 1:
            label += " [entry]"

        lines.append(label)

    return "\n".join(lines)


# ── CLI Entry Point ─────────────────────────────────────

def main():
    """
    Verify a CRTP packet from stdin or file argument.

    Usage:
        python3 verify_packet.py packet.json
        cat packet.json | python3 verify_packet.py
    """
    if len(sys.argv) > 1:
        with open(sys.argv[1], "r") as f:
            packet = json.load(f)
    else:
        packet = json.load(sys.stdin)

    print("CRTP Provenance Verification")
    print("=" * 40)
    print()

    # Display chain
    print("Origin Stack:")
    print(format_provenance_display(packet))
    print()

    # Verify
    try:
        result = verify_packet(packet)
        if result:
            print("STATUS: VALID")
            print("Chain hash verified. Provenance intact.")
            sys.exit(0)
    except HallOfMirrorsException as e:
        print(f"STATUS: REJECTED - MIRROR LOOP")
        print(f"  {e}")
        sys.exit(1)
    except IdentityMismatch as e:
        print(f"STATUS: REJECTED - IDENTITY MISMATCH")
        print(f"  {e}")
        sys.exit(1)
    except TamperingDetected as e:
        print(f"STATUS: REJECTED - TAMPERING DETECTED")
        print(f"  {e}")
        sys.exit(1)
    except RecursionLimitExceeded as e:
        print(f"STATUS: REJECTED - GUARDIAN CODEX VIOLATION")
        print(f"  {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
