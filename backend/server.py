"""
Tensor Forge API Server - Enhanced Architecture
Educational AI puzzle game backend with comprehensive learning system.
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

from api.game_endpoints import game_router
from core.components.registry import component_registry
from core.levels.manager import levels_manager
from core.engine.simulation import simulation_engine
from core.education.hints import hint_system
from core.education.progress import concept_tracker, learning_analytics

# Create FastAPI app
app = FastAPI(
    title="Tensor Forge API", 
    version="2.0.0-enhanced",
    description="Educational AI puzzle game backend with comprehensive learning system"
)

# CORS middleware - allow frontend to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include game endpoints
app.include_router(game_router)

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize the game systems on startup"""
    print("🚀 Starting Tensor Forge Enhanced API...")
    
    # Verify core systems are initialized
    print(f"📚 Loaded {len(levels_manager.levels)} levels")
    print(f"🧩 Registered {len(component_registry.components)} components")
    print("🎯 Hint system ready")
    print("📊 Analytics system ready")
    print("✅ All systems initialized successfully!")

# Root endpoint
@app.get("/")
async def root():
    """Welcome endpoint with API information"""
    return {
        "message": "Welcome to Tensor Forge Enhanced API!",
        "version": "2.0.0-enhanced", 
        "description": "Educational AI puzzle game backend",
        "features": [
            "Comprehensive level management",
            "Component registry system", 
            "Advanced simulation engine",
            "Adaptive hint system",
            "Learning progress tracking",
            "Educational analytics"
        ],
        "endpoints": {
            "levels": "/api/levels/{level_id}",
            "simulate": "/api/simulate-build",
            "train": "/api/train-shape-classifier", 
            "hint": "/api/hint",
            "progress": "/api/progress/{player_id}",
            "components": "/api/components"
        }
    }

# Error handlers
@app.exception_handler(404)
async def not_found_handler(request, exc):
    return {"error": "Endpoint not found", "message": "The requested resource does not exist"}

@app.exception_handler(500)
async def internal_error_handler(request, exc):
    return {"error": "Internal server error", "message": "An unexpected error occurred"}

# Development server
if __name__ == "__main__":
    uvicorn.run(
        "server:app", 
        host="0.0.0.0", 
        port=8001,
        reload=True,
        log_level="info"
    )