"""
Enhanced Simulation Engine
Provides computation graph execution and educational simulations.
"""
from typing import Dict, List, Any, Optional, Tuple
import torch
import torch.nn as nn
import numpy as np
from dataclasses import dataclass
from models.game_models import ComponentBuild, SimulationResult, ValidationResult, ValidationIssue
from core.components.registry import component_registry

@dataclass
class ComponentNode:
    """Represents a component in the computation graph"""
    id: str
    component_id: str
    inputs: List[str] = None
    outputs: List[str] = None
    parameters: Dict[str, Any] = None
    
    def __post_init__(self):
        if self.inputs is None:
            self.inputs = []
        if self.outputs is None:
            self.outputs = []
        if self.parameters is None:
            self.parameters = {}

class ComputationGraph:
    """Executes a sequence of AI components"""
    
    def __init__(self):
        self.nodes: List[ComponentNode] = []
        self.execution_order: List[str] = []
        self.intermediate_results: Dict[str, torch.Tensor] = {}
    
    def add_component(self, component_id: str, node_id: str, parameters: Dict[str, Any] = None) -> str:
        """Add a component to the computation graph"""
        node = ComponentNode(
            id=node_id,
            component_id=component_id,
            parameters=parameters or {}
        )
        self.nodes.append(node)
        self.execution_order.append(node_id)
        return node_id
    
    def execute(self, input_data: torch.Tensor) -> Dict[str, torch.Tensor]:
        """Execute the computation graph"""
        self.intermediate_results = {"input": input_data}
        current_data = input_data
        
        for node_id in self.execution_order:
            node = self._get_node(node_id)
            if not node:
                continue
            
            # Get component implementation
            implementation = component_registry.get_implementation(node.component_id)
            if not implementation:
                raise ValueError(f"No implementation found for component: {node.component_id}")
            
            # Execute component
            try:
                # Ensure parameters is a proper dict
                params = node.parameters if isinstance(node.parameters, dict) else {}
                current_data = implementation(current_data, **params)
                self.intermediate_results[node_id] = current_data
            except Exception as e:
                raise RuntimeError(f"Error executing component {node.component_id}: {str(e)}")
        
        return self.intermediate_results
    
    def _get_node(self, node_id: str) -> Optional[ComponentNode]:
        """Get node by ID"""
        for node in self.nodes:
            if node.id == node_id:
                return node
        return None
    
    def clear(self):
        """Clear the computation graph"""
        self.nodes = []
        self.execution_order = []
        self.intermediate_results = {}

class TensorForgeSimulationEngine:
    """Enhanced simulation engine for educational AI"""
    
    def __init__(self):
        self.computation_graph = ComputationGraph()
        self.validation_rules = self._load_validation_rules()
    
    def validate_build(self, build: ComponentBuild, level_id: int) -> ValidationResult:
        """Validate a component build for correctness"""
        issues = []
        
        # Check minimum component requirements
        if len(build.components) == 0:
            issues.append(ValidationIssue(
                type="missing_components",
                component_id=None,
                message="No components added to the network",
                severity="error",
                hint="Try adding some components from the library!"
            ))
            return ValidationResult(False, issues)
        
        # Check for required component types based on level
        required_components = self._get_required_components(level_id)
        component_ids = []
        
        for comp in build.components:
            if isinstance(comp, dict):
                comp_id = comp.get("id", comp.get("name", ""))
            else:
                comp_id = getattr(comp, 'id', "")
            component_ids.append(comp_id.lower())
        
        for required in required_components:
            if not any(required.lower() in comp_id for comp_id in component_ids):
                issues.append(ValidationIssue(
                    type="missing_required_component",
                    component_id=required,
                    message=f"Missing required component: {required}",
                    severity="error", 
                    hint=f"Try adding a {required} component to your network"
                ))
        
        # Check component order and compatibility
        self._validate_component_sequence(build.components, issues)
        
        # Level-specific validation
        self._validate_level_specific_requirements(build, level_id, issues)
        
        is_valid = not any(issue.severity == "error" for issue in issues)
        suggestions = [issue.hint for issue in issues if issue.hint and issue.severity != "error"]
        
        return ValidationResult(is_valid, issues, suggestions)
    
    def simulate_build(self, build: ComponentBuild, level_id: int, input_data: Optional[torch.Tensor] = None) -> SimulationResult:
        """Simulate a component build and return results"""
        
        # First validate the build
        validation_result = self.validate_build(build, level_id)
        if not validation_result.is_valid:
            error_messages = [issue.message for issue in validation_result.issues if issue.severity == "error"]
            return SimulationResult(
                success=False,
                score=0.0,
                message="; ".join(error_messages),
                validation_result=validation_result
            )
        
        try:
            # Clear previous computation graph
            self.computation_graph.clear()
            
            # Build computation graph from components
            for i, component in enumerate(build.components):
                # Handle component as dict or object
                if isinstance(component, dict):
                    comp_id = component.get("id", component.get("name", f"component_{i}"))
                    parameters = component.get("parameters", {})
                else:
                    comp_id = getattr(component, 'id', f"component_{i}")
                    parameters = getattr(component, 'parameters', {})
                
                node_id = f"node_{i}"
                self.computation_graph.add_component(comp_id, node_id, parameters)
            
            # Generate or use provided input data
            if input_data is None:
                input_data = self._generate_input_data(level_id)
            
            # Execute the computation graph
            results = self.computation_graph.execute(input_data)
            
            # Evaluate results based on level criteria
            success, score, message, visual_data = self._evaluate_results(results, level_id, build)
            
            # Generate educational feedback
            educational_feedback = self._generate_educational_feedback(build, results, level_id)
            
            return SimulationResult(
                success=success,
                score=score,
                message=message,
                visual_data=visual_data,
                validation_result=validation_result,
                educational_feedback=educational_feedback
            )
            
        except Exception as e:
            return SimulationResult(
                success=False,
                score=0.0,
                message=f"Simulation failed: {str(e)}",
                validation_result=validation_result
            )
    
    def _get_required_components(self, level_id: int) -> List[str]:
        """Get required components for a level"""
        requirements = {
            1: ["neural_layer"],
            2: ["neural_layer", "activation"],
            3: ["neural_layer", "tensor_add", "tensor_multiply"],
            4: ["neural_layer", "activation", "dense_layer"]
        }
        return requirements.get(level_id, [])
    
    def _validate_component_sequence(self, components: List[Dict], issues: List[ValidationIssue]):
        """Validate that components are in a reasonable sequence"""
        if not components:
            return
        
        # Check for activation after layers
        has_layer = False
        for i, comp in enumerate(components):
            if isinstance(comp, dict):
                comp_type = comp.get("type", "")
                comp_id = comp.get("id", comp.get("name", ""))
            else:
                comp_type = getattr(comp, 'type', "")
                comp_id = getattr(comp, 'id', "")
            
            if "layer" in comp_id.lower() or comp_type == "layer":
                has_layer = True
            elif "activation" in comp_id.lower() and not has_layer:
                issues.append(ValidationIssue(
                    type="sequence_error",
                    component_id=comp_id,
                    message="Activation function should come after a layer",
                    severity="warning",
                    hint="Try placing the activation function after a neural layer"
                ))
    
    def _validate_level_specific_requirements(self, build: ComponentBuild, level_id: int, issues: List[ValidationIssue]):
        """Validate level-specific requirements"""
        if level_id == 2:
            # Level 2 requires at least 3 components for complexity
            if len(build.components) < 3:
                issues.append(ValidationIssue(
                    type="insufficient_complexity",
                    component_id=None,
                    message=f"Need at least 3 components, you have {len(build.components)}",
                    severity="warning",
                    hint="Add more components to make your network more sophisticated"
                ))
        
        elif level_id == 4:
            # Mini-boss level requires higher complexity
            if len(build.components) < 4:
                issues.append(ValidationIssue(
                    type="insufficient_complexity",
                    component_id=None,
                    message="Mini-boss level requires at least 4 components for full credit",
                    severity="warning"
                ))
    
    def _generate_input_data(self, level_id: int) -> torch.Tensor:
        """Generate appropriate input data for a level"""
        if level_id == 2:
            return torch.tensor([1.0, 2.0, 3.0, 4.0])
        elif level_id == 3:
            return torch.tensor([0.5, 1.5, 2.5])
        else:
            return torch.tensor([1.0, 0.5, 0.8, 0.3])
    
    def _evaluate_results(self, results: Dict[str, torch.Tensor], level_id: int, build: ComponentBuild) -> Tuple[bool, float, str, Dict]:
        """Evaluate simulation results against level criteria"""
        final_output = list(results.values())[-1] if results else None
        
        if final_output is None:
            return False, 0.0, "No output generated", {}
        
        # Level-specific evaluation
        if level_id == 2:
            return self._evaluate_level_2(results, build)
        elif level_id == 3:
            return self._evaluate_level_3(results, build)
        elif level_id == 4:
            return self._evaluate_mini_boss_1(results, build)
        else:
            return self._evaluate_generic(results, build)
    
    def _evaluate_level_2(self, results: Dict[str, torch.Tensor], build: ComponentBuild) -> Tuple[bool, float, str, Dict]:
        """Evaluate Level 2 - Network Building"""
        score = 0.6  # Base score
        
        # Check component diversity
        component_types = set()
        for comp in build.components:
            comp_id = comp.get("id", comp.get("name", ""))
            if "neural" in comp_id.lower():
                component_types.add("neural")
            elif "dense" in comp_id.lower():
                component_types.add("dense")  
            elif "activation" in comp_id.lower():
                component_types.add("activation")
            elif "dropout" in comp_id.lower():
                component_types.add("dropout")
        
        # Scoring bonuses
        if "neural" in component_types:
            score += 0.15
        if "activation" in component_types:
            score += 0.1
        if "dense" in component_types:
            score += 0.1
        if len(component_types) >= 3:
            score += 0.05
        
        score = min(0.95, score)
        success = score >= 0.85
        
        if success:
            message = f"Excellent network! Your {len(build.components)}-layer network achieved {score:.1%} efficiency."
        else:
            missing = []
            if "neural" not in component_types:
                missing.append("Neural Layer")
            if "activation" not in component_types:
                missing.append("Activation Function") 
            message = f"Network needs improvement. Consider adding: {', '.join(missing)}. Current efficiency: {score:.1%}"
        
        visual_data = {
            "efficiency": score,
            "component_breakdown": dict(component_types),
            "network_depth": len(build.components)
        }
        
        return success, score, message, visual_data
    
    def _evaluate_level_3(self, results: Dict[str, torch.Tensor], build: ComponentBuild) -> Tuple[bool, float, str, Dict]:
        """Evaluate Level 3 - Pattern Detection"""
        # Simple pattern detection evaluation
        score = 0.75 if len(build.components) >= 3 else 0.5
        success = score >= 0.75
        
        message = "Pattern detection network built successfully!" if success else "Try adding more components for better pattern recognition."
        
        return success, score, message, {"pattern_score": score}
    
    def _evaluate_mini_boss_1(self, results: Dict[str, torch.Tensor], build: ComponentBuild) -> Tuple[bool, float, str, Dict]:
        """Evaluate Mini-Boss 1 - Smart Pet Challenge"""
        base_score = 0.7
        
        # Higher standards for mini-boss
        if len(build.components) >= 4:
            base_score += 0.1
        if len(build.components) >= 5:
            base_score += 0.05
        
        # Check for advanced components
        has_dropout = any("dropout" in comp.get("id", "").lower() for comp in build.components)
        has_dense = any("dense" in comp.get("id", "").lower() for comp in build.components)
        
        if has_dropout:
            base_score += 0.08
        if has_dense:
            base_score += 0.07
        
        score = min(0.95, base_score)
        success = score >= 0.9
        
        message = "Mini-boss conquered! Your AI is truly intelligent!" if success else f"Good attempt! Score: {score:.1%}. Try adding more advanced components."
        
        return success, score, message, {"mini_boss_score": score}
    
    def _evaluate_generic(self, results: Dict[str, torch.Tensor], build: ComponentBuild) -> Tuple[bool, float, str, Dict]:
        """Generic evaluation for other levels"""
        score = min(0.9, 0.6 + len(build.components) * 0.1)
        success = score >= 0.8
        message = "Network simulation completed successfully!" if success else "Try improving your network architecture."
        
        return success, score, message, {"generic_score": score}
    
    def _generate_educational_feedback(self, build: ComponentBuild, results: Dict, level_id: int) -> List[str]:
        """Generate educational feedback based on the build"""
        feedback = []
        
        # Component-specific feedback
        component_count = len(build.components)
        if component_count == 1:
            feedback.append("Great start! Single components are the building blocks of AI.")
        elif component_count <= 3:
            feedback.append("Nice architecture! Multiple components allow for more sophisticated processing.")
        else:
            feedback.append("Impressive network depth! Deep networks can learn complex patterns.")
        
        # Level-specific educational notes
        if level_id == 2:
            feedback.append("Remember: each layer transforms the data, making it easier for the next layer to understand.")
        elif level_id == 3:
            feedback.append("Pattern recognition is at the heart of all AI - your network is learning to find hidden relationships!")
        
        return feedback
    
    def _load_validation_rules(self) -> Dict[str, Any]:
        """Load validation rules (placeholder for future config-driven validation)"""
        return {}

# Global simulation engine instance
simulation_engine = TensorForgeSimulationEngine()