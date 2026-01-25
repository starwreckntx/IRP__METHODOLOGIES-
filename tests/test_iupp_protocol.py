"""
Comprehensive Test Suite for IUPP Protocol Module
==================================================
Tests the IUPPPacketBuilder class and all related functions.

Test Coverage:
- Packet building (request, response, broadcast)
- Packet validation
- Payload hash computation
- Result extraction from API responses
- Recursion depth management
- Edge cases and error handling
"""

import pytest
import json
import hashlib
import uuid
from datetime import datetime
from unittest.mock import patch

# Import the module under test
import sys
from pathlib import Path

# Add the irp_swarm_console directory to the path
sys.path.insert(0, str(Path(__file__).parent.parent / "irp_swarm_console"))

from iupp_protocol import (
    IUPPPacketBuilder,
    create_iupp_packet
)


class TestIUPPPacketBuilderInitialization:
    """Test IUPPPacketBuilder initialization."""

    def test_default_initialization(self):
        """Test builder initializes with default values."""
        builder = IUPPPacketBuilder()
        assert builder.origin_node_id == "Orchestrator-Main"
        assert builder.recursion_depth == 0

    def test_custom_origin_node(self):
        """Test builder initializes with custom origin node."""
        builder = IUPPPacketBuilder(origin_node_id="Custom-Node-123")
        assert builder.origin_node_id == "Custom-Node-123"
        assert builder.recursion_depth == 0

    def test_schema_version_constant(self):
        """Test schema version constant is set correctly."""
        assert IUPPPacketBuilder.SCHEMA_VERSION == "IRP_Peering_Protocol_v1.0"

    def test_default_constants(self):
        """Test default mandate and axiom constants."""
        assert IUPPPacketBuilder.DEFAULT_MANDATE == "P-001-R1"
        assert IUPPPacketBuilder.DEFAULT_AXIOM == "The Journey IS The Artifact"


class TestBuildPacket:
    """Test the main build_packet method."""

    def test_build_basic_packet(self):
        """Test building a basic packet with required parameters."""
        builder = IUPPPacketBuilder()

        packet = builder.build_packet(
            target_node_id="test-node",
            input_seed="Test input",
            required_methodology="test-methodology"
        )

        # Verify structure
        assert "$schema" in packet
        assert packet["$schema"] == "IRP_Peering_Protocol_v1.0"
        assert "header" in packet
        assert "mandate_context" in packet
        assert "contract_spec" in packet
        assert "payload" in packet
        assert "integrity" in packet

    def test_header_fields(self):
        """Test that header contains all required fields."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="node-123",
            input_seed="Test",
            required_methodology="test"
        )

        header = packet["header"]
        assert "packet_id" in header
        assert "timestamp" in header
        assert "origin_node_id" in header
        assert "target_node_id" in header
        assert "recursion_depth" in header

        # Verify values
        assert header["origin_node_id"] == "Orchestrator-Main"
        assert header["target_node_id"] == "node-123"
        assert header["recursion_depth"] == 0

        # Verify packet_id is a valid UUID
        uuid.UUID(header["packet_id"])  # Should not raise

        # Verify timestamp format
        assert header["timestamp"].endswith("Z")

    def test_mandate_context(self):
        """Test mandate context with default values."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )

        mandate = packet["mandate_context"]
        assert mandate["active_mandate"] == "P-001-R1"
        assert mandate["axiom"] == "The Journey IS The Artifact"

    def test_custom_mandate_and_axiom(self):
        """Test overriding default mandate and axiom."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test",
            active_mandate="P-002-R2",
            axiom="Custom Axiom"
        )

        mandate = packet["mandate_context"]
        assert mandate["active_mandate"] == "P-002-R2"
        assert mandate["axiom"] == "Custom Axiom"

    def test_contract_spec(self):
        """Test contract specification fields."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="red-team-audit",
            intent="REQUEST",
            output_format="JSON"
        )

        contract = packet["contract_spec"]
        assert contract["intent"] == "REQUEST"
        assert contract["required_methodology"] == "red-team-audit"
        assert contract["output_format"] == "JSON"

    def test_payload_structure(self):
        """Test payload contains input_seed and context_injection."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="This is the input seed",
            required_methodology="test",
            context_injection="This is context"
        )

        payload = packet["payload"]
        assert payload["input_seed"] == "This is the input seed"
        assert payload["context_injection"] == "This is context"

    def test_payload_default_context(self):
        """Test payload uses default context when not provided."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )

        assert packet["payload"]["context_injection"] == "No prior context"

    def test_metadata_inclusion(self):
        """Test optional metadata is included when provided."""
        builder = IUPPPacketBuilder()
        custom_metadata = {
            "user_id": "user123",
            "session_id": "session456",
            "priority": "high"
        }

        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test",
            metadata=custom_metadata
        )

        assert "metadata" in packet
        assert packet["metadata"] == custom_metadata

    def test_metadata_omitted_when_none(self):
        """Test metadata is not included when None."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )

        assert "metadata" not in packet

    def test_integrity_hash(self):
        """Test integrity hash is computed correctly."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test input",
            required_methodology="test"
        )

        integrity = packet["integrity"]
        assert "payload_hash" in integrity
        assert "algorithm" in integrity
        assert integrity["algorithm"] == "SHA-256"

        # Verify hash is correct
        payload_str = json.dumps(packet["payload"], sort_keys=True, ensure_ascii=False)
        expected_hash = hashlib.sha256(payload_str.encode('utf-8')).hexdigest()
        assert integrity["payload_hash"] == expected_hash

    def test_recursion_depth_in_packet(self):
        """Test recursion depth is included in packet header."""
        builder = IUPPPacketBuilder()
        builder.recursion_depth = 3

        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )

        assert packet["header"]["recursion_depth"] == 3


class TestBuildRequestPacket:
    """Test the build_request_packet convenience method."""

    def test_build_request_packet(self):
        """Test building a REQUEST packet."""
        builder = IUPPPacketBuilder()
        packet = builder.build_request_packet(
            target_node_id="node-1",
            query="Analyze this code",
            methodology="code-review"
        )

        assert packet["contract_spec"]["intent"] == "REQUEST"
        assert packet["payload"]["input_seed"] == "Analyze this code"
        assert packet["contract_spec"]["required_methodology"] == "code-review"

    def test_request_packet_with_context(self):
        """Test REQUEST packet with GAM context."""
        builder = IUPPPacketBuilder()
        packet = builder.build_request_packet(
            target_node_id="node-1",
            query="Continue analysis",
            methodology="analysis",
            gam_context="Previous analysis found 5 issues"
        )

        assert packet["payload"]["context_injection"] == "Previous analysis found 5 issues"

    def test_request_packet_without_context(self):
        """Test REQUEST packet defaults to 'No prior context'."""
        builder = IUPPPacketBuilder()
        packet = builder.build_request_packet(
            target_node_id="node-1",
            query="New analysis",
            methodology="analysis"
        )

        assert packet["payload"]["context_injection"] == "No prior context"


class TestBuildResponsePacket:
    """Test the build_response_packet method."""

    def test_build_response_packet(self):
        """Test building a RESPONSE packet."""
        builder = IUPPPacketBuilder()
        original_packet_id = str(uuid.uuid4())

        packet = builder.build_response_packet(
            target_node_id="orchestrator",
            result="Analysis complete: 3 issues found",
            original_packet_id=original_packet_id,
            methodology="code-review"
        )

        assert packet["contract_spec"]["intent"] == "RESPONSE"
        assert packet["payload"]["input_seed"] == "Analysis complete: 3 issues found"
        assert packet["header"]["in_reply_to"] == original_packet_id

    def test_response_includes_original_reference(self):
        """Test RESPONSE packet includes reference to original packet."""
        builder = IUPPPacketBuilder()
        original_id = "12345678-1234-1234-1234-123456789012"

        packet = builder.build_response_packet(
            target_node_id="test",
            result="Done",
            original_packet_id=original_id,
            methodology="test"
        )

        assert "in_reply_to" in packet["header"]
        assert packet["header"]["in_reply_to"] == original_id


class TestBuildBroadcastPacket:
    """Test the build_broadcast_packet method."""

    def test_build_broadcast_packet(self):
        """Test building a BROADCAST packet."""
        builder = IUPPPacketBuilder()
        packet = builder.build_broadcast_packet(
            message="System maintenance in 5 minutes"
        )

        assert packet["contract_spec"]["intent"] == "BROADCAST"
        assert packet["header"]["target_node_id"] == "*"
        assert packet["payload"]["input_seed"] == "System maintenance in 5 minutes"

    def test_broadcast_packet_custom_methodology(self):
        """Test BROADCAST packet with custom methodology."""
        builder = IUPPPacketBuilder()
        packet = builder.build_broadcast_packet(
            message="Alert: Security issue detected",
            methodology="security-alert"
        )

        assert packet["contract_spec"]["required_methodology"] == "security-alert"

    def test_broadcast_packet_default_methodology(self):
        """Test BROADCAST packet uses 'general' by default."""
        builder = IUPPPacketBuilder()
        packet = builder.build_broadcast_packet(
            message="General broadcast"
        )

        assert packet["contract_spec"]["required_methodology"] == "general"


class TestPayloadHashComputation:
    """Test payload hash computation methods."""

    def test_compute_payload_hash(self):
        """Test instance method for computing payload hash."""
        builder = IUPPPacketBuilder()
        payload = {
            "input_seed": "Test input",
            "context_injection": "Test context"
        }

        hash_result = builder._compute_payload_hash(payload)

        # Verify it's a valid hex string
        assert len(hash_result) == 64  # SHA-256 produces 64 hex characters
        assert all(c in '0123456789abcdef' for c in hash_result)

    def test_compute_payload_hash_deterministic(self):
        """Test hash computation is deterministic."""
        builder = IUPPPacketBuilder()
        payload = {
            "input_seed": "Same input",
            "context_injection": "Same context"
        }

        hash1 = builder._compute_payload_hash(payload)
        hash2 = builder._compute_payload_hash(payload)

        assert hash1 == hash2

    def test_compute_payload_hash_different_inputs(self):
        """Test different payloads produce different hashes."""
        builder = IUPPPacketBuilder()

        payload1 = {"input_seed": "Input 1", "context_injection": "Context 1"}
        payload2 = {"input_seed": "Input 2", "context_injection": "Context 2"}

        hash1 = builder._compute_payload_hash(payload1)
        hash2 = builder._compute_payload_hash(payload2)

        assert hash1 != hash2

    def test_static_hash_computation(self):
        """Test static method for hash computation."""
        payload = {
            "input_seed": "Test",
            "context_injection": "Context"
        }

        hash_result = IUPPPacketBuilder._compute_payload_hash_static(payload)

        assert len(hash_result) == 64
        assert all(c in '0123456789abcdef' for c in hash_result)

    def test_instance_and_static_hash_match(self):
        """Test instance and static hash methods produce same result."""
        builder = IUPPPacketBuilder()
        payload = {
            "input_seed": "Test input",
            "context_injection": "Test context"
        }

        instance_hash = builder._compute_payload_hash(payload)
        static_hash = IUPPPacketBuilder._compute_payload_hash_static(payload)

        assert instance_hash == static_hash

    def test_hash_with_unicode_characters(self):
        """Test hash computation with Unicode characters."""
        builder = IUPPPacketBuilder()
        payload = {
            "input_seed": "Test with émojis 🚀 and spëcial çhars",
            "context_injection": "Unicode: 你好世界"
        }

        hash_result = builder._compute_payload_hash(payload)

        # Should not raise and should produce valid hash
        assert len(hash_result) == 64


class TestPacketValidation:
    """Test the validate_packet static method."""

    def test_validate_valid_packet(self):
        """Test validation passes for a valid packet."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is True
        assert len(result["errors"]) == 0

    def test_validate_missing_schema(self):
        """Test validation fails when $schema is missing."""
        packet = {
            "header": {"packet_id": "123", "timestamp": "2024-01-01T00:00:00Z",
                      "origin_node_id": "test", "target_node_id": "test",
                      "recursion_depth": 0},
            "contract_spec": {"intent": "REQUEST"},
            "payload": {"input_seed": "test"}
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        assert "Missing $schema field" in result["errors"]

    def test_validate_missing_header(self):
        """Test validation fails when header is missing."""
        packet = {
            "$schema": "IRP_Peering_Protocol_v1.0",
            "contract_spec": {"intent": "REQUEST"},
            "payload": {"input_seed": "test"}
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        assert "Missing header section" in result["errors"]

    def test_validate_missing_header_fields(self):
        """Test validation fails when required header fields are missing."""
        packet = {
            "$schema": "IRP_Peering_Protocol_v1.0",
            "header": {"packet_id": "123"},  # Missing other required fields
            "contract_spec": {"intent": "REQUEST"},
            "payload": {"input_seed": "test"}
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        # Should have errors for missing header fields
        assert any("timestamp" in err for err in result["errors"])
        assert any("origin_node_id" in err for err in result["errors"])

    def test_validate_missing_contract_spec(self):
        """Test validation fails when contract_spec is missing."""
        packet = {
            "$schema": "IRP_Peering_Protocol_v1.0",
            "header": {"packet_id": "123", "timestamp": "2024-01-01T00:00:00Z",
                      "origin_node_id": "test", "target_node_id": "test",
                      "recursion_depth": 0},
            "payload": {"input_seed": "test"}
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        assert "Missing contract_spec section" in result["errors"]

    def test_validate_missing_payload(self):
        """Test validation fails when payload is missing."""
        packet = {
            "$schema": "IRP_Peering_Protocol_v1.0",
            "header": {"packet_id": "123", "timestamp": "2024-01-01T00:00:00Z",
                      "origin_node_id": "test", "target_node_id": "test",
                      "recursion_depth": 0},
            "contract_spec": {"intent": "REQUEST"}
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        assert "Missing payload section" in result["errors"]

    def test_validate_missing_input_seed(self):
        """Test validation fails when payload.input_seed is missing."""
        packet = {
            "$schema": "IRP_Peering_Protocol_v1.0",
            "header": {"packet_id": "123", "timestamp": "2024-01-01T00:00:00Z",
                      "origin_node_id": "test", "target_node_id": "test",
                      "recursion_depth": 0},
            "contract_spec": {"intent": "REQUEST"},
            "payload": {"context_injection": "test"}  # Missing input_seed
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        assert "Missing payload.input_seed" in result["errors"]

    def test_validate_warnings_for_optional_fields(self):
        """Test validation produces warnings for missing optional fields."""
        packet = {
            "$schema": "IRP_Peering_Protocol_v1.0",
            "header": {"packet_id": "123", "timestamp": "2024-01-01T00:00:00Z",
                      "origin_node_id": "test", "target_node_id": "test",
                      "recursion_depth": 0},
            "contract_spec": {"intent": "REQUEST"},  # Missing required_methodology
            "payload": {"input_seed": "test"}
        }

        result = IUPPPacketBuilder.validate_packet(packet)

        # Should be valid (only warnings, not errors)
        assert result["valid"] is True
        assert len(result["warnings"]) > 0

    def test_validate_integrity_check_passes(self):
        """Test validation verifies payload integrity correctly."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is True
        assert "Payload integrity check failed" not in result["errors"]

    def test_validate_integrity_check_fails(self):
        """Test validation detects tampered payload."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Original input",
            required_methodology="test"
        )

        # Tamper with payload after hash was computed
        packet["payload"]["input_seed"] = "Tampered input"

        result = IUPPPacketBuilder.validate_packet(packet)

        assert result["valid"] is False
        assert "Payload integrity check failed" in result["errors"]


class TestRecursionManagement:
    """Test recursion depth management methods."""

    def test_initial_recursion_depth(self):
        """Test recursion depth starts at 0."""
        builder = IUPPPacketBuilder()
        assert builder.recursion_depth == 0

    def test_increment_recursion(self):
        """Test incrementing recursion depth."""
        builder = IUPPPacketBuilder()
        builder.increment_recursion()
        assert builder.recursion_depth == 1

        builder.increment_recursion()
        assert builder.recursion_depth == 2

    def test_reset_recursion(self):
        """Test resetting recursion depth."""
        builder = IUPPPacketBuilder()
        builder.recursion_depth = 5

        builder.reset_recursion()
        assert builder.recursion_depth == 0

    def test_recursion_depth_in_built_packet(self):
        """Test recursion depth is reflected in built packets."""
        builder = IUPPPacketBuilder()

        packet1 = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )
        assert packet1["header"]["recursion_depth"] == 0

        builder.increment_recursion()
        packet2 = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test"
        )
        assert packet2["header"]["recursion_depth"] == 1


class TestExtractResult:
    """Test the extract_result static method."""

    def test_extract_from_message_format(self):
        """Test extracting result from message-based response."""
        response = {
            "choices": [
                {
                    "message": {
                        "content": "This is the result",
                        "role": "assistant"
                    }
                }
            ]
        }

        result = IUPPPacketBuilder.extract_result(response)
        assert result == "This is the result"

    def test_extract_from_text_format(self):
        """Test extracting result from text-based response."""
        response = {
            "choices": [
                {
                    "text": "This is the text result"
                }
            ]
        }

        result = IUPPPacketBuilder.extract_result(response)
        assert result == "This is the text result"

    def test_extract_from_empty_choices(self):
        """Test extraction returns None when choices is empty."""
        response = {
            "choices": []
        }

        result = IUPPPacketBuilder.extract_result(response)
        assert result is None

    def test_extract_from_missing_choices(self):
        """Test extraction returns None when choices key is missing."""
        response = {
            "id": "test",
            "object": "chat.completion"
        }

        result = IUPPPacketBuilder.extract_result(response)
        assert result is None

    def test_extract_from_invalid_response(self):
        """Test extraction handles malformed responses gracefully."""
        response = {
            "choices": [
                {
                    "invalid": "structure"
                }
            ]
        }

        result = IUPPPacketBuilder.extract_result(response)
        # Should return empty string or None, not raise
        assert result == "" or result is None

    def test_extract_multiple_choices(self):
        """Test extraction gets first choice when multiple exist."""
        response = {
            "choices": [
                {"message": {"content": "First result"}},
                {"message": {"content": "Second result"}}
            ]
        }

        result = IUPPPacketBuilder.extract_result(response)
        assert result == "First result"


class TestFormatPacketDisplay:
    """Test the format_packet_display static method."""

    def test_format_basic_packet(self):
        """Test formatting a basic packet for display."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test-node",
            input_seed="Test input",
            required_methodology="test-method"
        )

        formatted = IUPPPacketBuilder.format_packet_display(packet)

        assert "IUPP PACKET" in formatted
        assert "test-node" in formatted
        assert "test-method" in formatted
        assert "REQUEST" in formatted

    def test_format_includes_all_key_fields(self):
        """Test formatted output includes key packet fields."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="node-123",
            input_seed="Analysis request",
            required_methodology="security-audit",
            intent="REQUEST"
        )

        formatted = IUPPPacketBuilder.format_packet_display(packet)

        # Check for key fields
        assert "Packet ID:" in formatted
        assert "Timestamp:" in formatted
        assert "Origin:" in formatted
        assert "Target:" in formatted
        assert "Intent:" in formatted
        assert "Method:" in formatted
        assert "Input Seed:" in formatted

    def test_format_handles_missing_fields(self):
        """Test formatting handles missing optional fields gracefully."""
        incomplete_packet = {
            "header": {},
            "contract_spec": {},
            "payload": {}
        }

        formatted = IUPPPacketBuilder.format_packet_display(incomplete_packet)

        # Should not raise, should contain "N/A" for missing fields
        assert "N/A" in formatted

    def test_format_truncates_long_input(self):
        """Test formatting truncates very long input seeds."""
        builder = IUPPPacketBuilder()
        long_input = "x" * 200

        packet = builder.build_packet(
            target_node_id="test",
            input_seed=long_input,
            required_methodology="test"
        )

        formatted = IUPPPacketBuilder.format_packet_display(packet)

        # Should contain truncation indicator
        assert "..." in formatted


class TestCreateIUPPPacket:
    """Test the convenience function create_iupp_packet."""

    def test_create_basic_packet(self):
        """Test creating a packet with the convenience function."""
        packet = create_iupp_packet(
            target_node_id="test-node",
            input_seed="Test input",
            methodology="test-method"
        )

        assert packet["header"]["target_node_id"] == "test-node"
        assert packet["payload"]["input_seed"] == "Test input"
        assert packet["contract_spec"]["required_methodology"] == "test-method"

    def test_create_packet_with_context(self):
        """Test creating a packet with GAM context."""
        packet = create_iupp_packet(
            target_node_id="node",
            input_seed="Input",
            methodology="method",
            gam_context="Previous context here"
        )

        assert packet["payload"]["context_injection"] == "Previous context here"

    def test_create_packet_custom_origin(self):
        """Test creating a packet with custom origin node."""
        packet = create_iupp_packet(
            target_node_id="target",
            input_seed="Input",
            methodology="method",
            origin_node_id="Custom-Origin"
        )

        assert packet["header"]["origin_node_id"] == "Custom-Origin"

    def test_create_packet_defaults(self):
        """Test convenience function uses correct defaults."""
        packet = create_iupp_packet(
            target_node_id="target",
            input_seed="Input",
            methodology="method"
        )

        assert packet["header"]["origin_node_id"] == "Orchestrator-Main"
        assert packet["payload"]["context_injection"] == "No prior context"
        assert packet["contract_spec"]["intent"] == "REQUEST"


class TestEdgeCases:
    """Test edge cases and unusual inputs."""

    def test_empty_input_seed(self):
        """Test building packet with empty input seed."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="",
            required_methodology="test"
        )

        assert packet["payload"]["input_seed"] == ""
        # Should still be valid structure
        assert "$schema" in packet

    def test_very_long_input_seed(self):
        """Test building packet with very long input."""
        builder = IUPPPacketBuilder()
        long_input = "x" * 10000

        packet = builder.build_packet(
            target_node_id="test",
            input_seed=long_input,
            required_methodology="test"
        )

        assert packet["payload"]["input_seed"] == long_input
        # Hash should still be computed
        assert "integrity" in packet

    def test_unicode_in_all_fields(self):
        """Test Unicode characters in various fields."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="节点-123",
            input_seed="Tëst with spëcial chàrs 🚀",
            required_methodology="méthodologie-spéciale",
            context_injection="Contexte précédent 你好"
        )

        assert packet["header"]["target_node_id"] == "节点-123"
        assert "🚀" in packet["payload"]["input_seed"]
        # Should not raise during JSON serialization
        json.dumps(packet)

    def test_special_characters_in_methodology(self):
        """Test special characters in methodology name."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="method-with-dashes_and_underscores.and.dots"
        )

        assert packet["contract_spec"]["required_methodology"] == "method-with-dashes_and_underscores.and.dots"

    def test_wildcard_target_node(self):
        """Test using wildcard as target node."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="*",
            input_seed="Broadcast message",
            required_methodology="general"
        )

        assert packet["header"]["target_node_id"] == "*"

    def test_packet_serialization(self):
        """Test that built packets can be serialized to JSON."""
        builder = IUPPPacketBuilder()
        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test input",
            required_methodology="test"
        )

        # Should not raise
        json_str = json.dumps(packet)

        # Should be able to deserialize
        deserialized = json.loads(json_str)
        assert deserialized["header"]["target_node_id"] == "test"

    def test_nested_metadata(self):
        """Test packet with complex nested metadata."""
        builder = IUPPPacketBuilder()
        complex_metadata = {
            "level1": {
                "level2": {
                    "level3": ["array", "values"],
                    "number": 42
                }
            },
            "list": [1, 2, 3, {"key": "value"}]
        }

        packet = builder.build_packet(
            target_node_id="test",
            input_seed="Test",
            required_methodology="test",
            metadata=complex_metadata
        )

        assert packet["metadata"] == complex_metadata
        # Should be serializable
        json.dumps(packet)


class TestIntegrationScenarios:
    """Test realistic integration scenarios."""

    def test_request_response_flow(self):
        """Test creating a request and corresponding response."""
        builder = IUPPPacketBuilder()

        # Create request
        request = builder.build_request_packet(
            target_node_id="worker-node-1",
            query="Analyze security vulnerabilities",
            methodology="security-audit"
        )

        # Create response
        response = builder.build_response_packet(
            target_node_id="orchestrator",
            result="Found 3 vulnerabilities",
            original_packet_id=request["header"]["packet_id"],
            methodology="security-audit"
        )

        # Verify flow
        assert response["header"]["in_reply_to"] == request["header"]["packet_id"]
        assert request["contract_spec"]["intent"] == "REQUEST"
        assert response["contract_spec"]["intent"] == "RESPONSE"

    def test_multi_hop_routing(self):
        """Test building packets for multi-hop routing."""
        builder = IUPPPacketBuilder()

        # First hop
        packet1 = builder.build_packet(
            target_node_id="node-1",
            input_seed="Initial query",
            required_methodology="preprocessing"
        )
        assert packet1["header"]["recursion_depth"] == 0

        # Second hop
        builder.increment_recursion()
        packet2 = builder.build_packet(
            target_node_id="node-2",
            input_seed="Processed query",
            required_methodology="analysis"
        )
        assert packet2["header"]["recursion_depth"] == 1

        # Third hop
        builder.increment_recursion()
        packet3 = builder.build_packet(
            target_node_id="node-3",
            input_seed="Final analysis",
            required_methodology="synthesis"
        )
        assert packet3["header"]["recursion_depth"] == 2

    def test_broadcast_to_multiple_nodes(self):
        """Test creating broadcast packet."""
        builder = IUPPPacketBuilder()

        broadcast = builder.build_broadcast_packet(
            message="System status: All nodes operational",
            methodology="system-status"
        )

        assert broadcast["header"]["target_node_id"] == "*"
        assert broadcast["contract_spec"]["intent"] == "BROADCAST"

        # Validate the packet
        validation = IUPPPacketBuilder.validate_packet(broadcast)
        assert validation["valid"] is True

    def test_validate_then_route(self):
        """Test validating a packet before routing."""
        builder = IUPPPacketBuilder()

        packet = builder.build_request_packet(
            target_node_id="node-1",
            query="Test query",
            methodology="test"
        )

        # Validate before routing
        validation = IUPPPacketBuilder.validate_packet(packet)
        assert validation["valid"] is True

        # Packet is ready to route
        assert packet["header"]["target_node_id"] == "node-1"
