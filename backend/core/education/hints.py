"""
Adaptive Hint System
Provides intelligent, context-aware hints based on player progress and mistakes.
"""
from typing import List, Dict, Any, Optional
from ..models.game_models import Hint, HintAnalysis, ComponentBuild, ValidationResult, PlayerProgress
from ..levels.manager import levels_manager
import random

class AdaptiveHintSystem:
    """Intelligent hint generation system that adapts to player needs"""
    
    def __init__(self):
        self.hint_templates = self._load_hint_templates()
        self.concept_hints = self._load_concept_hints()
    
    def analyze_attempt(self, build: ComponentBuild, result: ValidationResult, 
                       level_id: int, attempt_count: int = 1, time_spent: int = 0) -> HintAnalysis:
        """Analyze a player's attempt to determine what hints to provide"""
        
        missing_components = []
        incorrect_connections = []
        conceptual_gaps = []
        
        # Analyze validation issues
        for issue in result.issues:
            if issue.type == "missing_required_component":
                missing_components.append(issue.component_id or "unknown")
            elif issue.type == "sequence_error":
                incorrect_connections.append(issue.component_id or "connection")
            elif issue.type == "insufficient_complexity":
                conceptual_gaps.append("complexity")
        
        # Analyze component composition
        if len(build.components) == 0:
            conceptual_gaps.append("basic_assembly")
        elif len(build.components) == 1:
            conceptual_gaps.append("network_depth")
        
        # Check for specific level concepts
        level_concepts = levels_manager.get_level_concepts(level_id)
        component_ids = [comp.get("id", "") for comp in build.components]
        
        for concept in level_concepts:
            if concept == "neural_networks" and not any("neural" in comp_id for comp_id in component_ids):
                conceptual_gaps.append("neural_networks")
            elif concept == "activation" and not any("activation" in comp_id for comp_id in component_ids):
                conceptual_gaps.append("activation")
        
        return HintAnalysis(
            missing_components=missing_components,
            incorrect_connections=incorrect_connections,
            conceptual_gaps=conceptual_gaps,
            attempt_count=attempt_count,
            time_spent=time_spent,
            previous_hints_used=[]  # TODO: Track this in player state
        )
    
    def generate_hint(self, analysis: HintAnalysis, level_id: int, 
                     hint_level: int = 1) -> Optional[Hint]:
        """Generate an appropriate hint based on the analysis"""
        
        # Progressive hint difficulty based on attempts
        difficulty = min(5, max(1, hint_level + (analysis.attempt_count - 1)))
        
        # Prioritize hints based on what's most wrong
        if analysis.missing_components:
            return self._generate_missing_component_hint(analysis.missing_components[0], difficulty)
        
        elif analysis.conceptual_gaps:
            return self._generate_concept_hint(analysis.conceptual_gaps[0], level_id, difficulty)
        
        elif analysis.incorrect_connections:
            return self._generate_connection_hint(analysis.incorrect_connections[0], difficulty)
        
        else:
            return self._generate_encouragement_hint(level_id, difficulty)
    
    def should_offer_assistance(self, attempt_count: int, time_spent: int, 
                               last_score: float = 0.0) -> bool:
        """Determine if the player needs proactive assistance"""
        
        # Offer help after multiple failed attempts
        if attempt_count >= 3:
            return True
        
        # Offer help if player is stuck for a long time
        if time_spent > 300:  # 5 minutes
            return True
        
        # Offer help if score is very low
        if last_score < 0.3 and attempt_count >= 2:
            return True
        
        return False
    
    def get_level_introduction_hints(self, level_id: int) -> List[Hint]:
        """Get introductory hints for a new level"""
        level_config = levels_manager.get_level(level_id)
        if not level_config:
            return []
        
        hints = []
        for hint_text in level_config.hints[:2]:  # First 2 hints as introduction
            hints.append(Hint(
                content=hint_text,
                type="concept",
                difficulty=1
            ))
        
        return hints
    
    def _generate_missing_component_hint(self, component_id: str, difficulty: int) -> Hint:
        """Generate hint for missing component"""
        component_names = {
            "neural_layer": "Neural Layer",
            "activation_relu": "Activation Function", 
            "dense_layer": "Dense Layer",
            "dropout": "Dropout",
            "tensor_add": "Tensor Addition",
            "tensor_multiply": "Tensor Multiplication"
        }
        
        component_name = component_names.get(component_id, component_id.title())
        
        if difficulty <= 2:
            content = f"Your AI might benefit from including a {component_name}."
        elif difficulty <= 4:
            content = f"Try adding a {component_name} component to your network."
        else:
            content = f"You need to add a {component_name} component. Look for it in the component library."
        
        return Hint(
            content=content,
            type="structure",
            difficulty=difficulty,
            visual_highlight=component_id
        )
    
    def _generate_concept_hint(self, concept: str, level_id: int, difficulty: int) -> Hint:
        """Generate hint based on missing concepts"""
        concept_hints = {
            "basic_assembly": [
                "Try dragging a component from the library to get started!",
                "Start by adding some components to build your AI network.",
                "Click and drag components from the left panel into the center area."
            ],
            "network_depth": [
                "Consider adding more components to make your network more sophisticated.",
                "Deeper networks with multiple components often perform better.",
                "Try stacking more layers to give your AI more processing power."
            ],
            "neural_networks": [
                "Every AI needs a brain! Try adding a Neural Layer.",
                "Neural networks need neurons - add a Neural Layer component.",
                "Start with a Neural Layer as the foundation of your AI."
            ],
            "activation": [
                "Your network needs non-linearity - try adding an Activation Function.",
                "Add an Activation Function to help your AI learn complex patterns.",
                "Activation Functions are essential - they help neurons make decisions."
            ]
        }
        
        hints_list = concept_hints.get(concept, [f"Consider the concept of {concept} for this level."])
        hint_index = min(difficulty - 1, len(hints_list) - 1)
        
        return Hint(
            content=hints_list[hint_index],
            type="concept",
            difficulty=difficulty
        )
    
    def _generate_connection_hint(self, connection_issue: str, difficulty: int) -> Hint:
        """Generate hint for connection problems"""
        if difficulty <= 2:
            content = "Check the order of your components - some work better in specific sequences."
        elif difficulty <= 4:
            content = "Try rearranging your components. Activation functions usually come after layers."
        else:
            content = "Components have an optimal order: Layer → Activation → Layer → etc."
        
        return Hint(
            content=content,
            type="structure",
            difficulty=difficulty
        )
    
    def _generate_encouragement_hint(self, level_id: int, difficulty: int) -> Hint:
        """Generate encouraging hint when player is close to success"""
        encouragements = [
            "You're on the right track! Try fine-tuning your approach.",
            "Great progress! Your AI architecture looks promising.",
            "Almost there! Consider if any components could work better together.",
            "Nice work! Your network structure shows good understanding.",
            "Excellent attempt! Small adjustments might give you that extra boost."
        ]
        
        return Hint(
            content=random.choice(encouragements),
            type="encouragement", 
            difficulty=difficulty
        )
    
    def _load_hint_templates(self) -> Dict[str, List[str]]:
        """Load hint templates (could be from config files in future)"""
        return {
            "missing_component": [
                "Your AI needs a {component_name}.",
                "Try adding a {component_name} component.",
                "You're missing a {component_name} - add it from the library."
            ],
            "wrong_order": [
                "Check the order of your components.",
                "Try rearranging your components for better flow.",
                "Component order matters - consider the data flow."
            ]
        }
    
    def _load_concept_hints(self) -> Dict[str, Dict[str, List[str]]]:
        """Load concept-specific hints by level"""
        return {
            "neural_networks": {
                "definition": "Neural networks are systems inspired by biological brains.",
                "usage": "Add a Neural Layer to give your AI processing power.",
                "analogy": "Think of neural layers as the 'brain cells' of your AI."
            },
            "activation": {
                "definition": "Activation functions help AI learn non-linear patterns.",
                "usage": "Place an Activation Function after a Neural Layer.",
                "analogy": "Activations are like switches that help neurons make decisions."
            }
        }

# Global hint system instance
hint_system = AdaptiveHintSystem()