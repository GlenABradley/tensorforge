import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { DndProvider } from 'react-dnd';
import { HTML5Backend } from 'react-dnd-html5-backend';
import DrawingCanvas from './components/DrawingCanvas';
import ComponentLibrary from './components/ComponentLibrary';
import NetworkBuilder from './components/NetworkBuilder';
import TrainingPanel from './components/TrainingPanel';
import ProgressDisplay from './components/ProgressDisplay';
import LevelSelector from './components/LevelSelector';
import { Brain, Zap, Target, Trophy, Sparkles } from 'lucide-react';
import './App.css';

const BACKEND_URL = process.env.REACT_APP_BACKEND_URL || 'http://localhost:8001';

function App() {
  const [currentLevel, setCurrentLevel] = useState(1);
  const [levelData, setLevelData] = useState(null);
  const [playerBuild, setPlayerBuild] = useState([]);
  const [drawings, setDrawings] = useState([]);
  const [trainingData, setTrainingData] = useState([]);
  const [isTraining, setIsTraining] = useState(false);
  const [trainingResults, setTrainingResults] = useState(null);
  const [gamePhase, setGamePhase] = useState('building'); // 'building', 'training', 'complete'
  const [showCelebration, setShowCelebration] = useState(false);
  const [aiPersonality, setAiPersonality] = useState('curious'); // 'curious', 'excited', 'confident'

  useEffect(() => {
    loadLevel(currentLevel);
  }, [currentLevel]);

  const loadLevel = async (levelId) => {
    try {
      console.log(`Loading level ${levelId} from ${BACKEND_URL}/api/levels/${levelId}`);
      const response = await fetch(`${BACKEND_URL}/api/levels/${levelId}`);
      
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      
      const data = await response.json();
      console.log('Level data loaded:', data);
      setLevelData(data);
      setPlayerBuild([]);
      setDrawings([]);
      setTrainingData([]);
      setTrainingResults(null);
      setGamePhase('building');
      setShowCelebration(false);
    } catch (error) {
      console.error('Failed to load level:', error);
      // Fallback level data to prevent infinite loading - provide appropriate fallback based on level
      if (levelId === 2) {
        setLevelData({
          id: 2,
          title: "Build Your First Neural Network",
          description: "Learn to stack layers and create deeper AI networks!",
          objective: "Build a multi-layer neural network and understand tensor flow",
          available_components: [
            {
              id: "neural_layer",
              name: "Neural Layer",
              description: "A layer of artificial neurons",
              type: "layer",
              icon: "brain"
            },
            {
              id: "activation",
              name: "Activation Function",
              description: "Makes the network learn non-linear patterns",
              type: "function",
              icon: "zap"
            },
            {
              id: "dense_layer",
              name: "Dense Layer",
              description: "A fully connected layer for deeper learning",
              type: "layer",
              icon: "layers"
            },
            {
              id: "dropout",
              name: "Dropout",
              description: "Prevents overfitting by randomly ignoring neurons",
              type: "regularization",
              icon: "lightbulb"
            }
          ],
          target_accuracy: 0.85,
          max_epochs: 100
        });
      } else {
        // Default to Level 1 fallback
        setLevelData({
          id: levelId,
          title: "Train Your First AI Pet",
          description: "Draw shapes and watch your AI learn to recognize them!",
          objective: "Train a neural network to classify hand-drawn shapes",
          available_components: [
            {
              id: "neural_layer",
              name: "Neural Layer",
              description: "A layer of artificial neurons",
              type: "layer",
              icon: "brain"
            },
            {
              id: "activation",
              name: "Activation Function",
              description: "Makes the network learn non-linear patterns",
              type: "function",
              icon: "zap"
            }
          ],
          target_accuracy: 0.8,
          max_epochs: 50
        });
      }
    }
  };

  const addComponent = (component) => {
    setPlayerBuild(prev => [...prev, { ...component, id: Date.now() }]);
    
    // AI personality reaction
    if (component.id === 'neural_layer') {
      setAiPersonality('excited');
      setTimeout(() => setAiPersonality('curious'), 2000);
    }
  };

  const removeComponent = (componentId) => {
    setPlayerBuild(prev => prev.filter(comp => comp.id !== componentId));
  };

  const addDrawing = (drawingData, label) => {
    const newDrawing = {
      id: Date.now(),
      points: drawingData,
      label: label,
      timestamp: new Date().toISOString()
    };
    
    setDrawings(prev => [...prev, newDrawing]);
    setTrainingData(prev => [
      ...prev,
      { drawing: drawingData, label: label }
    ]);
  };

  const startTraining = async () => {
    // Level-specific training logic
    if (currentLevel === 1) {
      // Level 1: Shape classifier training
      if (trainingData.length < 3) {
        alert('Draw at least 3 shapes to train your AI!');
        return;
      }

      setIsTraining(true);
      setGamePhase('training');
      setAiPersonality('excited');

      try {
        console.log('Starting training with data:', trainingData);
        
        const response = await fetch(`${BACKEND_URL}/api/train-shape-classifier`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            drawings: trainingData.map(d => ({ points: d.drawing })),
            labels: trainingData.map(d => d.label)
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const results = await response.json();
        console.log('Training results:', results);
        setTrainingResults(results);
        
        if (results.success) {
          setGamePhase('complete');
          setShowCelebration(true);
          setAiPersonality('confident');
          
          // Celebration timeout
          setTimeout(() => {
            setShowCelebration(false);
          }, 4000);
        } else {
          setGamePhase('building');
          setAiPersonality('curious');
        }
      } catch (error) {
        console.error('Training failed:', error);
        alert(`Training failed: ${error.message}. Please try again.`);
        setGamePhase('building');
        setAiPersonality('curious');
      } finally {
        setIsTraining(false);
      }
    } else if (currentLevel === 2) {
      // Level 2: Network simulation
      if (playerBuild.length < 3) {
        alert('Build at least 3 components to run the simulation!');
        return;
      }

      setIsTraining(true);
      setGamePhase('training');
      setAiPersonality('excited');

      try {
        console.log('Starting network simulation with components:', playerBuild);
        
        const response = await fetch(`${BACKEND_URL}/api/simulate-build`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            components: playerBuild.map(comp => ({
              name: comp.name,
              type: comp.type,
              id: comp.id
            })),
            level_id: currentLevel
          })
        });

        if (!response.ok) {
          throw new Error(`HTTP error! status: ${response.status}`);
        }

        const results = await response.json();
        console.log('Simulation results:', results);
        setTrainingResults(results);
        
        if (results.success) {
          setGamePhase('complete');
          setShowCelebration(true);
          setAiPersonality('confident');
          
          // Celebration timeout
          setTimeout(() => {
            setShowCelebration(false);
          }, 4000);
        } else {
          setGamePhase('building');
          setAiPersonality('curious');
        }
      } catch (error) {
        console.error('Simulation failed:', error);
        alert(`Simulation failed: ${error.message}. Please try again.`);
        setGamePhase('building');
        setAiPersonality('curious');
      } finally {
        setIsTraining(false);
      }
    }
  };

  const resetLevel = () => {
    loadLevel(currentLevel);
  };

  const nextLevel = () => {
    if (currentLevel < 21) {
      setCurrentLevel(currentLevel + 1);
    }
  };

  const getAiMessage = () => {
    if (isTraining) return "I'm learning from your drawings! 🧠";
    
    // Level-specific AI messages
    if (currentLevel === 2) {
      switch (aiPersonality) {
        case 'excited':
          return "More layers! I'm getting more powerful! 🚀";
        case 'confident':
          return "I'm ready to tackle complex problems now! 💪";
        case 'curious':
        default:
          if (playerBuild.length === 0) {
            return "Hi! I'm ready for Level 2. Let's build a deeper network! 🧠";
          } else if (playerBuild.length < 3) {
            return "Add more layers to make me smarter! I need at least 3 components. 🎯";
          } else {
            return `Great! I have ${playerBuild.length} components. Ready to process data! 📊`;
          }
      }
    }
    
    // Level 1 messages
    switch (aiPersonality) {
      case 'excited':
        return "Wow! A neural layer! I can feel myself getting smarter! ✨";
      case 'confident':
        return "I'm ready for anything now! What should we learn next? 🚀";
      case 'curious':
      default:
        if (playerBuild.length === 0) {
          return "Hi! I'm your AI pet. Help me learn by adding components! 🤖";
        } else if (trainingData.length === 0) {
          return "I have a brain now! Can you draw some shapes for me to learn? 🎨";
        } else {
          return `I've seen ${trainingData.length} drawings. Ready to start learning! 📚`;
        }
    }
  };

  if (!levelData) {
    return (
      <div className="loading-screen">
        <motion.div
          animate={{ rotate: 360 }}
          transition={{ duration: 2, repeat: Infinity, ease: "linear" }}
        >
          <Brain size={48} className="text-blue-400" />
        </motion.div>
        <p>Loading Tensor Forge...</p>
      </div>
    );
  }

  return (
    <DndProvider backend={HTML5Backend}>
      <div className="app">
        <AnimatePresence>
          {showCelebration && (
            <motion.div
              initial={{ opacity: 0, scale: 0.5 }}
              animate={{ opacity: 1, scale: 1 }}
              exit={{ opacity: 0, scale: 0.5 }}
              className="celebration-overlay"
            >
              <div className="celebration-content">
                <motion.div
                  animate={{ rotate: [0, 360], scale: [1, 1.2, 1] }}
                  transition={{ duration: 2, repeat: Infinity }}
                >
                  <Trophy size={80} className="text-yellow-400" />
                </motion.div>
                <h2>Level Complete!</h2>
                <p>Your AI learned to recognize shapes! 🎉</p>
                <Sparkles className="celebration-sparkle" />
              </div>
            </motion.div>
          )}
        </AnimatePresence>

        <header className="app-header">
          <div className="header-content">
            <motion.div
              className="logo"
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
            >
              <Brain className="logo-icon" />
              <span>Tensor Forge</span>
            </motion.div>
            
            <LevelSelector 
              currentLevel={currentLevel}
              onLevelSelect={setCurrentLevel}
            />
            
            <ProgressDisplay 
              level={currentLevel}
              phase={gamePhase}
              score={trainingResults?.score}
            />
          </div>
        </header>

        <main className="app-main">
          <div className="level-header">
            <motion.h1
              key={levelData.title}
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              className="level-title"
            >
              <Target className="level-icon" />
              {levelData.title}
            </motion.h1>
            <p className="level-description">{levelData.description}</p>
          </div>

          <div className="game-layout">
            <div className="left-panel">
              <ComponentLibrary 
                components={levelData.available_components}
                onAddComponent={addComponent}
                disabled={gamePhase === 'training'}
              />
              
              <motion.div 
                className="ai-chat"
                animate={{ 
                  scale: aiPersonality === 'excited' ? [1, 1.05, 1] : 1,
                  backgroundColor: 
                    aiPersonality === 'excited' ? '#1e40af' :
                    aiPersonality === 'confident' ? '#059669' : '#374151'
                }}
                transition={{ duration: 0.5 }}
              >
                <div className="ai-avatar">
                  <motion.div
                    animate={{ 
                      rotate: isTraining ? 360 : 0,
                      scale: isTraining ? [1, 1.1, 1] : 1
                    }}
                    transition={{ 
                      duration: isTraining ? 2 : 0.5,
                      repeat: isTraining ? Infinity : 0
                    }}
                  >
                    <Brain size={24} />
                  </motion.div>
                </div>
                <div className="ai-message">
                  {getAiMessage()}
                </div>
              </motion.div>
            </div>

            <div className="center-panel">
              <NetworkBuilder
                components={playerBuild}
                onRemoveComponent={removeComponent}
                disabled={gamePhase === 'training'}
              />
              
              {currentLevel === 1 && (
                <DrawingCanvas
                  onDrawingComplete={addDrawing}
                  disabled={gamePhase === 'training'}
                  drawings={drawings}
                />
              )}
            </div>

            <div className="right-panel">
              <TrainingPanel
                onStartTraining={startTraining}
                isTraining={isTraining}
                results={trainingResults}
                canTrain={playerBuild.length > 0 && trainingData.length >= 3}
                trainingDataCount={trainingData.length}
              />
              
              {gamePhase === 'complete' && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="level-complete-actions"
                >
                  <button onClick={resetLevel} className="secondary-button">
                    Try Again
                  </button>
                  <button onClick={nextLevel} className="primary-button">
                    Next Level <Zap size={16} />
                  </button>
                </motion.div>
              )}
            </div>
          </div>
        </main>
      </div>
    </DndProvider>
  );
}

export default App;