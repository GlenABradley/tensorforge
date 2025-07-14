import torch
import torch.nn as nn
from typing import Dict, List, Any, Callable
from engine import TensorForgeEngine, EducationalLinearLayer, EducationalActivation

class LevelsManager:
    """Manages educational AI levels and progression"""
    
    def __init__(self, engine: TensorForgeEngine):
        self.engine = engine
        self.levels: Dict[int, Dict[str, Any]] = {}
        self.current_level = 1
        self.player_progress = {}
        
        # Initialize all levels
        self._initialize_levels()
        
    def _initialize_levels(self):
        """Initialize all 21 levels with educational content"""
        
        # Level 1: First AI Pet - Shape Recognition
        self.levels[1] = {
            'id': 1,
            'title': 'Train Your First AI Pet',
            'description': 'Draw shapes and watch your AI learn to recognize them!',
            'type': 'interactive_training',
            'objective': 'Train a neural network to classify hand-drawn shapes',
            'concepts': ['neural networks', 'training', 'classification'],
            'components': self._get_level_1_components(),
            'target_accuracy': 0.8,
            'max_epochs': 50,
            'educational_content': {
                'intro': 'Welcome to AI training! You\'re about to create your first artificial intelligence.',
                'concepts_explained': {
                    'neural_network': 'A network of artificial neurons that can learn patterns',
                    'training': 'Teaching the AI by showing it examples',
                    'classification': 'The AI learns to put things into categories'
                }
            }
        }
        
        # Level 2: Tensor Playground
        self.levels[2] = {
            'id': 2,
            'title': 'Tensor Playground',
            'description': 'Learn the building blocks of AI - tensors!',
            'type': 'tensor_operations',
            'objective': 'Master basic tensor operations: addition and multiplication',
            'concepts': ['tensors', 'vector operations', 'element-wise operations'],
            'components': self._get_level_2_components(),
            'inputs': torch.tensor([1.0, 2.0, 3.0]),
            'target': torch.tensor([3.0, 6.0, 9.0]),
            'educational_content': {
                'intro': 'Tensors are like super-powered lists that AI uses to think!',
                'concepts_explained': {
                    'tensor': 'A multi-dimensional array - the basic unit of AI computation',
                    'addition': 'Combining tensors element by element',
                    'multiplication': 'Scaling tensor values for learning'
                }
            }
        }
        
        # Level 3: Pattern Detective
        self.levels[3] = {
            'id': 3,
            'title': 'Pattern Detective',
            'description': 'Build an AI that finds hidden patterns in data',
            'type': 'pattern_recognition',
            'objective': 'Create a simple linear model to find patterns',
            'concepts': ['linear models', 'weights', 'bias'],
            'components': self._get_level_3_components(),
            'educational_content': {
                'intro': 'Every AI is a pattern detective - let\'s teach yours to find clues!',
                'concepts_explained': {
                    'linear_model': 'A simple AI that draws straight lines through data',
                    'weights': 'How much the AI pays attention to each input',
                    'bias': 'The AI\'s starting assumption about the answer'
                }
            }
        }
        
        # Mini-Boss 1: Smart Pet Challenge
        self.levels[4] = {
            'id': 4,
            'title': 'Smart Pet Challenge',
            'description': 'MINI-BOSS: Combine everything to create the ultimate AI pet!',
            'type': 'mini_boss',
            'objective': 'Build a complete AI system using Levels 1-3 knowledge',
            'concepts': ['integration', 'multi-task learning', 'AI systems'],
            'components': self._get_mini_boss_1_components(),
            'challenges': [
                'Recognize 5 different shapes',
                'Process multiple inputs at once',
                'Achieve 90% accuracy'
            ],
            'educational_content': {
                'intro': 'Time for your AI to prove itself! Can it handle multiple challenges?',
                'victory_message': 'Congratulations! Your AI pet is now officially smart!'
            }
        }
        
        # Continue with levels 5-21 (abbreviated for now)
        self._initialize_advanced_levels()
        
    def _get_level_1_components(self) -> List[Dict[str, Any]]:
        """Components available in Level 1"""
        return [
            {
                'id': 'neural_layer',
                'name': 'Neural Layer',
                'description': 'A layer of artificial neurons that can learn',
                'type': 'layer',
                'icon': 'brain',
                'educational_note': 'This is where the magic happens - neurons learn to recognize patterns!'
            },
            {
                'id': 'activation_relu',
                'name': 'ReLU Activation',
                'description': 'Helps the AI learn complex patterns',
                'type': 'activation',
                'icon': 'zap',
                'educational_note': 'ReLU means "turn negative thoughts into zero" - it helps AI focus on positive signals!'
            },
            {
                'id': 'training_loop',
                'name': 'Training Loop',
                'description': 'Teaches the AI by showing it examples repeatedly',
                'type': 'training',
                'icon': 'repeat',
                'educational_note': 'Just like humans, AI gets better with practice!'
            }
        ]
        
    def _get_level_2_components(self) -> List[Dict[str, Any]]:
        """Components available in Level 2"""
        return [
            {
                'id': 'tensor_add',
                'name': 'Tensor Addition',
                'description': 'Add two tensors together',
                'type': 'operation',
                'icon': 'plus',
                'educational_note': 'Addition is how AI combines information from different sources!'
            },
            {
                'id': 'tensor_multiply',
                'name': 'Tensor Multiplication',
                'description': 'Multiply tensors element-wise',
                'type': 'operation', 
                'icon': 'x',
                'educational_note': 'Multiplication is how AI amplifies important signals!'
            },
            {
                'id': 'scalar_multiply',
                'name': 'Scalar Multiply',
                'description': 'Scale a tensor by a number',
                'type': 'operation',
                'icon': 'trending-up',
                'educational_note': 'Scaling helps AI adjust the strength of its responses!'
            }
        ]
        
    def _get_level_3_components(self) -> List[Dict[str, Any]]:
        """Components available in Level 3"""
        return [
            {
                'id': 'linear_layer',
                'name': 'Linear Layer',
                'description': 'The foundation of all neural networks',
                'type': 'layer',
                'icon': 'layers',
                'educational_note': 'Linear layers are like AI\'s way of drawing conclusions from data!'
            },
            {
                'id': 'weight_matrix',
                'name': 'Weight Matrix',
                'description': 'How the AI remembers what it learned',
                'type': 'parameter',
                'icon': 'grid',
                'educational_note': 'Weights are the AI\'s memory - they store everything it learns!'
            },
            {
                'id': 'bias_vector',
                'name': 'Bias Vector',
                'description': 'The AI\'s starting assumptions',
                'type': 'parameter',
                'icon': 'anchor',
                'educational_note': 'Bias helps AI make good guesses even with limited information!'
            }
        ]
        
    def _get_mini_boss_1_components(self) -> List[Dict[str, Any]]:
        """Components available in Mini-Boss 1"""
        # Combine all components from levels 1-3
        components = []
        components.extend(self._get_level_1_components())
        components.extend(self._get_level_2_components())
        components.extend(self._get_level_3_components())
        
        # Add special mini-boss components
        components.extend([
            {
                'id': 'multi_classifier',
                'name': 'Multi-Class Classifier',
                'description': 'Can recognize many different types of things',
                'type': 'advanced_layer',
                'icon': 'layers-2',
                'educational_note': 'This is how AI learns to tell the difference between many things at once!'
            },
            {
                'id': 'confidence_meter',
                'name': 'Confidence Meter',
                'description': 'Shows how sure the AI is about its answer',
                'type': 'evaluation',
                'icon': 'gauge',
                'educational_note': 'Good AI knows when it\'s unsure - just like smart humans!'
            }
        ])
        
        return components
        
    def _initialize_advanced_levels(self):
        """Initialize levels 5-21 with increasing complexity"""
        
        # Levels 5-7: Introduction to Deep Learning
        self.levels[5] = {
            'id': 5,
            'title': 'Deep Learning Architect',
            'description': 'Stack layers to create your first deep neural network',
            'concepts': ['deep networks', 'layer stacking', 'hidden layers']
        }
        
        # Level 8: Mini-Boss 2
        self.levels[8] = {
            'id': 8,
            'title': 'The Backprop Beast',
            'description': 'MINI-BOSS: Master the art of learning from mistakes',
            'type': 'mini_boss',
            'concepts': ['backpropagation', 'gradient descent', 'optimization']
        }
        
        # Continue pattern for all 21 levels...
        # (Implementation can be expanded as needed)
        
    def get_level(self, level_id: int) -> Dict[str, Any]:
        """Get level configuration"""
        return self.levels.get(level_id, {})
        
    def load_level(self, level_id: int) -> bool:
        """Load a level into the engine"""
        level = self.levels.get(level_id)
        if not level:
            return False
            
        # Clear previous level
        self.engine.reset_build()
        
        # Load level components into engine
        self._load_level_components(level_id)
        
        # Set level data
        self.engine.level_data = level
        self.current_level = level_id
        
        return True
        
    def _load_level_components(self, level_id: int):
        """Load level-specific components into the engine"""
        
        # Basic tensor operations (available in most levels)
        self.engine.add_component('tensor_add', torch.add)
        self.engine.add_component('tensor_multiply', torch.multiply)
        self.engine.add_component('scalar_multiply', lambda x, scalar: x * scalar)
        
        # Neural network components
        def create_linear_layer(input_size, output_size):
            return EducationalLinearLayer(input_size, output_size)
            
        def create_activation(activation_type='relu'):
            return EducationalActivation(activation_type)
            
        self.engine.add_component('linear_layer', create_linear_layer)
        self.engine.add_component('activation_relu', lambda x: create_activation('relu')(x))
        self.engine.add_component('activation_sigmoid', lambda x: create_activation('sigmoid')(x))
        
    def get_progress(self) -> Dict[str, Any]:
        """Get player progress information"""
        return {
            'current_level': self.current_level,
            'completed_levels': list(self.player_progress.keys()),
            'total_levels': len(self.levels),
            'mini_bosses_defeated': len([l for l in self.player_progress.values() if l.get('type') == 'mini_boss']),
            'concepts_learned': self._get_concepts_learned()
        }
        
    def _get_concepts_learned(self) -> List[str]:
        """Get list of AI concepts the player has learned"""
        concepts = set()
        for level_id in self.player_progress.keys():
            level = self.levels.get(level_id, {})
            concepts.update(level.get('concepts', []))
        return sorted(list(concepts))
        
    def mark_level_complete(self, level_id: int, score: float, time_taken: int):
        """Mark a level as completed"""
        self.player_progress[level_id] = {
            'completed': True,
            'score': score,
            'time_taken': time_taken,
            'type': self.levels[level_id].get('type', 'normal')
        }

# Testing
if __name__ == "__main__":
    from engine import TensorForgeEngine
    
    engine = TensorForgeEngine()
    manager = LevelsManager(engine)
    
    # Test Level 2 setup
    success = manager.load_level(2)
    print(f"Level 2 loaded: {success}")
    
    if success:
        level_info = manager.get_level(2)
        print(f"Level 2: {level_info['title']}")
        print(f"Objective: {level_info['objective']}")
        
        # Test tensor operations
        engine.append_to_build('tensor_add', torch.tensor([1.0, 2.0, 3.0]))
        engine.append_to_build('scalar_multiply', 2.0)
        
        result = engine.build_and_simulate(level_info['inputs'])
        success = engine.check_win(result, level_info['target'])
        
        print(f"Simulation result: {result}")
        print(f"Target: {level_info['target']}")
        print(f"Success: {success}")