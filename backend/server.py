from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
import torch
import torch.nn as nn
import torch.optim as optim
import json
import numpy as np
from engine import TensorForgeEngine
from levels import LevelsManager
import base64
from PIL import Image
import io

app = FastAPI(title="Tensor Forge API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize game engine
engine = TensorForgeEngine()
levels_manager = LevelsManager(engine)

# Pydantic models
class TrainingData(BaseModel):
    drawings: List[Dict[str, Any]]
    labels: List[str]

class GameBuild(BaseModel):
    components: List[Dict[str, Any]]
    level_id: int

class SimulationResult(BaseModel):
    success: bool
    score: float
    message: str
    visual_data: Optional[Dict[str, Any]] = None

@app.get("/api/health")
async def health_check():
    return {"status": "healthy", "message": "Tensor Forge API is running!"}

@app.get("/api/levels/{level_id}")
async def get_level(level_id: int):
    """Get level configuration and requirements"""
    if level_id == 1:
        return {
            "id": 1,
            "title": "Train Your First AI Pet",
            "description": "Draw shapes and watch your AI learn to recognize them!",
            "objective": "Train a neural network to classify hand-drawn shapes",
            "available_components": [
                {
                    "id": "neural_layer",
                    "name": "Neural Layer",
                    "description": "A layer of artificial neurons",
                    "type": "layer",
                    "icon": "brain"
                },
                {
                    "id": "activation",
                    "name": "Activation Function",
                    "description": "Makes the network learn non-linear patterns",
                    "type": "function",
                    "icon": "zap"
                }
            ],
            "target_accuracy": 0.8,
            "max_epochs": 50
        }
    else:
        raise HTTPException(status_code=404, detail="Level not found")

@app.post("/api/train-shape-classifier")
async def train_shape_classifier(training_data: TrainingData):
    """Train a simple shape classifier with user drawings"""
    try:
        # Process drawings into training data
        X_train = []
        y_train = []
        
        label_map = {"circle": 0, "square": 1, "triangle": 2}
        
        for drawing, label in zip(training_data.drawings, training_data.labels):
            if label not in label_map:
                continue
                
            # Convert drawing points to 28x28 image
            image_array = drawing_to_array(drawing["points"])
            X_train.append(image_array.flatten())
            y_train.append(label_map[label])
        
        if len(X_train) < 3:
            return SimulationResult(
                success=False,
                score=0.0,
                message="Need at least 3 training examples!",
                visual_data={"error": "insufficient_data"}
            )
        
        # Convert to tensors
        X_tensor = torch.FloatTensor(X_train)
        y_tensor = torch.LongTensor(y_train)
        
        # Create simple neural network
        model = SimpleShapeClassifier()
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=0.01)
        
        # Training loop
        training_history = []
        for epoch in range(30):
            optimizer.zero_grad()
            outputs = model(X_tensor)
            loss = criterion(outputs, y_tensor)
            loss.backward()
            optimizer.step()
            
            # Calculate accuracy
            _, predicted = torch.max(outputs.data, 1)
            accuracy = (predicted == y_tensor).sum().item() / len(y_tensor)
            
            training_history.append({
                "epoch": epoch + 1,
                "loss": loss.item(),
                "accuracy": accuracy
            })
        
        final_accuracy = training_history[-1]["accuracy"]
        success = final_accuracy >= 0.8
        
        return SimulationResult(
            success=success,
            score=final_accuracy,
            message=f"AI trained! Final accuracy: {final_accuracy:.1%}",
            visual_data={
                "training_history": training_history,
                "model_weights": get_model_visualization(model),
                "predictions": get_predictions(model, X_tensor, y_tensor)
            }
        )
        
    except Exception as e:
        return SimulationResult(
            success=False,
            score=0.0,
            message=f"Training failed: {str(e)}",
            visual_data={"error": "training_failed"}
        )

@app.post("/api/simulate-build")
async def simulate_build(build: GameBuild):
    """Simulate a player's component build"""
    try:
        # Load the specified level
        success = levels_manager.load_level(build.level_id)
        if not success:
            raise HTTPException(status_code=404, detail="Level not found")
        
        # Clear previous build
        engine.player_build = []
        
        # Add components to build
        for component in build.components:
            engine.append_to_build(component["name"], *component.get("args", []))
        
        # Run simulation
        if build.level_id == 1:
            # Special handling for shape classifier level
            return SimulationResult(
                success=True,
                score=0.9,
                message="Neural network built successfully! Ready for training.",
                visual_data={"network_structure": build.components}
            )
        else:
            # Standard tensor simulation
            result = engine.build_and_simulate(engine.level_data['inputs'])
            success = engine.check_win(result, engine.level_data['target'])
            
            return SimulationResult(
                success=success,
                score=1.0 if success else 0.0,
                message="Success!" if success else "Try again!",
                visual_data={"result": result.tolist()}
            )
            
    except Exception as e:
        return SimulationResult(
            success=False,
            score=0.0,
            message=f"Simulation failed: {str(e)}"
        )

# Helper classes and functions
class SimpleShapeClassifier(nn.Module):
    def __init__(self):
        super(SimpleShapeClassifier, self).__init__()
        self.fc1 = nn.Linear(784, 64)  # 28x28 = 784
        self.fc2 = nn.Linear(64, 32)
        self.fc3 = nn.Linear(32, 3)   # 3 classes: circle, square, triangle
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)
        
    def forward(self, x):
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x

def drawing_to_array(points):
    """Convert drawing points to 28x28 numpy array"""
    # Create blank 28x28 image
    image = np.zeros((28, 28))
    
    if not points:
        return image
    
    # Normalize points to 28x28 grid
    xs = [p["x"] for p in points]
    ys = [p["y"] for p in points]
    
    if not xs or not ys:
        return image
        
    min_x, max_x = min(xs), max(xs)
    min_y, max_y = min(ys), max(ys)
    
    # Avoid division by zero
    if max_x == min_x:
        max_x = min_x + 1
    if max_y == min_y:
        max_y = min_y + 1
    
    for point in points:
        # Normalize to 0-27 range
        x = int(((point["x"] - min_x) / (max_x - min_x)) * 27)
        y = int(((point["y"] - min_y) / (max_y - min_y)) * 27)
        
        # Ensure within bounds
        x = max(0, min(27, x))
        y = max(0, min(27, y))
        
        image[y, x] = 1.0
    
    return image

def get_model_visualization(model):
    """Extract model weights for visualization"""
    weights = {}
    for name, param in model.named_parameters():
        weights[name] = param.data.cpu().numpy().tolist()
    return weights

def get_predictions(model, X_tensor, y_tensor):
    """Get model predictions for visualization"""
    with torch.no_grad():
        outputs = model(X_tensor)
        _, predicted = torch.max(outputs, 1)
        
    label_names = ["circle", "square", "triangle"]
    predictions = []
    
    for i in range(len(predicted)):
        predictions.append({
            "true_label": label_names[y_tensor[i].item()],
            "predicted_label": label_names[predicted[i].item()],
            "confidence": torch.softmax(outputs[i], 0).tolist()
        })
    
    return predictions

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)