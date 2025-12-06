"""
IUPP Protocol Module
====================
Inter-Unit Peering Protocol packet builder and validator.
Constructs valid IUPP JSON packets for IRP swarm communication.
"""

import uuid
import json
import hashlib
from datetime import datetime
from typing import Dict, Any, Optional, List


class IUPPPacketBuilder:
    """
    Builder for IUPP (Inter-Unit Peering Protocol) packets.
    Follows the IRP_Peering_Protocol_v1.0 schema.
    """
    
    SCHEMA_VERSION = "IRP_Peering_Protocol_v1.0"
    DEFAULT_MANDATE = "P-001-R1"
    DEFAULT_AXIOM = "The Journey IS The Artifact"
    
    def __init__(self, origin_node_id: str = "Orchestrator-Main"):
        """
        Initialize the packet builder.
        
        Args:
            origin_node_id: Default origin node identifier
        """
        self.origin_node_id = origin_node_id
        self.recursion_depth = 0
    
    def build_packet(
        self,
        target_node_id: str,
        input_seed: str,
        required_methodology: str,
        context_injection: str = "",
        intent: str = "REQUEST",
        output_format: str = "JSON",
        active_mandate: str = None,
        axiom: str = None,
        metadata: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """
        Build a complete IUPP packet.
        
        Args:
            target_node_id: Target node identifier
            input_seed: Primary content/query for the target
            required_methodology: Methodology the target should use
            context_injection: GAM context to inject
            intent: Packet intent (REQUEST, RESPONSE, BROADCAST)
            output_format: Expected output format (JSON, Markdown)
            active_mandate: Override default mandate
            axiom: Override default axiom
            metadata: Additional metadata to include
            
        Returns:
            Complete IUPP packet as dictionary
        """
        packet_id = str(uuid.uuid4())
        timestamp = datetime.utcnow().isoformat() + "Z"
        
        packet = {
            "$schema": self.SCHEMA_VERSION,
            "header": {
                "packet_id": packet_id,
                "timestamp": timestamp,
                "origin_node_id": self.origin_node_id,
                "target_node_id": target_node_id,
                "recursion_depth": self.recursion_depth
            },
            "mandate_context": {
                "active_mandate": active_mandate or self.DEFAULT_MANDATE,
                "axiom": axiom or self.DEFAULT_AXIOM
            },
            "contract_spec": {
                "intent": intent,
                "required_methodology": required_methodology,
                "output_format": output_format
            },
            "payload": {
                "input_seed": input_seed,
                "context_injection": context_injection or "No prior context"
            }
        }
        
        # Add optional metadata
        if metadata:
            packet["metadata"] = metadata
        
        # Add integrity hash
        packet["integrity"] = {
            "payload_hash": self._compute_payload_hash(packet["payload"]),
            "algorithm": "SHA-256"
        }
        
        return packet
    
    def build_request_packet(
        self,
        target_node_id: str,
        query: str,
        methodology: str,
        gam_context: str = ""
    ) -> Dict[str, Any]:
        """
        Convenience method to build a REQUEST packet.
        
        Args:
            target_node_id: Target node
            query: User query/input
            methodology: Required methodology
            gam_context: Optional GAM context
            
        Returns:
            REQUEST packet
        """
        return self.build_packet(
            target_node_id=target_node_id,
            input_seed=query,
            required_methodology=methodology,
            context_injection=gam_context,
            intent="REQUEST"
        )
    
    def build_response_packet(
        self,
        target_node_id: str,
        result: str,
        original_packet_id: str,
        methodology: str
    ) -> Dict[str, Any]:
        """
        Build a RESPONSE packet in reply to a request.
        
        Args:
            target_node_id: Node to send response to
            result: Result content
            original_packet_id: ID of the original request packet
            methodology: Methodology that was used
            
        Returns:
            RESPONSE packet
        """
        packet = self.build_packet(
            target_node_id=target_node_id,
            input_seed=result,
            required_methodology=methodology,
            intent="RESPONSE"
        )
        
        # Add reference to original packet
        packet["header"]["in_reply_to"] = original_packet_id
        
        return packet
    
    def build_broadcast_packet(
        self,
        message: str,
        methodology: str = "general"
    ) -> Dict[str, Any]:
        """
        Build a BROADCAST packet for all nodes.
        
        Args:
            message: Broadcast message content
            methodology: Methodology context
            
        Returns:
            BROADCAST packet
        """
        return self.build_packet(
            target_node_id="*",  # Wildcard for broadcast
            input_seed=message,
            required_methodology=methodology,
            intent="BROADCAST"
        )
    
    def _compute_payload_hash(self, payload: Dict[str, Any]) -> str:
        """
        Compute SHA-256 hash of payload for integrity verification.
        
        Args:
            payload: Payload dictionary
            
        Returns:
            Hex digest of hash
        """
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
    
    @staticmethod
    def validate_packet(packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Validate an IUPP packet structure.
        
        Args:
            packet: Packet to validate
            
        Returns:
            Validation result with errors if any
        """
        errors = []
        warnings = []
        
        # Check schema
        if "$schema" not in packet:
            errors.append("Missing $schema field")
        
        # Check header
        if "header" not in packet:
            errors.append("Missing header section")
        else:
            header = packet["header"]
            required_header = ["packet_id", "timestamp", "origin_node_id", 
                            "target_node_id", "recursion_depth"]
            for field in required_header:
                if field not in header:
                    errors.append(f"Missing header field: {field}")
        
        # Check mandate_context
        if "mandate_context" not in packet:
            warnings.append("Missing mandate_context section")
        
        # Check contract_spec
        if "contract_spec" not in packet:
            errors.append("Missing contract_spec section")
        else:
            contract = packet["contract_spec"]
            if "intent" not in contract:
                errors.append("Missing contract_spec.intent")
            if "required_methodology" not in contract:
                warnings.append("Missing required_methodology")
        
        # Check payload
        if "payload" not in packet:
            errors.append("Missing payload section")
        else:
            if "input_seed" not in packet["payload"]:
                errors.append("Missing payload.input_seed")
        
        # Verify integrity if present
        if "integrity" in packet and "payload" in packet:
            expected_hash = IUPPPacketBuilder._compute_payload_hash_static(
                packet["payload"]
            )
            actual_hash = packet["integrity"].get("payload_hash", "")
            if expected_hash != actual_hash:
                errors.append("Payload integrity check failed")
        
        return {
            "valid": len(errors) == 0,
            "errors": errors,
            "warnings": warnings
        }
    
    @staticmethod
    def _compute_payload_hash_static(payload: Dict[str, Any]) -> str:
        """Static version of hash computation for validation."""
        payload_str = json.dumps(payload, sort_keys=True, ensure_ascii=False)
        return hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
    
    def increment_recursion(self) -> None:
        """Increment recursion depth for nested packets."""
        self.recursion_depth += 1
    
    def reset_recursion(self) -> None:
        """Reset recursion depth."""
        self.recursion_depth = 0
    
    @staticmethod
    def extract_result(response: Dict[str, Any]) -> Optional[str]:
        """
        Extract the result content from an OpenAI-compatible response.
        
        Args:
            response: API response dictionary
            
        Returns:
            Extracted content string or None
        """
        try:
            if "choices" in response and len(response["choices"]) > 0:
                choice = response["choices"][0]
                if "message" in choice:
                    return choice["message"].get("content", "")
                elif "text" in choice:
                    return choice["text"]
            return None
        except Exception:
            return None
    
    @staticmethod
    def format_packet_display(packet: Dict[str, Any]) -> str:
        """
        Format a packet for human-readable display.
        
        Args:
            packet: IUPP packet
            
        Returns:
            Formatted string representation
        """
        header = packet.get("header", {})
        contract = packet.get("contract_spec", {})
        payload = packet.get("payload", {})
        
        return f"""
╔══════════════════════════════════════════════════════════════════╗
║                        IUPP PACKET                                ║
╠══════════════════════════════════════════════════════════════════╣
║ Packet ID: {header.get('packet_id', 'N/A')[:36]}    ║
║ Timestamp: {header.get('timestamp', 'N/A')}                       ║
║ Origin:    {header.get('origin_node_id', 'N/A')}                  ║
║ Target:    {header.get('target_node_id', 'N/A')}                  ║
║ Intent:    {contract.get('intent', 'N/A')}                        ║
║ Method:    {contract.get('required_methodology', 'N/A')}          ║
╠══════════════════════════════════════════════════════════════════╣
║ Input Seed:                                                       ║
║ {payload.get('input_seed', 'N/A')[:60]}{'...' if len(payload.get('input_seed', '')) > 60 else ''}
╚══════════════════════════════════════════════════════════════════╝
"""


def create_iupp_packet(
    target_node_id: str,
    input_seed: str,
    methodology: str,
    gam_context: str = "",
    origin_node_id: str = "Orchestrator-Main"
) -> Dict[str, Any]:
    """
    Convenience function to create an IUPP packet.
    
    Args:
        target_node_id: Target node
        input_seed: Input content
        methodology: Required methodology
        gam_context: Optional context injection
        origin_node_id: Origin node ID
        
    Returns:
        IUPP packet dictionary
    """
    builder = IUPPPacketBuilder(origin_node_id)
    return builder.build_request_packet(
        target_node_id=target_node_id,
        query=input_seed,
        methodology=methodology,
        gam_context=gam_context
    )


if __name__ == "__main__":
    # Test packet building
    builder = IUPPPacketBuilder()
    
    # Build a test packet
    packet = builder.build_request_packet(
        target_node_id="test-node-1",
        query="Analyze this system for security vulnerabilities",
        methodology="internal-red-team-audit",
        gam_context="Previous analysis found 3 critical issues"
    )
    
    print("📦 Generated IUPP Packet:")
    print(json.dumps(packet, indent=2))
    
    # Validate the packet
    validation = IUPPPacketBuilder.validate_packet(packet)
    print(f"\n✅ Validation: {validation}")
    
    # Display formatted
    print(IUPPPacketBuilder.format_packet_display(packet))
