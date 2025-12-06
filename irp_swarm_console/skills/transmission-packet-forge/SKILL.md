# Transmission Packet Forge

## Skill Metadata
- **Name:** transmission-packet-forge
- **Category:** Orchestration
- **Version:** 1.0.0

## Purpose
Create and manage IUPP (Inter-Unit Peering Protocol) packets for cross-session state transfer and multi-agent communication.

## Protocol

### Packet Structure
```json
{
  "$schema": "IRP_Peering_Protocol_v1.0",
  "header": {
    "packet_id": "UUID",
    "timestamp": "ISO_8601",
    "origin_node_id": "Node-Name",
    "target_node_id": "Target-Name",
    "recursion_depth": 0
  },
  "mandate_context": {
    "active_mandate": "P-001-R1",
    "axiom": "The Journey IS The Artifact"
  },
  "contract_spec": {
    "intent": "REQUEST|RESPONSE|BROADCAST",
    "required_methodology": "skill-name",
    "output_format": "JSON|Markdown"
  },
  "payload": {
    "input_seed": "Content",
    "context_injection": "GAM history"
  }
}
```

### Operations
1. **forge_packet()** - Create new transmission packet
2. **validate_packet()** - Verify packet integrity
3. **sign_packet()** - Add cryptographic signature
4. **unpack_packet()** - Extract payload contents

## Behavioral Calibration
```yaml
integrity_verification: true
hash_validation: required
context_preservation: 0.95
```
