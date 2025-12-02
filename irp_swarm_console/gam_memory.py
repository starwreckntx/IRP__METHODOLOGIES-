"""
GAM (General Agentic Memory) Module
===================================
Persistent memory system using JSONL file storage.
Tracks session history, interactions, and provides context for IUPP packets.
"""

import json
import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict


@dataclass
class GAMEntry:
    """A single entry in the GAM journey log."""
    session_id: str
    timestamp: str
    user_input: str
    node_used: str
    resultant_seed: str
    protocol_packet: Dict[str, Any]
    entry_id: str = ""
    
    def __post_init__(self):
        if not self.entry_id:
            self.entry_id = str(uuid.uuid4())
    
    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "GAMEntry":
        return cls(**data)


class GAMMemory:
    """
    General Agentic Memory system.
    Provides persistent storage and retrieval of session interactions.
    """
    
    def __init__(self, log_path: str = None):
        """
        Initialize GAM memory system.
        
        Args:
            log_path: Path to the JSONL log file. 
                     Defaults to gam_journey_log.jsonl in the module directory.
        """
        if log_path is None:
            base_dir = Path(__file__).parent
            log_path = base_dir / "gam_journey_log.jsonl"
        
        self.log_path = Path(log_path)
        self.entries: List[GAMEntry] = []
        self.current_session_id: str = str(uuid.uuid4())
        
        # Load existing history on startup
        self._load_history()
    
    def _load_history(self) -> None:
        """Load existing entries from JSONL file."""
        if not self.log_path.exists():
            print(f"📝 Creating new GAM log: {self.log_path}")
            return
        
        try:
            with open(self.log_path, 'r', encoding='utf-8') as f:
                for line in f:
                    line = line.strip()
                    if line:
                        try:
                            data = json.loads(line)
                            entry = GAMEntry.from_dict(data)
                            self.entries.append(entry)
                        except json.JSONDecodeError as e:
                            print(f"⚠️ Skipping malformed line: {e}")
            
            print(f"📂 Loaded {len(self.entries)} GAM entries")
            
        except Exception as e:
            print(f"❌ Error loading GAM history: {e}")
    
    def load_history(self) -> List[Dict[str, Any]]:
        """
        Public method to load and return history.
        
        Returns:
            List of entry dictionaries
        """
        return [entry.to_dict() for entry in self.entries]
    
    def append_entry(
        self,
        user_input: str,
        node_used: str,
        resultant_seed: str,
        protocol_packet: Dict[str, Any],
        session_id: str = None
    ) -> GAMEntry:
        """
        Append a new entry to the GAM log.
        
        Args:
            user_input: Original user input/command
            node_used: Node that processed the request
            resultant_seed: Output/result from processing
            protocol_packet: The IUPP packet used
            session_id: Optional session ID (uses current session if not provided)
            
        Returns:
            The created GAMEntry
        """
        entry = GAMEntry(
            session_id=session_id or self.current_session_id,
            timestamp=datetime.utcnow().isoformat() + "Z",
            user_input=user_input,
            node_used=node_used,
            resultant_seed=resultant_seed,
            protocol_packet=protocol_packet
        )
        
        self.entries.append(entry)
        self._persist_entry(entry)
        
        return entry
    
    def _persist_entry(self, entry: GAMEntry) -> None:
        """
        Append an entry to the JSONL file.
        
        Args:
            entry: Entry to persist
        """
        try:
            with open(self.log_path, 'a', encoding='utf-8') as f:
                json_line = json.dumps(entry.to_dict(), ensure_ascii=False)
                f.write(json_line + '\n')
        except Exception as e:
            print(f"❌ Error persisting GAM entry: {e}")
    
    def query_history(
        self,
        filters: Dict[str, Any] = None,
        limit: int = None
    ) -> List[Dict[str, Any]]:
        """
        Search and filter past entries.
        
        Args:
            filters: Dictionary of field-value pairs to filter by
                    Supported filters:
                    - session_id: Match specific session
                    - node_used: Match specific node
                    - search_text: Search in user_input and resultant_seed
                    - after: ISO timestamp, entries after this time
                    - before: ISO timestamp, entries before this time
            limit: Maximum number of results to return
            
        Returns:
            List of matching entry dictionaries
        """
        results = []
        
        for entry in self.entries:
            if filters:
                # Session filter
                if 'session_id' in filters:
                    if entry.session_id != filters['session_id']:
                        continue
                
                # Node filter
                if 'node_used' in filters:
                    if entry.node_used != filters['node_used']:
                        continue
                
                # Text search
                if 'search_text' in filters:
                    search = filters['search_text'].lower()
                    if search not in entry.user_input.lower() and \
                       search not in entry.resultant_seed.lower():
                        continue
                
                # Time range filters
                if 'after' in filters:
                    if entry.timestamp < filters['after']:
                        continue
                
                if 'before' in filters:
                    if entry.timestamp > filters['before']:
                        continue
            
            results.append(entry.to_dict())
        
        # Apply limit
        if limit:
            results = results[-limit:]  # Get most recent
        
        return results
    
    def get_context_for_injection(
        self,
        max_entries: int = 5,
        relevance_query: str = None
    ) -> str:
        """
        Get relevant history formatted for IUPP packet context injection.
        
        Args:
            max_entries: Maximum number of entries to include
            relevance_query: Optional query to filter relevant entries
            
        Returns:
            Formatted context string for injection
        """
        if not self.entries:
            return "No prior context available."
        
        # Filter by relevance if query provided
        if relevance_query:
            filtered = self.query_history(
                filters={'search_text': relevance_query},
                limit=max_entries
            )
        else:
            # Get most recent entries from current session
            filtered = self.query_history(
                filters={'session_id': self.current_session_id},
                limit=max_entries
            )
            
            # Fall back to all recent if no current session entries
            if not filtered:
                filtered = self.query_history(limit=max_entries)
        
        if not filtered:
            return "No prior context available."
        
        # Format for injection
        context_parts = ["=== GAM Context Injection ===\n"]
        
        for entry in filtered:
            context_parts.append(f"""
--- Entry [{entry['timestamp']}] ---
Session: {entry['session_id'][:8]}...
Input: {entry['user_input'][:200]}{'...' if len(entry['user_input']) > 200 else ''}
Node: {entry['node_used']}
Result Summary: {entry['resultant_seed'][:300]}{'...' if len(entry['resultant_seed']) > 300 else ''}
""")
        
        context_parts.append("\n=== End GAM Context ===")
        
        return '\n'.join(context_parts)
    
    def get_session_history(self, session_id: str = None) -> List[Dict[str, Any]]:
        """
        Get all entries for a specific session.
        
        Args:
            session_id: Session to retrieve (current session if None)
            
        Returns:
            List of entries for the session
        """
        target_session = session_id or self.current_session_id
        return self.query_history(filters={'session_id': target_session})
    
    def start_new_session(self) -> str:
        """
        Start a new session with fresh session ID.
        
        Returns:
            New session ID
        """
        self.current_session_id = str(uuid.uuid4())
        return self.current_session_id
    
    def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the GAM memory.
        
        Returns:
            Statistics dictionary
        """
        session_ids = set(e.session_id for e in self.entries)
        nodes_used = set(e.node_used for e in self.entries)
        
        return {
            "total_entries": len(self.entries),
            "unique_sessions": len(session_ids),
            "unique_nodes": len(nodes_used),
            "nodes_list": list(nodes_used),
            "current_session": self.current_session_id,
            "current_session_entries": len([
                e for e in self.entries 
                if e.session_id == self.current_session_id
            ]),
            "log_file": str(self.log_path)
        }
    
    def clear_session(self, session_id: str = None) -> int:
        """
        Clear entries for a specific session (in memory only).
        Note: Does not modify the JSONL file.
        
        Args:
            session_id: Session to clear (current if None)
            
        Returns:
            Number of entries removed
        """
        target = session_id or self.current_session_id
        before = len(self.entries)
        self.entries = [e for e in self.entries if e.session_id != target]
        return before - len(self.entries)
    
    def export_session(self, session_id: str = None) -> str:
        """
        Export a session's entries as JSON.
        
        Args:
            session_id: Session to export
            
        Returns:
            JSON string of session entries
        """
        entries = self.get_session_history(session_id)
        return json.dumps(entries, indent=2, ensure_ascii=False)


# Singleton instance
_gam_instance: Optional[GAMMemory] = None


def get_gam_memory(log_path: str = None) -> GAMMemory:
    """
    Get or create the global GAM memory instance.
    
    Args:
        log_path: Optional path to JSONL log file
        
    Returns:
        GAMMemory instance
    """
    global _gam_instance
    
    if _gam_instance is None:
        _gam_instance = GAMMemory(log_path)
    
    return _gam_instance


if __name__ == "__main__":
    # Test the GAM system
    gam = GAMMemory()
    
    print(f"📊 GAM Stats: {json.dumps(gam.get_stats(), indent=2)}")
    
    # Add a test entry
    entry = gam.append_entry(
        user_input="Test input for GAM",
        node_used="test-node",
        resultant_seed="Test result output",
        protocol_packet={"test": "packet"}
    )
    print(f"\n✅ Added entry: {entry.entry_id}")
    
    # Get context for injection
    context = gam.get_context_for_injection()
    print(f"\n📋 Context for injection:\n{context}")
    
    # Query history
    history = gam.query_history(limit=5)
    print(f"\n📜 Recent history ({len(history)} entries)")
