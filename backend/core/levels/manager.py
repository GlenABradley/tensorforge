"""
Enhanced Levels Manager
Manages educational AI levels with comprehensive progression system.
"""
from typing import Dict, List, Optional, Any
from models.game_models import LevelConfig, PlayerProgress, ComponentType
from core.components.registry import component_registry
import json
import os

class LevelsManager:
    """Enhanced manager for educational AI levels and progression"""
    
    def __init__(self):
        self.levels: Dict[int, LevelConfig] = {}
        self.level_dependencies: Dict[int, List[int]] = {}
        self._initialize_levels()
    
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
    
    def _initialize_levels(self):
        """Initialize all levels with their configurations"""
        
        # Level 1: Train Your First AI Pet
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
        
        # Level 2: Build Your First Neural Network  
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
        
        # Level 3: Pattern Detective
        self.levels[3] = LevelConfig(
            id=3,
            title="Pattern Detective",
            description="Build an AI that finds hidden patterns in data", 
            objective="Create a simple linear model to find patterns",
            concepts=["linear_models", "weights", "bias", "pattern_recognition"],
            available_components=["neural_layer", "activation_relu", "dense_layer", "tensor_add", "tensor_multiply"],
            success_criteria={
                "accuracy_threshold": 0.75,
                "pattern_recognition": True,
                "required_operations": ["tensor_add", "tensor_multiply"]
            },
            hints=[
                "Use tensor operations to transform your input data.",
                "Try combining addition and multiplication to find patterns.", 
                "Linear models use weighted combinations - multiplication helps with weighting!",
                "Remember: your AI needs to both process (multiply) and combine (add) information."
            ],
            educational_content={
                "intro": "Every AI is a pattern detective - let's teach yours to find clues!",
                "concepts_explained": {
                    "linear_models": "A simple AI that draws straight lines through data",
                    "weights": "How much the AI pays attention to each input",
                    "bias": "The AI's starting assumption about the answer",
                    "pattern_recognition": "Finding meaningful relationships in data"
                }
            },
            type="standard",
            prerequisites=[2]
        )
        
        # Mini-Boss 1: Smart Pet Challenge
        self.levels[4] = LevelConfig(
            id=4,
            title="Smart Pet Challenge",
            description="MINI-BOSS: Combine everything to create the ultimate AI pet!",
            objective="Build a complete AI system using Levels 1-3 knowledge",
            concepts=["integration", "multi_task_learning", "ai_systems"],
            available_components=["neural_layer", "activation_relu", "dense_layer", "dropout", "tensor_add", "tensor_multiply"],
            success_criteria={
                "accuracy_threshold": 0.9,
                "multi_task_performance": True,
                "architecture_complexity": 4,  # At least 4 components
                "efficiency_threshold": 0.88
            },
            hints=[
                "This is a challenge level - you'll need to use everything you've learned!",
                "Build a deep network with multiple layers for better performance.",
                "Include regularization (Dropout) to make your AI more robust.",
                "Use tensor operations to preprocess your data effectively.",
                "Aim for at least 4 components in a well-structured architecture."
            ],
            educational_content={
                "intro": "Time for your AI to prove itself! Can it handle multiple challenges?",
                "victory_message": "Congratulations! Your AI pet is now officially smart!",
                "concepts_explained": {
                    "integration": "Combining multiple AI techniques for better performance",
                    "multi_task_learning": "Training AI to handle several related tasks",
                    "ai_systems": "Complete AI solutions that combine many components"
                }
            },
            type="mini_boss",
            prerequisites=[3]
        )

# Global levels manager instance
levels_manager = LevelsManager()