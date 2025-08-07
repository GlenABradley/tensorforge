"""
Enhanced Levels Manager - Configuration Driven
Manages educational AI levels with comprehensive progression system using YAML configuration.
"""
from typing import Dict, List, Optional, Any
from models.game_models import LevelConfig, PlayerProgress, ComponentType
from core.components.registry import component_registry
from config.config_loader import config_loader
import json
import os

class LevelsManager:
    """Enhanced manager for educational AI levels and progression"""
    
    def __init__(self):
        self.levels: Dict[int, LevelConfig] = {}
        self.level_dependencies: Dict[int, List[int]] = {}
        self._initialize_levels_from_config()
    
    def get_level(self, level_id: int) -> Optional[LevelConfig]:
        """Get level configuration by ID"""
        return self.levels.get(level_id)
    
    def get_available_levels(self, player_progress: PlayerProgress) -> List[int]:
        """Get list of levels available to the player"""
        available = []
        for level_id, level_config in self.levels.items():
            if self._is_level_unlocked(level_id, player_progress):
                available.append(level_id)
        return sorted(available)
    
    def get_level_concepts(self, level_id: int) -> List[str]:
        """Get concepts taught in a specific level"""
        level = self.get_level(level_id)
        return level.concepts if level else []
    
    def get_concepts_learned(self, player_progress: PlayerProgress) -> List[str]:
        """Get all concepts the player has learned"""
        concepts = set()
        for level_id in player_progress.completed_levels.keys():
            concepts.update(self.get_level_concepts(level_id))
        return sorted(list(concepts))
    
    def get_next_level(self, current_level: int, player_progress: PlayerProgress) -> Optional[int]:
        """Get the next recommended level"""
        available_levels = self.get_available_levels(player_progress)
        higher_levels = [l for l in available_levels if l > current_level]
        return min(higher_levels) if higher_levels else None
    
    def mark_level_complete(self, level_id: int, player_progress: PlayerProgress, 
                           score: float, time_taken: int, attempts: int = 1):
        """Mark a level as completed and update progress"""
        level_record = {
            'completed': True,
            'score': score,
            'time_taken': time_taken,
            'attempts': attempts,
            'timestamp': self._get_timestamp()
        }
        
        player_progress.completed_levels[level_id] = level_record
        
        # Update concept mastery
        level_concepts = self.get_level_concepts(level_id)
        for concept in level_concepts:
            # Simple mastery calculation based on score and attempts
            mastery_score = score * (1.0 / attempts) 
            if mastery_score >= 0.9:
                player_progress.concept_mastery[concept] = "proficient"
            elif mastery_score >= 0.7:
                player_progress.concept_mastery[concept] = "learning"
            else:
                player_progress.concept_mastery[concept] = "novice"
    
    def get_level_difficulty_rating(self, level_id: int) -> str:
        """Get difficulty rating for a level"""
        level = self.get_level(level_id)
        if not level:
            return "unknown"
        
        if level.type == "final_boss":
            return "expert"
        elif level.type == "mini_boss":
            return "challenging"
        elif level_id <= 3:
            return "beginner"
        elif level_id <= 8:
            return "intermediate"
        else:
            return "advanced"
    
    def _is_level_unlocked(self, level_id: int, player_progress: PlayerProgress) -> bool:
        """Check if a level is unlocked for the player"""
        level = self.get_level(level_id)
        if not level:
            return False
        
        # Level 1 is always unlocked
        if level_id == 1:
            return True
        
        # Check prerequisites
        for prereq in level.prerequisites:
            if prereq not in player_progress.completed_levels:
                return False
        
        # For standard progression, just check if previous level is complete
        if level_id - 1 in self.levels and level_id - 1 not in player_progress.completed_levels:
            return False
        
        return True
    
    def _get_timestamp(self) -> int:
        """Get current timestamp"""
        import time
        return int(time.time())
    
    def _initialize_levels_from_config(self):
        """Initialize levels from YAML configuration"""
        try:
            levels_config = config_loader.get_all_levels()
            
            for level_id, level_data in levels_config.items():
                # Convert level_id to int if it's a string
                if isinstance(level_id, str):
                    level_id = int(level_id)
                
                # Create LevelConfig from YAML data
                self.levels[level_id] = LevelConfig(
                    id=level_data.get('id', level_id),
                    title=level_data.get('title', f'Level {level_id}'),
                    description=level_data.get('description', ''),
                    objective=level_data.get('objective', ''),
                    concepts=level_data.get('concepts', []),
                    available_components=level_data.get('available_components', []),
                    success_criteria=level_data.get('success_criteria', {}),
                    hints=level_data.get('hints', []),
                    educational_content=level_data.get('educational_content', {}),
                    type=level_data.get('type', 'standard'),
                    prerequisites=level_data.get('prerequisites', []),
                    max_attempts=level_data.get('max_attempts'),
                    time_limit=level_data.get('time_limit')
                )
            
            print(f"📚 Loaded {len(self.levels)} levels from configuration")
            
            # Validate configuration
            validation_result = config_loader.validate_config()
            if validation_result["errors"]:
                print("⚠️  Configuration errors found:")
                for error in validation_result["errors"]:
                    print(f"   - {error}")
            
            if validation_result["warnings"]:
                print("⚠️  Configuration warnings:")
                for warning in validation_result["warnings"]:
                    print(f"   - {warning}")
                    
        except Exception as e:
            print(f"❌ Error loading levels from config: {e}")
            print("   Falling back to hardcoded levels...")
            self._initialize_fallback_levels()
    
    def _initialize_fallback_levels(self):
        """Fallback to hardcoded levels if config fails"""
        # Keep the original hardcoded levels as fallback
        self.levels[1] = LevelConfig(
            id=1,
            title="Train Your First AI Pet",
            description="Draw shapes and watch your AI learn to recognize them!",
            objective="Train a neural network to classify hand-drawn shapes",
            concepts=["neural_networks", "training", "classification"],
            available_components=["neural_layer", "activation_relu"],
            success_criteria={
                "accuracy_threshold": 0.8,
                "required_components": ["neural_layer"],
                "min_training_examples": 3
            },
            hints=[
                "Try adding a Neural Layer first to give your AI a brain!",
                "Don't forget the Activation Function - it helps your AI think in complex ways!",
                "Draw at least 3 different shapes to teach your AI properly.",
                "Make sure to include both a Neural Layer AND an Activation Function."
            ],
            educational_content={
                "intro": "Welcome to AI training! You're about to create your first artificial intelligence.",
                "concepts_explained": {
                    "neural_network": "A network of artificial neurons that can learn patterns",
                    "training": "Teaching the AI by showing it examples", 
                    "classification": "The AI learns to put things into categories"
                }
            },
            type="standard"
        )
        
        self.levels[2] = LevelConfig(
            id=2,
            title="Build Your First Neural Network", 
            description="Learn to stack layers and create deeper AI networks!",
            objective="Build a multi-layer neural network and understand tensor flow",
            concepts=["deep_networks", "layer_stacking", "tensor_operations"],
            available_components=["neural_layer", "activation_relu", "dense_layer", "dropout"],
            success_criteria={
                "efficiency_threshold": 0.85,
                "required_components": ["neural_layer", "activation_relu"],
                "min_components": 3,
                "bonus_components": ["dense_layer", "dropout"]
            },
            hints=[
                "Start with a Neural Layer as your foundation.",
                "Add a Dense Layer to make your network deeper and smarter.",
                "Don't forget an Activation Function - your network needs non-linearity!",
                "Try adding Dropout to prevent overfitting and improve performance.",
                "You need at least 3 components, but more layers often work better!"
            ],
            educational_content={
                "intro": "Now let's build a more sophisticated AI! Deep networks can learn complex patterns.",
                "concepts_explained": {
                    "deep_networks": "Networks with multiple layers can learn increasingly complex features",
                    "layer_stacking": "Each layer processes and transforms the data before passing it on",
                    "tensor_operations": "Mathematical operations on multi-dimensional data arrays"
                }
            },
            type="standard",
            prerequisites=[1]
        )

# Global levels manager instance
levels_manager = LevelsManager()