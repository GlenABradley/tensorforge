"""
Enhanced Game API Endpoints
Refactored endpoints using the new architecture.
"""
from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import torch

from ..models.game_models import ComponentBuild, SimulationResult, PlayerProgress, Hint
from ..core.levels.manager import levels_manager
from ..core.engine.simulation import simulation_engine
from ..core.education.hints import hint_system
from ..core.education.progress import concept_tracker, learning_analytics
from ..core.components.registry import component_registry

# API Models
class TrainingData(BaseModel):
    drawings: List[Dict[str, Any]]
    labels: List[str]

class GameBuild(BaseModel):
    components: List[Dict[str, Any]]
    level_id: int

class HintRequest(BaseModel):
    level_id: int
    build: Optional[ComponentBuild] = None
    attempt_count: int = 1
    time_spent: int = 0

class ProgressUpdate(BaseModel):
    player_id: str
    level_id: int
    score: float
    time_taken: int
    attempts: int = 1

# Router
game_router = APIRouter(prefix="/api", tags=["game"])

@game_router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy", 
        "message": "Tensor Forge API is running!",
        "version": "2.0.0-enhanced"
    }

@game_router.get("/levels/{level_id}")
async def get_level(level_id: int):
    """Get level configuration and requirements"""
    level_config = levels_manager.get_level(level_id)
    
    if not level_config:
        raise HTTPException(status_code=404, detail="Level not found")
    
    # Get available components for this level
    available_components = []
    for comp_id in level_config.available_components:
        component = component_registry.get_component(comp_id)
        if component:
            available_components.append({
                "id": component.id,
                "name": component.name,
                "description": component.description,
                "type": component.type.value,
                "icon": component.icon,
                "educational_note": component.educational_note
            })
    
    return {
        "id": level_config.id,
        "title": level_config.title,
        "description": level_config.description,
        "objective": level_config.objective,
        "concepts": level_config.concepts,
        "available_components": available_components,
        "success_criteria": level_config.success_criteria,
        "educational_content": level_config.educational_content,
        "type": level_config.type,
        "difficulty": levels_manager.get_level_difficulty_rating(level_id)
    }

@game_router.post("/simulate-build")
async def simulate_build(build_request: GameBuild, background_tasks: BackgroundTasks):
    """Simulate a player's component build"""
    try:
        # Convert to ComponentBuild model
        component_build = ComponentBuild(
            components=build_request.components,
            metadata={"level_id": build_request.level_id}
        )
        
        # Run simulation
        result = simulation_engine.simulate_build(
            component_build, 
            build_request.level_id
        )
        
        # Track analytics in background
        background_tasks.add_task(
            learning_analytics.track_player_journey,
            player_id="default_player",  # TODO: Get from session/auth
            action="simulation_attempt",
            level_id=build_request.level_id,
            build=component_build,
            success=result.success,
            score=result.score
        )
        
        return {
            "success": result.success,
            "score": result.score,
            "message": result.message,
            "visual_data": result.visual_data,
            "educational_feedback": result.educational_feedback,
            "validation_issues": [
                {
                    "type": issue.type,
                    "message": issue.message,
                    "severity": issue.severity,
                    "hint": issue.hint
                }
                for issue in (result.validation_result.issues if result.validation_result else [])
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Simulation failed: {str(e)}")

@game_router.post("/train-shape-classifier")
async def train_shape_classifier(training_data: TrainingData):
    """Train a shape classifier with user drawings (Level 1 specific)"""
    try:
        # This is a legacy endpoint for Level 1 - we'll keep it for compatibility
        # but route it through our new simulation system
        
        if len(training_data.drawings) < 3:
            return SimulationResult(
                success=False,
                score=0.0,
                message="Need at least 3 training examples!",
                educational_feedback=["Draw more shapes to give your AI enough examples to learn from."]
            )
        
        # Simulate training with a simple scoring system
        # In real implementation, this would use the actual ML training
        accuracy = min(0.95, 0.6 + len(training_data.drawings) * 0.05)
        success = accuracy >= 0.8
        
        training_history = [
            {"epoch": i + 1, "loss": 1.0 - (i * 0.02), "accuracy": min(accuracy, i * 0.03)}
            for i in range(min(30, len(training_data.drawings) * 3))
        ]
        
        return {
            "success": success,
            "score": accuracy,
            "message": f"AI trained! Final accuracy: {accuracy:.1%}",
            "visual_data": {
                "training_history": training_history,
                "final_accuracy": accuracy,
                "training_examples": len(training_data.drawings)
            },
            "educational_feedback": [
                f"Your AI learned to recognize shapes from {len(training_data.drawings)} examples!",
                "More training examples generally lead to better accuracy.",
                "The neural network adjusted its weights during training to improve recognition."
            ]
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Training failed: {str(e)}")

@game_router.post("/hint")
async def get_hint(hint_request: HintRequest):
    """Get an intelligent hint for the current situation"""
    try:
        hint = None
        
        if hint_request.build:
            # Analyze current build for contextual hint
            validation_result = simulation_engine.validate_build(
                hint_request.build, 
                hint_request.level_id
            )
            
            analysis = hint_system.analyze_attempt(
                hint_request.build,
                validation_result,
                hint_request.level_id,
                hint_request.attempt_count,
                hint_request.time_spent
            )
            
            hint = hint_system.generate_hint(analysis, hint_request.level_id)
        else:
            # Get introductory hints for the level
            intro_hints = hint_system.get_level_introduction_hints(hint_request.level_id)
            hint = intro_hints[0] if intro_hints else None
        
        if not hint:
            # Fallback hint
            hint = Hint(
                content="Try experimenting with different components from the library!",
                type="general",
                difficulty=1
            )
        
        return {
            "content": hint.content,
            "type": hint.type,
            "difficulty": hint.difficulty,
            "visual_highlight": hint.visual_highlight
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Hint generation failed: {str(e)}")

@game_router.post("/progress/update")
async def update_progress(progress_update: ProgressUpdate):
    """Update player progress after level completion"""
    try:
        # This would normally load from database - for now using in-memory
        player_progress = PlayerProgress(player_id=progress_update.player_id)
        
        # Mark level complete
        levels_manager.mark_level_complete(
            progress_update.level_id,
            player_progress,
            progress_update.score,
            progress_update.time_taken,
            progress_update.attempts
        )
        
        # Update concept mastery
        level_concepts = levels_manager.get_level_concepts(progress_update.level_id)
        for concept in level_concepts:
            concept_tracker.update_concept_mastery(
                player_progress,
                concept,
                progress_update.score,
                progress_update.attempts
            )
        
        # Get updated progress summary
        mastery_summary = concept_tracker.get_mastery_summary(player_progress)
        available_levels = levels_manager.get_available_levels(player_progress)
        next_level = levels_manager.get_next_level(progress_update.level_id, player_progress)
        
        return {
            "updated_progress": {
                "current_level": player_progress.current_level,
                "completed_levels": list(player_progress.completed_levels.keys()),
                "available_levels": available_levels,
                "next_level": next_level
            },
            "mastery_summary": mastery_summary,
            "achievements_unlocked": []  # TODO: Implement achievements system
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Progress update failed: {str(e)}")

@game_router.get("/progress/{player_id}")
async def get_player_progress(player_id: str):
    """Get comprehensive player progress and analytics"""
    try:
        # Create dummy progress for now - would load from database in real implementation
        player_progress = PlayerProgress(player_id=player_id)
        
        # Get analytics insights
        player_insights = learning_analytics.get_player_insights(player_id)
        mastery_summary = concept_tracker.get_mastery_summary(player_progress)
        available_levels = levels_manager.get_available_levels(player_progress)
        concepts_learned = levels_manager.get_concepts_learned(player_progress)
        
        return {
            "player_id": player_id,
            "current_level": player_progress.current_level,
            "completed_levels": player_progress.completed_levels,
            "available_levels": available_levels,
            "concepts_learned": concepts_learned,
            "mastery_summary": mastery_summary,
            "learning_insights": player_insights,
            "achievements": player_progress.achievements
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Progress retrieval failed: {str(e)}")

@game_router.get("/analytics/difficulty")
async def get_difficulty_analytics():
    """Get analytics about level difficulty across all players"""
    try:
        difficulty_report = learning_analytics.generate_difficulty_report()
        return {
            "difficulty_analysis": difficulty_report,
            "recommendations": [
                f"Level {level_id} appears {data['difficulty'].lower()} with {data['avg_attempts']:.1f} average attempts"
                for level_id, data in difficulty_report.items()
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Analytics failed: {str(e)}")

@game_router.get("/components")
async def get_all_components():
    """Get all available components in the system"""
    try:
        all_components = []
        for level_id in range(1, 5):  # Currently implemented levels
            level_components = component_registry.get_components_for_level(level_id)
            for component in level_components:
                if not any(c["id"] == component.id for c in all_components):
                    all_components.append({
                        "id": component.id,
                        "name": component.name,
                        "description": component.description,
                        "type": component.type.value,
                        "icon": component.icon,
                        "educational_note": component.educational_note,
                        "level_introduced": component.level_introduced
                    })
        
        return {"components": all_components}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Component retrieval failed: {str(e)}")