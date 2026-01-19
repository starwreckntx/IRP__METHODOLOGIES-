"""
Guardian_Codex Hardened Logic Engine
====================================
Implements robust protection against recursion and circular reference attacks.
Part of the IRP v2.0 'DIFFUSE' protocol.
"""

import logging
import json
from typing import Dict, List, Set, Any, Optional

# --- Configuration ---
MAX_RECURSION_DEPTH = 50
FAILURE_THRESHOLD = 5

class LogicError(Exception):
    """Base exception for logic engine errors."""
    pass

class RecursionLimitExceeded(LogicError):
    """Raised when the maximum recursion depth is exceeded."""
    pass

class CircularReferenceDetected(LogicError):
    """Raised when a circular reference is detected between laws."""
    pass

class CircuitBreakerOpen(LogicError):
    """Raised when the circuit breaker is in an open (failed) state."""
    pass


class LogicCircuitBreaker:
    """
    Prevents cascading failures by stopping execution after a threshold of faults.
    """
    def __init__(self, threshold: int = FAILURE_THRESHOLD):
        self.failure_count = 0
        self.threshold = threshold
        self.is_open = False

    def report_failure(self):
        self.failure_count += 1
        if self.failure_count >= self.threshold:
            self.is_open = True
            logging.error("CRITICAL: Logic Engine Circuit Breaker OPENED.")

    def reset(self):
        self.failure_count = 0
        self.is_open = False


class HardenedLogicEngine:
    """
    The core logic engine for the Guardian_Codex with built-in protections.
    """
    def __init__(self):
        self.circuit_breaker = LogicCircuitBreaker()
        self.laws: Dict[str, Dict[str, Any]] = {}

    def register_laws(self, laws: List[Dict[str, Any]]):
        """Register a set of laws for processing."""
        for law in laws:
            self.laws[law['law_id']] = law

    def process_law(self, law_id: str, depth: int = 0, visited: Set[str] = None) -> bool:
        """
        Processes a law and its dependencies with recursion and circularity checks.
        """
        if self.circuit_breaker.is_open:
            raise CircuitBreakerOpen("Logic engine is in failsafe mode.")

        if visited is None:
            visited = set()

        # 1. Check Recursion Depth
        if depth > MAX_RECURSION_DEPTH:
            self.circuit_breaker.report_failure()
            raise RecursionLimitExceeded(f"Max depth {MAX_RECURSION_DEPTH} exceeded at {law_id}")

        # 2. Check Circular References
        if law_id in visited:
            self.circuit_breaker.report_failure()
            raise CircularReferenceDetected(f"Circular reference detected: {law_id}")

        if law_id not in self.laws:
            # Mycelial Hook: Log unknown law but don't necessarily crash
            logging.warning(f"Unknown law encountered: {law_id}")
            return True

        # 3. Process Law Logic
        visited.add(law_id)
        law = self.laws[law_id]
        
        # Simulate dependency processing
        for ref in law.get('references', []):
            try:
                self.process_law(ref, depth + 1, visited.copy())
            except (RecursionLimitExceeded, CircularReferenceDetected) as e:
                # Log and re-raise to be caught by circuit breaker or caller
                logging.error(f"Logic failure in dependency {ref} of {law_id}: {e}")
                raise

        return True

    def validate_constitution(self) -> Dict[str, Any]:
        """
        Performs a full scan of all registered laws to ensure no systemic faults.
        """
        results = {"valid": True, "errors": []}
        for law_id in self.laws:
            try:
                self.process_law(law_id)
            except LogicError as e:
                results["valid"] = False
                results["errors"].append(str(e))
        
        return results

# --- Mycelial Integration (DIFFUSE) ---
def mycelial_integrity_hook(packet: Dict[str, Any]) -> Dict[str, Any]:
    """
    Decentralized hook for checking packet logic before propagation.
    Extracts laws from the packet payload and validates them against the engine.
    """
    engine = HardenedLogicEngine()
    results = {"valid": True, "errors": [], "warnings": []}

    try:
        # 1. Extract laws from payload
        payload = packet.get("payload", {})
        input_seed = payload.get("input_seed", "")
        
        # In this protocol, laws can be passed in 'metadata' or embedded in 'input_seed' as JSON
        candidate_laws = []
        
        # Check metadata for explicit laws
        metadata = packet.get("metadata", {})
        if "laws" in metadata:
            candidate_laws.extend(metadata["laws"])
            
        # Check input_seed if it's a JSON string containing laws
        if isinstance(input_seed, str) and input_seed.strip().startswith("{"):
            try:
                seed_data = json.loads(input_seed)
                if "laws" in seed_data:
                    candidate_laws.extend(seed_data["laws"])
            except json.JSONDecodeError:
                pass

        if not candidate_laws:
            results["warnings"].append("No candidate laws found in packet for validation.")
            return results

        # 2. Register and Validate
        engine.register_laws(candidate_laws)
        validation = engine.validate_constitution()
        
        if not validation["valid"]:
            results["valid"] = False
            results["errors"].extend(validation["errors"])

    except Exception as e:
        results["valid"] = False
        results["errors"].append(f"Hook Execution Error: {str(e)}")

    return results
