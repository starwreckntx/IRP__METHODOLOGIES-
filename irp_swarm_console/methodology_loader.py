"""
Methodology Loader Module
=========================
Scans and parses SKILL.md files from the skills directory to create
a lookup dictionary keyed by methodology name.
"""

import os
import re
from pathlib import Path
from typing import Dict, Optional, Any


class MethodologyLoader:
    """
    Loads and manages methodology files from the skills directory.
    """
    
    def __init__(self, skills_dir: str = None):
        """
        Initialize the methodology loader.
        
        Args:
            skills_dir: Path to the skills directory. Defaults to ./skills/
        """
        if skills_dir is None:
            # Default to skills directory relative to this file
            base_dir = Path(__file__).parent
            skills_dir = base_dir / "skills"
        
        self.skills_dir = Path(skills_dir)
        self.methodologies: Dict[str, Dict[str, Any]] = {}
        self._load_all_methodologies()
    
    def _load_all_methodologies(self) -> None:
        """Scan skills directory recursively and load all SKILL.md files."""
        if not self.skills_dir.exists():
            print(f"⚠️ Skills directory not found: {self.skills_dir}")
            return
        
        # Find all SKILL.md files
        skill_files = list(self.skills_dir.rglob("SKILL.md"))
        
        for skill_path in skill_files:
            methodology_name = self._derive_methodology_name(skill_path)
            methodology_data = self._parse_skill_file(skill_path)
            
            if methodology_data:
                self.methodologies[methodology_name] = methodology_data
                print(f"✅ Loaded methodology: {methodology_name}")
    
    def _derive_methodology_name(self, skill_path: Path) -> str:
        """
        Derive methodology name from folder path.
        
        Args:
            skill_path: Path to the SKILL.md file
            
        Returns:
            Methodology name (e.g., 'internal-red-team-audit')
        """
        # Get the parent folder name as the methodology name
        return skill_path.parent.name
    
    def _parse_skill_file(self, skill_path: Path) -> Optional[Dict[str, Any]]:
        """
        Parse a SKILL.md file and extract structured data.
        
        Args:
            skill_path: Path to the SKILL.md file
            
        Returns:
            Dictionary with parsed methodology data
        """
        try:
            content = skill_path.read_text(encoding='utf-8')
            
            # Extract metadata
            metadata = self._extract_metadata(content)
            
            # Extract sections
            sections = self._extract_sections(content)
            
            # Extract behavioral calibration
            calibration = self._extract_calibration(content)
            
            return {
                'path': str(skill_path),
                'content': content,
                'metadata': metadata,
                'sections': sections,
                'calibration': calibration,
                'name': metadata.get('name', skill_path.parent.name),
                'category': metadata.get('category', 'Uncategorized'),
                'version': metadata.get('version', '1.0.0')
            }
        except Exception as e:
            print(f"❌ Error parsing {skill_path}: {e}")
            return None
    
    def _extract_metadata(self, content: str) -> Dict[str, str]:
        """Extract metadata fields from SKILL.md content."""
        metadata = {}
        
        # Pattern for metadata items: - **Key:** Value
        pattern = r'\*\*(\w+):\*\*\s*(.+)'
        matches = re.findall(pattern, content)
        
        for key, value in matches:
            metadata[key.lower()] = value.strip()
        
        return metadata
    
    def _extract_sections(self, content: str) -> Dict[str, str]:
        """Extract major sections from SKILL.md content."""
        sections = {}
        
        # Split by ## headers
        section_pattern = r'^##\s+(.+?)$'
        parts = re.split(section_pattern, content, flags=re.MULTILINE)
        
        # Skip the first part (before first ##)
        for i in range(1, len(parts) - 1, 2):
            section_name = parts[i].strip()
            section_content = parts[i + 1].strip() if i + 1 < len(parts) else ''
            sections[section_name] = section_content
        
        return sections
    
    def _extract_calibration(self, content: str) -> Dict[str, Any]:
        """Extract behavioral calibration settings."""
        calibration = {}
        
        # Look for YAML-like calibration block
        yaml_pattern = r'```yaml\s*([\s\S]*?)```'
        yaml_match = re.search(yaml_pattern, content)
        
        if yaml_match:
            yaml_content = yaml_match.group(1)
            # Parse simple YAML-like key: value pairs
            for line in yaml_content.strip().split('\n'):
                if ':' in line:
                    key, value = line.split(':', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Try to convert to appropriate type
                    if value.lower() == 'true':
                        calibration[key] = True
                    elif value.lower() == 'false':
                        calibration[key] = False
                    elif value.lower() in ('high', 'medium', 'low'):
                        calibration[key] = value.lower()
                    else:
                        try:
                            calibration[key] = float(value)
                        except ValueError:
                            calibration[key] = value
        
        return calibration
    
    def get_methodology(self, name: str) -> Optional[Dict[str, Any]]:
        """
        Get a methodology by name.
        
        Args:
            name: Methodology name (e.g., 'internal-red-team-audit')
            
        Returns:
            Methodology data dictionary or None if not found
        """
        return self.methodologies.get(name)
    
    def get_methodology_content(self, name: str) -> Optional[str]:
        """
        Get raw content of a methodology file.
        
        Args:
            name: Methodology name
            
        Returns:
            Raw markdown content or None
        """
        methodology = self.get_methodology(name)
        return methodology.get('content') if methodology else None
    
    def list_methodologies(self) -> Dict[str, Dict[str, str]]:
        """
        List all available methodologies with basic info.
        
        Returns:
            Dictionary of methodology names to basic info
        """
        return {
            name: {
                'category': data.get('category', 'Unknown'),
                'version': data.get('version', '1.0.0'),
                'path': data.get('path', '')
            }
            for name, data in self.methodologies.items()
        }
    
    def search_methodologies(self, query: str) -> Dict[str, Dict[str, Any]]:
        """
        Search methodologies by name or content.
        
        Args:
            query: Search query string
            
        Returns:
            Matching methodologies
        """
        query_lower = query.lower()
        results = {}
        
        for name, data in self.methodologies.items():
            # Search in name
            if query_lower in name.lower():
                results[name] = data
                continue
            
            # Search in content
            if query_lower in data.get('content', '').lower():
                results[name] = data
                continue
            
            # Search in category
            if query_lower in data.get('category', '').lower():
                results[name] = data
        
        return results
    
    def get_by_category(self, category: str) -> Dict[str, Dict[str, Any]]:
        """
        Get all methodologies in a specific category.
        
        Args:
            category: Category name (partial match supported)
            
        Returns:
            Methodologies in the category
        """
        category_lower = category.lower()
        return {
            name: data
            for name, data in self.methodologies.items()
            if category_lower in data.get('category', '').lower()
        }
    
    def reload(self) -> None:
        """Reload all methodologies from disk."""
        self.methodologies.clear()
        self._load_all_methodologies()
    
    def get_protocol_instructions(self, name: str) -> Optional[str]:
        """
        Get the Protocol section for a methodology.
        
        Args:
            name: Methodology name
            
        Returns:
            Protocol section content or None
        """
        methodology = self.get_methodology(name)
        if methodology:
            sections = methodology.get('sections', {})
            return sections.get('Protocol', sections.get('protocol', None))
        return None


# Singleton instance for easy access
_loader_instance: Optional[MethodologyLoader] = None


def get_methodology_loader(skills_dir: str = None) -> MethodologyLoader:
    """
    Get or create the global methodology loader instance.
    
    Args:
        skills_dir: Optional skills directory path
        
    Returns:
        MethodologyLoader instance
    """
    global _loader_instance
    
    if _loader_instance is None:
        _loader_instance = MethodologyLoader(skills_dir)
    
    return _loader_instance


if __name__ == "__main__":
    # Test the loader
    loader = MethodologyLoader()
    
    print("\n📋 Available Methodologies:")
    for name, info in loader.list_methodologies().items():
        print(f"  - {name} ({info['category']})")
    
    print("\n🔍 Testing methodology lookup:")
    test_name = "internal-red-team-audit"
    methodology = loader.get_methodology(test_name)
    if methodology:
        print(f"  Found: {test_name}")
        print(f"  Category: {methodology['category']}")
        print(f"  Calibration: {methodology['calibration']}")
    else:
        print(f"  Not found: {test_name}")
