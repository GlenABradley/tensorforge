import torch
import torch.nn as nn
import numpy as np
from typing import Dict, List, Any, Callable, Optional

class TensorForgeEngine:
    """Enhanced engine for educational AI simulations"""
    
    def __init__(self):
        self.components: Dict[str, Callable] = {}
        self.player_build: List[Callable] = []
        self.level_data: Dict[str, Any] = {}
        self.training_history: List[Dict[str, float]] = []
        
    def add_component(self, op_name: str, op_func: Callable):
        """Add a component operation to the engine"""
        self.components[op_name] = op_func
        
    def append_to_build(self, op_name: str, *args, **kwargs):
        """Add an operation to the player's build pipeline"""
        if op_name not in self.components:
            raise ValueError(f"Component '{op_name}' not available")
            
        def op_func(x):
            return self.components[op_name](x, *args, **kwargs)
        
        self.player_build.append(op_func)
        
    def build_and_simulate(self, inputs: torch.Tensor) -> torch.Tensor:
        """Execute the player's build pipeline"""
        result = inputs
        for op in self.player_build:
            result = op(result)
        return result
        
    def check_win(self, result: torch.Tensor, target: torch.Tensor, tolerance: float = 1e-3) -> bool:
        """Check if simulation result matches target within tolerance"""
        if result.shape != target.shape:
            return False
        loss = nn.MSELoss()(result.float(), target.float())
        return loss.item() < tolerance
        
    def reset_build(self):
        """Clear the current build pipeline"""
        self.player_build = []
        self.training_history = []
        
    def get_component_info(self, op_name: str) -> Dict[str, Any]:
        """Get information about a component"""
        component_info = {
            'tensor_add': {
                'name': 'Tensor Addition',
                'description': 'Adds two tensors element-wise',
                'inputs': ['tensor1', 'tensor2'],
                'category': 'basic_ops'
            },
            'tensor_multiply': {
                'name': 'Tensor Multiplication', 
                'description': 'Multiplies two tensors element-wise',
                'inputs': ['tensor1', 'tensor2'],
                'category': 'basic_ops'
            },
            'linear_layer': {
                'name': 'Linear Layer',
                'description': 'Fully connected neural network layer',
                'inputs': ['input_size', 'output_size'],
                'category': 'neural_layers'
            },
            'activation_relu': {
                'name': 'ReLU Activation',
                'description': 'Rectified Linear Unit activation function',
                'inputs': ['tensor'],
                'category': 'activations'
            },
            'activation_sigmoid': {
                'name': 'Sigmoid Activation',
                'description': 'Sigmoid activation function (0 to 1)',
                'inputs': ['tensor'],
                'category': 'activations'
            }
        }
        return component_info.get(op_name, {'name': op_name, 'description': 'Unknown component'})

# Educational neural network components
class EducationalLinearLayer(nn.Module):
    """A linear layer with educational visualization"""
    
    def __init__(self, input_size: int, output_size: int):
        super().__init__()
        self.linear = nn.Linear(input_size, output_size)
        self.input_size = input_size
        self.output_size = output_size
        
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.linear(x)
        
    def get_weights_info(self) -> Dict[str, Any]:
        """Get weight information for visualization"""
        return {
            'weights': self.linear.weight.data.tolist(),
            'bias': self.linear.bias.data.tolist(),
            'input_size': self.input_size,
            'output_size': self.output_size
        }

class EducationalActivation(nn.Module):
    """Activation functions with educational visualization"""
    
    def __init__(self, activation_type: str = 'relu'):
        super().__init__()
        self.activation_type = activation_type
        
        if activation_type == 'relu':
            self.activation = nn.ReLU()
        elif activation_type == 'sigmoid':
            self.activation = nn.Sigmoid()
        elif activation_type == 'tanh':
            self.activation = nn.Tanh()
        else:
            raise ValueError(f"Unknown activation type: {activation_type}")
            
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return self.activation(x)
        
    def get_activation_info(self) -> Dict[str, Any]:
        """Get activation function information"""
        return {
            'type': self.activation_type,
            'description': self._get_description()
        }
        
    def _get_description(self) -> str:
        descriptions = {
            'relu': 'Outputs max(0, x) - kills negative values',
            'sigmoid': 'Squashes values between 0 and 1',
            'tanh': 'Squashes values between -1 and 1'
        }
        return descriptions.get(self.activation_type, 'Unknown activation')

# Example usage and testing
if __name__ == "__main__":
    engine = TensorForgeEngine()
    
    # Test basic tensor operations
    def tensor_add(x, y):
        return torch.add(x, y)
    
    def tensor_multiply(x, y):
        return torch.multiply(x, y)
    
    engine.add_component('add', tensor_add)
    engine.add_component('multiply', tensor_multiply)
    
    # Test Level 1 simulation
    inputs = torch.tensor([1.0, 2.0, 3.0])
    target = torch.tensor([2.0, 3.0, 4.0])
    
    engine.append_to_build('add', torch.tensor([1.0, 1.0, 1.0]))
    result = engine.build_and_simulate(inputs)
    
    success = engine.check_win(result, target)
    print(f"Level 1 Test - Success: {success}")
    print(f"Result: {result}")
    print(f"Target: {target}")