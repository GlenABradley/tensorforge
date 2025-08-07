"""
Component Registry System
Manages all available components and their implementations.
"""
from typing import Dict, List, Optional, Callable, Any
import torch
import torch.nn as nn
from models.game_models import Component, ComponentType, TensorSpec
from collections import defaultdict

class ComponentRegistry:
    """Central registry for all game components"""
    
    def __init__(self):
        self.components: Dict[str, Component] = {}
        self.implementations: Dict[str, Callable] = {}
        self.level_components: Dict[int, List[str]] = defaultdict(list)
        self._register_core_components()
    
    def register_component(self, component: Component, implementation: Callable):
        """Register a new component with its implementation"""
        self.components[component.id] = component
        self.implementations[component.id] = implementation
        
        # Auto-register to appropriate level
        if component.level_introduced:
            self.level_components[component.level_introduced].append(component.id)
    
    def get_component(self, component_id: str) -> Optional[Component]:
        """Get component definition by ID"""
        return self.components.get(component_id)
    
    def get_implementation(self, component_id: str) -> Optional[Callable]:
        """Get component implementation by ID"""
        return self.implementations.get(component_id)
    
    def get_components_for_level(self, level_id: int) -> List[Component]:
        """Get all components available for a specific level"""
        available_components = []
        
        # Get all components up to and including this level
        for level in range(1, level_id + 1):
            for comp_id in self.level_components[level]:
                if comp_id in self.components:
                    available_components.append(self.components[comp_id])
        
        return available_components
    
    def get_components_by_type(self, component_type: ComponentType) -> List[Component]:
        """Get all components of a specific type"""
        return [comp for comp in self.components.values() 
                if comp.type == component_type]
    
    def validate_component_compatibility(self, comp1_id: str, comp2_id: str) -> bool:
        """Check if two components can be connected"""
        comp1 = self.get_component(comp1_id)
        comp2 = self.get_component(comp2_id)
        
        if not comp1 or not comp2:
            return False
        
        # Simple validation: check if output specs of comp1 match input specs of comp2
        if comp1.output_specs and comp2.input_specs:
            # This is simplified - in reality would need more sophisticated matching
            return len(comp1.output_specs) > 0 and len(comp2.input_specs) > 0
        
        return True
    
    def _register_core_components(self):
        """Register the core components for Tensor Forge"""
        
        # Level 1 Components - Basic Neural Network
        neural_layer = Component(
            id="neural_layer",
            name="Neural Layer", 
            description="A layer of artificial neurons that can learn",
            type=ComponentType.LAYER,
            icon="brain",
            educational_note="This is where the magic happens - neurons learn to recognize patterns!",
            input_specs=[TensorSpec("input", [-1, -1], description="Input features")],
            output_specs=[TensorSpec("output", [-1, -1], description="Transformed features")],
            level_introduced=1
        )
        
        activation_relu = Component(
            id="activation_relu",
            name="ReLU Activation",
            description="Helps the AI learn complex patterns by adding non-linearity",
            type=ComponentType.ACTIVATION,
            icon="zap", 
            educational_note="ReLU means 'turn negative thoughts into zero' - it helps AI focus on positive signals!",
            input_specs=[TensorSpec("input", [-1, -1], description="Any tensor")],
            output_specs=[TensorSpec("output", [-1, -1], description="ReLU activated tensor")],
            level_introduced=1
        )
        
        # Level 2 Components - Tensor Operations
        tensor_add = Component(
            id="tensor_add",
            name="Tensor Addition",
            description="Add two tensors element-wise",
            type=ComponentType.OPERATION,
            icon="plus",
            educational_note="Addition is how AI combines information from different sources!",
            input_specs=[
                TensorSpec("tensor1", [-1], description="First tensor"),
                TensorSpec("tensor2", [-1], description="Second tensor")
            ],
            output_specs=[TensorSpec("result", [-1], description="Sum of tensors")],
            level_introduced=2
        )
        
        tensor_multiply = Component(
            id="tensor_multiply", 
            name="Tensor Multiplication",
            description="Multiply tensors element-wise",
            type=ComponentType.OPERATION,
            icon="x",
            educational_note="Multiplication is how AI amplifies important signals!",
            input_specs=[
                TensorSpec("tensor1", [-1], description="First tensor"),
                TensorSpec("tensor2", [-1], description="Second tensor") 
            ],
            output_specs=[TensorSpec("result", [-1], description="Product of tensors")],
            level_introduced=2
        )
        
        # Level 3+ Components - Advanced Layers
        dense_layer = Component(
            id="dense_layer",
            name="Dense Layer",
            description="A fully connected layer for deeper learning",
            type=ComponentType.LAYER,
            icon="layers",
            educational_note="Dense layers are like AI's way of finding complex relationships in data!",
            input_specs=[TensorSpec("input", [-1, -1], description="Input features")],
            output_specs=[TensorSpec("output", [-1, -1], description="Dense layer output")],
            level_introduced=2
        )
        
        dropout = Component(
            id="dropout",
            name="Dropout",
            description="Prevents overfitting by randomly ignoring neurons",
            type=ComponentType.REGULARIZATION,
            icon="lightbulb",
            educational_note="Dropout is like teaching your AI to not rely too heavily on any single piece of information!",
            input_specs=[TensorSpec("input", [-1, -1], description="Input features")],
            output_specs=[TensorSpec("output", [-1, -1], description="Regularized output")],
            level_introduced=2
        )
        
        # Register implementations
        self.register_component(neural_layer, self._neural_layer_impl)
        self.register_component(activation_relu, self._relu_activation_impl)
        self.register_component(tensor_add, self._tensor_add_impl)
        self.register_component(tensor_multiply, self._tensor_multiply_impl)
        self.register_component(dense_layer, self._dense_layer_impl)
        self.register_component(dropout, self._dropout_impl)
    
    # Implementation functions for core components
    def _neural_layer_impl(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        """Simple neural layer implementation"""
        # For educational purposes, create a small linear transformation
        input_size = x.shape[-1] if len(x.shape) > 1 else x.shape[0]
        output_size = kwargs.get('output_size', max(2, input_size // 2))
        
        layer = nn.Linear(input_size, output_size)
        return layer(x.float())
    
    def _relu_activation_impl(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        """ReLU activation implementation"""
        return torch.relu(x)
    
    def _tensor_add_impl(self, x: torch.Tensor, y: torch.Tensor, **kwargs) -> torch.Tensor:
        """Tensor addition implementation"""
        return torch.add(x, y)
    
    def _tensor_multiply_impl(self, x: torch.Tensor, y: torch.Tensor, **kwargs) -> torch.Tensor:
        """Tensor multiplication implementation"""
        return torch.multiply(x, y)
    
    def _dense_layer_impl(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        """Dense layer implementation"""
        input_size = x.shape[-1] if len(x.shape) > 1 else x.shape[0]
        output_size = kwargs.get('output_size', max(2, input_size // 2))
        
        layer = nn.Linear(input_size, output_size)
        return layer(x.float())
    
    def _dropout_impl(self, x: torch.Tensor, **kwargs) -> torch.Tensor:
        """Dropout implementation"""
        dropout_rate = kwargs.get('dropout_rate', 0.2)
        dropout = nn.Dropout(dropout_rate)
        return dropout(x)

# Global component registry instance
component_registry = ComponentRegistry()