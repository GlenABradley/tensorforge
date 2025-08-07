"""
Configuration Loader for Tensor Forge
Loads game configuration from YAML files for better maintainability.
"""
import yaml
import os
from pathlib import Path
from typing import Dict, Any, List, Optional

class ConfigLoader:
    """Loads and manages game configuration from YAML files"""
    
    def __init__(self, config_dir: Optional[str] = None):
        if config_dir is None:
            # Default to config directory relative to this file
            config_dir = Path(__file__).parent
        
        self.config_dir = Path(config_dir)
        self._levels_config = None
        self._components_config = None
        self._load_configs()
    
    def _load_configs(self):
        """Load all configuration files"""
        try:
            # Load levels configuration
            levels_file = self.config_dir / "levels.yaml"
            if levels_file.exists():
                with open(levels_file, 'r') as f:
                    self._levels_config = yaml.safe_load(f)
            else:
                print(f"Warning: levels.yaml not found at {levels_file}")
                self._levels_config = {"levels": {}, "concepts": {}}
            
            # Load components configuration
            components_file = self.config_dir / "components.yaml"
            if components_file.exists():
                with open(components_file, 'r') as f:
                    self._components_config = yaml.safe_load(f)
            else:
                print(f"Warning: components.yaml not found at {components_file}")
                self._components_config = {"components": {}, "categories": {}}
                
        except Exception as e:
            print(f"Error loading configurations: {e}")
            # Initialize with empty configs as fallback
            self._levels_config = {"levels": {}, "concepts": {}}
            self._components_config = {"components": {}, "categories": {}}
    
    def get_level_config(self, level_id: int) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific level"""
        if not self._levels_config:
            return None
        
        return self._levels_config.get("levels", {}).get(level_id)
    
    def get_all_levels(self) -> Dict[int, Dict[str, Any]]:
        """Get all level configurations"""
        return self._levels_config.get("levels", {})
    
    def get_component_config(self, component_id: str) -> Optional[Dict[str, Any]]:
        """Get configuration for a specific component"""
        if not self._components_config:
            return None
        
        return self._components_config.get("components", {}).get(component_id)
    
    def get_all_components(self) -> Dict[str, Dict[str, Any]]:
        """Get all component configurations"""
        return self._components_config.get("components", {})
    
    def get_component_categories(self) -> Dict[str, Dict[str, Any]]:
        """Get component categories for UI organization"""
        return self._components_config.get("categories", {})
    
    def get_concept_definitions(self) -> Dict[str, str]:
        """Get all concept definitions"""
        return self._levels_config.get("concepts", {})
    
    def get_levels_for_component(self, component_id: str) -> List[int]:
        """Get all levels where a component is available"""
        levels = []
        
        for level_id, level_config in self.get_all_levels().items():
            available_components = level_config.get("available_components", [])
            if component_id in available_components:
                levels.append(level_id)
        
        return sorted(levels)
    
    def get_components_for_level(self, level_id: int) -> List[str]:
        """Get all components available for a specific level"""
        level_config = self.get_level_config(level_id)
        if not level_config:
            return []
        
        return level_config.get("available_components", [])
    
    def get_level_concepts(self, level_id: int) -> List[str]:
        """Get concepts taught in a specific level"""
        level_config = self.get_level_config(level_id)
        if not level_config:
            return []
        
        return level_config.get("concepts", [])
    
    def get_concept_dependencies(self) -> Dict[str, List[str]]:
        """Get concept dependency relationships"""
        # This could be loaded from config in the future
        return {
            "deep_networks": ["neural_networks"],
            "layer_stacking": ["neural_networks", "deep_networks"],
            "activation": ["neural_networks"],
            "regularization": ["neural_networks", "training"],
            "pattern_recognition": ["neural_networks", "training"],
            "linear_models": ["neural_networks"],
            "weights": ["neural_networks"],
            "bias": ["neural_networks", "weights"],
            "tensor_operations": ["neural_networks"],
            "integration": ["neural_networks", "deep_networks"],
            "multi_task_learning": ["neural_networks", "training"],
            "ai_systems": ["neural_networks", "deep_networks", "integration"]
        }
    
    def validate_config(self) -> Dict[str, List[str]]:
        """Validate configuration for consistency"""
        issues = {
            "errors": [],
            "warnings": []
        }
        
        # Validate level prerequisites
        all_levels = self.get_all_levels()
        for level_id, level_config in all_levels.items():
            prerequisites = level_config.get("prerequisites", [])
            for prereq in prerequisites:
                if prereq not in all_levels:
                    issues["errors"].append(f"Level {level_id} requires non-existent level {prereq}")
        
        # Validate component references
        all_components = set(self.get_all_components().keys())
        for level_id, level_config in all_levels.items():
            for component_id in level_config.get("available_components", []):
                if component_id not in all_components:
                    issues["warnings"].append(f"Level {level_id} references undefined component {component_id}")
        
        return issues
    
    def reload_configs(self):
        """Reload configuration files (useful for development)"""
        self._load_configs()

# Global config loader instance
config_loader = ConfigLoader()