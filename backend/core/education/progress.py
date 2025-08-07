"""
Educational Progress Tracking
Tracks concept mastery, learning analytics, and adaptive difficulty.
"""
from typing import Dict, List, Any, Optional
from enum import Enum
from models.game_models import PlayerProgress, MasteryLevel, ComponentBuild
from core.levels.manager import levels_manager
import json
from pathlib import Path

class ConceptTracker:
    """Tracks player's understanding and mastery of AI concepts"""
    
    def __init__(self):
        self.concept_definitions = self._load_concept_definitions()
        self.concept_dependencies = self._load_concept_dependencies()
    
    def track_concept_exposure(self, player_progress: PlayerProgress, concept: str, level_id: int):
        """Track when a player is exposed to a concept"""
        if concept not in player_progress.concept_mastery:
            player_progress.concept_mastery[concept] = MasteryLevel.NOVICE
    
    def assess_concept_mastery(self, player_progress: PlayerProgress, concept: str) -> MasteryLevel:
        """Assess current mastery level of a concept"""
        return player_progress.concept_mastery.get(concept, MasteryLevel.NOVICE)
    
    def update_concept_mastery(self, player_progress: PlayerProgress, concept: str, 
                              performance_score: float, attempts: int):
        """Update concept mastery based on performance"""
        current_mastery = self.assess_concept_mastery(player_progress, concept)
        
        # Calculate mastery progression based on performance and attempts
        mastery_score = performance_score * (1.0 / max(1, attempts - 1)) if attempts > 1 else performance_score
        
        if mastery_score >= 0.95 and current_mastery.value != MasteryLevel.EXPERT.value:
            new_mastery = MasteryLevel.EXPERT
        elif mastery_score >= 0.85:
            new_mastery = MasteryLevel.PROFICIENT
        elif mastery_score >= 0.7:
            new_mastery = MasteryLevel.LEARNING
        else:
            new_mastery = MasteryLevel.NOVICE
        
        # Only advance mastery, don't regress
        if self._mastery_level_value(new_mastery) > self._mastery_level_value(current_mastery):
            player_progress.concept_mastery[concept] = new_mastery
    
    def recommend_review(self, player_progress: PlayerProgress) -> List[str]:
        """Recommend concepts that need review"""
        recommendations = []
        
        for concept, mastery in player_progress.concept_mastery.items():
            if mastery == MasteryLevel.NOVICE:
                recommendations.append(concept)
        
        # Sort by dependencies (prerequisites first)
        return self._sort_by_dependencies(recommendations)
    
    def get_mastery_summary(self, player_progress: PlayerProgress) -> Dict[str, Any]:
        """Get a summary of the player's concept mastery"""
        mastery_counts = {level.value: 0 for level in MasteryLevel}
        
        for mastery in player_progress.concept_mastery.values():
            mastery_counts[mastery.value] += 1
        
        total_concepts = len(player_progress.concept_mastery)
        
        return {
            "total_concepts": total_concepts,
            "mastery_breakdown": mastery_counts,
            "overall_progress": self._calculate_overall_progress(player_progress),
            "strong_areas": self._get_strong_concepts(player_progress),
            "areas_to_improve": self._get_weak_concepts(player_progress)
        }
    
    def _mastery_level_value(self, level: MasteryLevel) -> int:
        """Convert mastery level to numeric value for comparison"""
        level_values = {
            MasteryLevel.NOVICE: 0,
            MasteryLevel.LEARNING: 1,
            MasteryLevel.PROFICIENT: 2,
            MasteryLevel.EXPERT: 3
        }
        return level_values.get(level, 0)
    
    def _calculate_overall_progress(self, player_progress: PlayerProgress) -> float:
        """Calculate overall learning progress (0.0 to 1.0)"""
        if not player_progress.concept_mastery:
            return 0.0
        
        total_score = sum(self._mastery_level_value(mastery) for mastery in player_progress.concept_mastery.values())
        max_possible_score = len(player_progress.concept_mastery) * 3  # 3 = max mastery level
        
        return total_score / max_possible_score if max_possible_score > 0 else 0.0
    
    def _get_strong_concepts(self, player_progress: PlayerProgress) -> List[str]:
        """Get concepts the player has mastered well"""
        return [concept for concept, mastery in player_progress.concept_mastery.items() 
                if mastery in [MasteryLevel.PROFICIENT, MasteryLevel.EXPERT]]
    
    def _get_weak_concepts(self, player_progress: PlayerProgress) -> List[str]:
        """Get concepts that need more work"""
        return [concept for concept, mastery in player_progress.concept_mastery.items()
                if mastery == MasteryLevel.NOVICE]
    
    def _sort_by_dependencies(self, concepts: List[str]) -> List[str]:
        """Sort concepts by their dependencies (prerequisites first)"""
        # Simple topological sort based on dependencies
        sorted_concepts = []
        remaining = set(concepts)
        
        while remaining:
            # Find concepts with no remaining dependencies
            ready = []
            for concept in remaining:
                deps = self.concept_dependencies.get(concept, [])
                if not any(dep in remaining for dep in deps):
                    ready.append(concept)
            
            if not ready:
                # Break cycles by taking any remaining concept
                ready.append(next(iter(remaining)))
            
            for concept in ready:
                sorted_concepts.append(concept)
                remaining.remove(concept)
        
        return sorted_concepts
    
    def _load_concept_definitions(self) -> Dict[str, str]:
        """Load concept definitions and explanations"""
        return {
            "neural_networks": "Networks of artificial neurons that can learn patterns from data",
            "training": "The process of teaching AI by showing it examples",
            "classification": "Teaching AI to categorize or label different types of data",
            "tensor_operations": "Mathematical operations on multi-dimensional data arrays",
            "deep_networks": "Neural networks with multiple layers for learning complex patterns",
            "layer_stacking": "Combining multiple processing layers to build sophisticated AI",
            "activation": "Functions that help neurons make non-linear decisions",
            "regularization": "Techniques to prevent AI from memorizing instead of learning",
            "pattern_recognition": "The ability to identify meaningful structures in data",
            "linear_models": "Simple AI models that find straight-line relationships in data",
            "weights": "Parameters that determine how much attention AI pays to each input",
            "bias": "AI's initial assumptions or starting point for making decisions"
        }
    
    def _load_concept_dependencies(self) -> Dict[str, List[str]]:
        """Load concept dependency relationships"""
        return {
            "deep_networks": ["neural_networks"],
            "layer_stacking": ["neural_networks", "deep_networks"],
            "activation": ["neural_networks"],
            "regularization": ["neural_networks", "training"],
            "pattern_recognition": ["neural_networks", "training"],
            "linear_models": ["neural_networks"],
            "weights": ["neural_networks"],
            "bias": ["neural_networks", "weights"]
        }

class LearningAnalytics:
    """Analyzes player learning patterns and provides insights"""
    
    def __init__(self):
        self.analytics_data = {}
    
    def track_player_journey(self, player_id: str, action: str, level_id: int, 
                           build: Optional[ComponentBuild] = None, **kwargs):
        """Track a player action for analytics"""
        if player_id not in self.analytics_data:
            self.analytics_data[player_id] = {
                "actions": [],
                "level_attempts": {},
                "common_mistakes": [],
                "learning_patterns": {}
            }
        
        action_data = {
            "action": action,
            "level_id": level_id,
            "timestamp": self._get_timestamp(),
            **kwargs
        }
        
        if build:
            action_data["components_used"] = [comp.get("id", "") for comp in build.components]
            action_data["component_count"] = len(build.components)
        
        self.analytics_data[player_id]["actions"].append(action_data)
        
        # Track level attempts
        if level_id not in self.analytics_data[player_id]["level_attempts"]:
            self.analytics_data[player_id]["level_attempts"][level_id] = 0
        self.analytics_data[player_id]["level_attempts"][level_id] += 1
    
    def analyze_common_mistakes(self, level_id: int) -> List[Dict[str, Any]]:
        """Analyze common mistakes across all players for a level"""
        mistakes = []
        
        for player_data in self.analytics_data.values():
            for action in player_data["actions"]:
                if action["level_id"] == level_id and action["action"] == "failed_attempt":
                    mistake = {
                        "level_id": level_id,
                        "error_type": action.get("error_type", "unknown"),
                        "components_used": action.get("components_used", []),
                        "component_count": action.get("component_count", 0)
                    }
                    mistakes.append(mistake)
        
        # Group and count similar mistakes
        mistake_patterns = {}
        for mistake in mistakes:
            pattern_key = f"{mistake['error_type']}_{mistake['component_count']}"
            if pattern_key not in mistake_patterns:
                mistake_patterns[pattern_key] = {"count": 0, "details": mistake}
            mistake_patterns[pattern_key]["count"] += 1
        
        return sorted(mistake_patterns.values(), key=lambda x: x["count"], reverse=True)
    
    def generate_difficulty_report(self) -> Dict[str, Any]:
        """Generate a report on level difficulty based on player data"""
        level_stats = {}
        
        for player_data in self.analytics_data.values():
            for level_id, attempts in player_data["level_attempts"].items():
                if level_id not in level_stats:
                    level_stats[level_id] = {
                        "total_attempts": 0,
                        "total_players": 0,
                        "completion_rates": []
                    }
                
                level_stats[level_id]["total_attempts"] += attempts
                level_stats[level_id]["total_players"] += 1
                
                # Estimate completion based on attempts (simplified)
                completion_rate = 1.0 / attempts if attempts > 0 else 0
                level_stats[level_id]["completion_rates"].append(completion_rate)
        
        # Calculate difficulty metrics
        difficulty_report = {}
        for level_id, stats in level_stats.items():
            avg_attempts = stats["total_attempts"] / stats["total_players"] if stats["total_players"] > 0 else 0
            avg_completion_rate = sum(stats["completion_rates"]) / len(stats["completion_rates"]) if stats["completion_rates"] else 0
            
            difficulty_score = avg_attempts * (1 - avg_completion_rate)  # Higher = more difficult
            
            if difficulty_score > 3:
                difficulty = "Very Hard"
            elif difficulty_score > 2:
                difficulty = "Hard"
            elif difficulty_score > 1:
                difficulty = "Medium"
            else:
                difficulty = "Easy"
            
            difficulty_report[level_id] = {
                "difficulty": difficulty,
                "avg_attempts": avg_attempts,
                "avg_completion_rate": avg_completion_rate,
                "difficulty_score": difficulty_score,
                "total_players": stats["total_players"]
            }
        
        return difficulty_report
    
    def get_player_insights(self, player_id: str) -> Dict[str, Any]:
        """Get learning insights for a specific player"""
        if player_id not in self.analytics_data:
            return {"error": "No data found for player"}
        
        player_data = self.analytics_data[player_id]
        
        # Calculate learning velocity (levels per hour)
        if len(player_data["actions"]) >= 2:
            first_action_time = player_data["actions"][0]["timestamp"]
            last_action_time = player_data["actions"][-1]["timestamp"]
            time_span_hours = (last_action_time - first_action_time) / 3600
            levels_completed = len(player_data["level_attempts"])
            learning_velocity = levels_completed / time_span_hours if time_span_hours > 0 else 0
        else:
            learning_velocity = 0
        
        # Analyze preferred components
        component_usage = {}
        for action in player_data["actions"]:
            for component in action.get("components_used", []):
                component_usage[component] = component_usage.get(component, 0) + 1
        
        preferred_components = sorted(component_usage.items(), key=lambda x: x[1], reverse=True)[:5]
        
        return {
            "learning_velocity": learning_velocity,
            "total_actions": len(player_data["actions"]),
            "levels_attempted": len(player_data["level_attempts"]),
            "avg_attempts_per_level": sum(player_data["level_attempts"].values()) / len(player_data["level_attempts"]) if player_data["level_attempts"] else 0,
            "preferred_components": preferred_components,
            "learning_style": self._infer_learning_style(player_data)
        }
    
    def _infer_learning_style(self, player_data: Dict) -> str:
        """Infer player's learning style from their behavior"""
        total_actions = len(player_data["actions"])
        if total_actions == 0:
            return "unknown"
        
        # Count different types of actions
        quick_attempts = sum(1 for action in player_data["actions"] 
                           if action.get("time_spent", 0) < 30)  # Less than 30 seconds
        
        if quick_attempts / total_actions > 0.7:
            return "trial_and_error"  # Prefers trying quickly
        elif sum(player_data["level_attempts"].values()) / len(player_data["level_attempts"]) > 3:
            return "methodical"  # Takes time, multiple careful attempts
        else:
            return "balanced"  # Mix of both approaches
    
    def _get_timestamp(self) -> int:
        """Get current timestamp"""
        import time
        return int(time.time())

# Global instances
concept_tracker = ConceptTracker()
learning_analytics = LearningAnalytics()