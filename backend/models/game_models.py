"""
Tensor Forge Game Models
Comprehensive data models for the game system.
"""
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional, Callable, Union
from enum import Enum
import torch

class ComponentType(Enum):
    LAYER = "layer"
    ACTIVATION = "activation"  
    OPERATION = "operation"
    TRAINING = "training"
    REGULARIZATION = "regularization"
    ATTENTION = "attention"
    EMBEDDING = "embedding"
    OUTPUT = "output"

class GamePhase(Enum):
    BUILDING = "building"
    TRAINING = "training"
    COMPLETE = "complete"

class MasteryLevel(Enum):
    NOVICE = "novice"
    LEARNING = "learning" 
    PROFICIENT = "proficient"
    EXPERT = "expert"

@dataclass
class TensorSpec:
    """Specification for tensor input/output requirements"""
    name: str
    shape: List[int]
    dtype: str = "float32"
    description: str = ""

@dataclass
class Component:
    """Enhanced component definition with full metadata"""
    id: str
    name: str
    description: str
    type: ComponentType
    icon: str
    educational_note: str = ""
    input_specs: List[TensorSpec] = field(default_factory=list)
    output_specs: List[TensorSpec] = field(default_factory=list)
    parameters: Dict[str, Any] = field(default_factory=dict)
    level_introduced: int = 1
    prerequisites: List[str] = field(default_factory=list)

@dataclass
class ComponentBuild:
    """Represents a player's component assembly"""
    components: List[Dict[str, Any]]
    connections: List[Dict[str, Any]] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class ValidationIssue:
    """Represents a validation problem with a build"""
    type: str
    component_id: Optional[str]
    message: str
    severity: str  # "error", "warning", "info"
    hint: Optional[str] = None

@dataclass 
class ValidationResult:
    """Result of build validation"""
    is_valid: bool
    issues: List[ValidationIssue]
    suggestions: List[str] = field(default_factory=list)

@dataclass
class SimulationResult:
    """Enhanced simulation result with detailed feedback"""
    success: bool
    score: float
    message: str
    visual_data: Optional[Dict[str, Any]] = None
    validation_result: Optional[ValidationResult] = None
    educational_feedback: List[str] = field(default_factory=list)
    concept_progress: Dict[str, float] = field(default_factory=dict)

@dataclass
class LevelConfig:
    """Complete level configuration"""
    id: int
    title: str
    description: str
    objective: str
    concepts: List[str]
    available_components: List[str]  # Component IDs
    success_criteria: Dict[str, Any]
    hints: List[str] = field(default_factory=list)
    educational_content: Dict[str, Any] = field(default_factory=dict)
    type: str = "standard"  # "standard", "mini_boss", "final_boss"
    prerequisites: List[int] = field(default_factory=list)
    max_attempts: Optional[int] = None
    time_limit: Optional[int] = None

@dataclass
class PlayerProgress:
    """Comprehensive player progress tracking"""
    player_id: str
    completed_levels: Dict[int, Dict[str, Any]] = field(default_factory=dict)
    current_level: int = 1
    concept_mastery: Dict[str, MasteryLevel] = field(default_factory=dict)
    total_playtime: int = 0
    achievements: List[str] = field(default_factory=list)
    preferences: Dict[str, Any] = field(default_factory=dict)

@dataclass
class Hint:
    """Intelligent hint with context"""
    content: str
    type: str  # "concept", "structure", "debug", "encouragement"
    difficulty: int  # 1-5, where 1 is gentle nudge, 5 is direct answer
    prerequisites: List[str] = field(default_factory=list)
    visual_highlight: Optional[str] = None  # Component or area to highlight

@dataclass
class HintAnalysis:
    """Analysis of player's current situation for hint generation"""
    missing_components: List[str]
    incorrect_connections: List[str] 
    conceptual_gaps: List[str]
    attempt_count: int
    time_spent: int
    previous_hints_used: List[str]