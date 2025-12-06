"""
Node Registry Module
====================
Manages registration and routing of IRP swarm nodes.
Handles actual HTTP communication with external endpoints.
"""

import json
import requests
from typing import Dict, List, Optional, Any
from datetime import datetime
from dataclasses import dataclass, field, asdict


@dataclass
class NodeInfo:
    """Information about a registered node."""
    node_id: str
    url: str
    api_key: str
    capabilities: List[str] = field(default_factory=list)
    status: str = "active"
    last_heartbeat: str = ""
    registered_at: str = ""
    error_count: int = 0
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class NodeRegistry:
    """
    Registry for managing IRP swarm nodes.
    Provides registration, status tracking, and packet routing.
    """
    
    def __init__(self):
        """Initialize the node registry."""
        self.nodes: Dict[str, NodeInfo] = {}
        self._request_timeout = 30  # seconds
    
    def register_node(
        self,
        node_id: str,
        url: str,
        api_key: str,
        capabilities: List[str] = None
    ) -> Dict[str, Any]:
        """
        Register a new node in the registry.
        
        Args:
            node_id: Unique identifier for the node
            url: Base URL for the node's API endpoint
            api_key: API key for authentication
            capabilities: List of methodology capabilities
            
        Returns:
            Registration result with status
        """
        if capabilities is None:
            capabilities = []
        
        # Normalize URL (ensure no trailing slash)
        url = url.rstrip('/')
        
        now = datetime.utcnow().isoformat() + "Z"
        
        node = NodeInfo(
            node_id=node_id,
            url=url,
            api_key=api_key,
            capabilities=capabilities,
            status="active",
            last_heartbeat=now,
            registered_at=now,
            error_count=0
        )
        
        self.nodes[node_id] = node
        
        return {
            "success": True,
            "message": f"Node '{node_id}' registered successfully",
            "node": node.to_dict()
        }
    
    def remove_node(self, node_id: str) -> Dict[str, Any]:
        """
        Remove a node from the registry.
        
        Args:
            node_id: ID of the node to remove
            
        Returns:
            Removal result
        """
        if node_id in self.nodes:
            del self.nodes[node_id]
            return {
                "success": True,
                "message": f"Node '{node_id}' removed"
            }
        return {
            "success": False,
            "message": f"Node '{node_id}' not found"
        }
    
    def get_node(self, node_id: str) -> Optional[NodeInfo]:
        """
        Get a specific node by ID.
        
        Args:
            node_id: Node identifier
            
        Returns:
            NodeInfo or None if not found
        """
        return self.nodes.get(node_id)
    
    def get_all_nodes(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all registered nodes with their info.
        
        Returns:
            Dictionary of node_id to node info
        """
        return {
            node_id: node.to_dict()
            for node_id, node in self.nodes.items()
        }
    
    def update_node_status(self, node_id: str, status: str) -> bool:
        """
        Update a node's status.
        
        Args:
            node_id: Node identifier
            status: New status (active, inactive, error)
            
        Returns:
            Success boolean
        """
        if node_id in self.nodes:
            self.nodes[node_id].status = status
            self.nodes[node_id].last_heartbeat = datetime.utcnow().isoformat() + "Z"
            return True
        return False
    
    def route_packet(
        self,
        target_node_id: str,
        packet_json: Dict[str, Any],
        endpoint: str = "/v1/chat/completions"
    ) -> Dict[str, Any]:
        """
        Route an IUPP packet to a target node using HTTP POST.
        
        Args:
            target_node_id: ID of the target node
            packet_json: The IUPP packet as a dictionary
            endpoint: API endpoint path (default: /v1/chat/completions)
            
        Returns:
            Response dictionary with status and data
        """
        node = self.nodes.get(target_node_id)
        
        if not node:
            return {
                "success": False,
                "error": f"Node '{target_node_id}' not found in registry",
                "data": None
            }
        
        if node.status != "active":
            return {
                "success": False,
                "error": f"Node '{target_node_id}' is not active (status: {node.status})",
                "data": None
            }
        
        # Build the full URL
        full_url = f"{node.url}{endpoint}"
        
        # Prepare headers
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {node.api_key}"
        }
        
        # Convert packet to chat completion format for LLM nodes
        chat_payload = self._convert_to_chat_format(packet_json)
        
        try:
            response = requests.post(
                full_url,
                headers=headers,
                json=chat_payload,
                timeout=self._request_timeout
            )
            
            # Update heartbeat
            node.last_heartbeat = datetime.utcnow().isoformat() + "Z"
            
            if response.status_code == 200:
                node.error_count = 0
                return {
                    "success": True,
                    "status_code": response.status_code,
                    "data": response.json(),
                    "node_id": target_node_id
                }
            else:
                node.error_count += 1
                if node.error_count >= 3:
                    node.status = "error"
                
                return {
                    "success": False,
                    "status_code": response.status_code,
                    "error": f"HTTP {response.status_code}: {response.text[:500]}",
                    "data": None,
                    "node_id": target_node_id
                }
                
        except requests.exceptions.Timeout:
            node.error_count += 1
            return {
                "success": False,
                "error": f"Request to '{target_node_id}' timed out",
                "data": None,
                "node_id": target_node_id
            }
        except requests.exceptions.ConnectionError as e:
            node.error_count += 1
            node.status = "unreachable"
            return {
                "success": False,
                "error": f"Connection error to '{target_node_id}': {str(e)}",
                "data": None,
                "node_id": target_node_id
            }
        except Exception as e:
            node.error_count += 1
            return {
                "success": False,
                "error": f"Error routing to '{target_node_id}': {str(e)}",
                "data": None,
                "node_id": target_node_id
            }
    
    def _convert_to_chat_format(self, packet: Dict[str, Any]) -> Dict[str, Any]:
        """
        Convert an IUPP packet to OpenAI-compatible chat completion format.
        
        Args:
            packet: IUPP packet dictionary
            
        Returns:
            Chat completion API payload
        """
        # Extract relevant fields from IUPP packet
        payload = packet.get("payload", {})
        contract = packet.get("contract_spec", {})
        mandate = packet.get("mandate_context", {})
        
        # Build system message with methodology context
        system_content = f"""You are operating under the IRP (Intelligent Relay Protocol) framework.

Active Mandate: {mandate.get('active_mandate', 'P-001-R1')}
Axiom: {mandate.get('axiom', 'The Journey IS The Artifact')}

Required Methodology: {contract.get('required_methodology', 'general')}
Output Format: {contract.get('output_format', 'JSON')}

Context Injection:
{payload.get('context_injection', 'No prior context')}
"""
        
        # Build user message with input seed
        user_content = payload.get("input_seed", "")
        
        return {
            "model": "default",  # Will use the node's default model
            "messages": [
                {"role": "system", "content": system_content},
                {"role": "user", "content": user_content}
            ],
            "temperature": 0.7,
            "max_tokens": 4096
        }
    
    def find_nodes_by_capability(self, capability: str) -> List[str]:
        """
        Find all nodes that support a given capability.
        
        Args:
            capability: Methodology or capability name
            
        Returns:
            List of node IDs with the capability
        """
        matching_nodes = []
        capability_lower = capability.lower()
        
        for node_id, node in self.nodes.items():
            if node.status != "active":
                continue
            
            # Check capabilities (partial match)
            for cap in node.capabilities:
                if capability_lower in cap.lower():
                    matching_nodes.append(node_id)
                    break
        
        return matching_nodes
    
    def health_check(self, node_id: str) -> Dict[str, Any]:
        """
        Perform a health check on a specific node.
        
        Args:
            node_id: Node to check
            
        Returns:
            Health check result
        """
        node = self.nodes.get(node_id)
        
        if not node:
            return {
                "success": False,
                "error": f"Node '{node_id}' not found"
            }
        
        try:
            # Try to reach the node's base URL
            response = requests.get(
                node.url,
                timeout=5
            )
            
            node.last_heartbeat = datetime.utcnow().isoformat() + "Z"
            node.status = "active"
            node.error_count = 0
            
            return {
                "success": True,
                "node_id": node_id,
                "status": "healthy",
                "response_time_ms": response.elapsed.total_seconds() * 1000
            }
            
        except Exception as e:
            node.status = "unreachable"
            return {
                "success": False,
                "node_id": node_id,
                "status": "unreachable",
                "error": str(e)
            }
    
    def broadcast_packet(
        self,
        packet_json: Dict[str, Any],
        capability_filter: str = None
    ) -> List[Dict[str, Any]]:
        """
        Broadcast a packet to multiple nodes.
        
        Args:
            packet_json: IUPP packet to broadcast
            capability_filter: Optional filter for node capabilities
            
        Returns:
            List of responses from all nodes
        """
        responses = []
        
        for node_id in self.nodes:
            if capability_filter:
                if node_id not in self.find_nodes_by_capability(capability_filter):
                    continue
            
            response = self.route_packet(node_id, packet_json)
            responses.append(response)
        
        return responses


# Singleton instance
_registry_instance: Optional[NodeRegistry] = None


def get_node_registry() -> NodeRegistry:
    """
    Get or create the global node registry instance.
    
    Returns:
        NodeRegistry instance
    """
    global _registry_instance
    
    if _registry_instance is None:
        _registry_instance = NodeRegistry()
    
    return _registry_instance


if __name__ == "__main__":
    # Test the registry
    registry = NodeRegistry()
    
    # Register a test node
    result = registry.register_node(
        node_id="test-node-1",
        url="http://localhost:11434",
        api_key="test-key",
        capabilities=["internal-red-team-audit", "rtc-consensus-synthesis"]
    )
    print(f"Registration: {result}")
    
    # List all nodes
    print(f"\nAll nodes: {json.dumps(registry.get_all_nodes(), indent=2)}")
    
    # Find by capability
    matching = registry.find_nodes_by_capability("red-team")
    print(f"\nNodes with 'red-team': {matching}")
