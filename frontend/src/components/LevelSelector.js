import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { ChevronDown, Lock, CheckCircle, Crown } from 'lucide-react';

const LevelSelector = ({ currentLevel, onLevelSelect }) => {
  const [isOpen, setIsOpen] = useState(false);

  const levels = Array.from({ length: 21 }, (_, i) => {
    const level = i + 1;
    const isMiniBoss = level % 4 === 0 && level <= 20;
    const isUnlocked = level <= currentLevel + 1; // Allow access to current + 1 level
    const isCompleted = level < currentLevel;
    
    return {
      id: level,
      name: isMiniBoss ? `Mini-Boss ${Math.floor(level / 4)}` : `Level ${level}`,
      isMiniBoss,
      isUnlocked,
      isCompleted,
      title: getLevelTitle(level, isMiniBoss)
    };
  });

  function getLevelTitle(level, isMiniBoss) {
    if (isMiniBoss) {
      const bossNames = [
        'Smart Pet Challenge',
        'The Backprop Beast', 
        'Conv Neural Dragon',
        'Transformer Titan',
        'The Final LLM'
      ];
      return bossNames[Math.floor(level / 4) - 1] || `Boss ${Math.floor(level / 4)}`;
    }
    
    const levelTitles = {
      1: 'Train Your First AI Pet',
      2: 'Tensor Playground',
      3: 'Pattern Detective',
      5: 'Deep Learning Architect',
      6: 'Gradient Descent Master',
      7: 'Loss Function Explorer',
      9: 'Activation Alchemist',
      10: 'Optimization Wizard',
      11: 'Regularization Sage',
      13: 'Convolution Creator',
      14: 'Pooling Prodigy',
      15: 'Feature Map Master',
      17: 'Attention Architect',
      18: 'Transformer Builder',
      19: 'Self-Attention Savant',
      21: 'LLM Grandmaster'
    };
    
    return levelTitles[level] || `Level ${level}`;
  }

  const handleLevelSelect = (level) => {
    if (level.isUnlocked) {
      onLevelSelect(level.id);
      setIsOpen(false);
    }
  };

  return (
    <div className="level-selector">
      <motion.button
        className="level-selector-button"
        onClick={() => setIsOpen(!isOpen)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
      >
        <span className="current-level">
          {levels.find(l => l.id === currentLevel)?.name || `Level ${currentLevel}`}
        </span>
        <motion.div
          animate={{ rotate: isOpen ? 180 : 0 }}
          transition={{ duration: 0.2 }}
        >
          <ChevronDown size={16} />
        </motion.div>
      </motion.button>

      <AnimatePresence>
        {isOpen && (
          <>
            <motion.div
              className="level-selector-overlay"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              exit={{ opacity: 0 }}
              onClick={() => setIsOpen(false)}
            />
            <motion.div
              className="level-selector-dropdown"
              initial={{ opacity: 0, y: -10, scale: 0.95 }}
              animate={{ opacity: 1, y: 0, scale: 1 }}
              exit={{ opacity: 0, y: -10, scale: 0.95 }}
              transition={{ type: 'spring', stiffness: 300, damping: 30 }}
            >
              <div className="dropdown-header">
                <h4>Select Level</h4>
                <p>Choose your AI learning adventure</p>
              </div>
              
              <div className="levels-grid">
                {levels.map((level, index) => (
                  <motion.div
                    key={level.id}
                    className={`level-item ${
                      level.id === currentLevel ? 'current' : ''
                    } ${
                      !level.isUnlocked ? 'locked' : ''
                    } ${
                      level.isCompleted ? 'completed' : ''
                    } ${
                      level.isMiniBoss ? 'mini-boss' : ''
                    }`}
                    initial={{ opacity: 0, x: -20 }}
                    animate={{ opacity: 1, x: 0 }}
                    transition={{ delay: index * 0.02 }}
                    onClick={() => handleLevelSelect(level)}
                    whileHover={level.isUnlocked ? { scale: 1.02 } : {}}
                    whileTap={level.isUnlocked ? { scale: 0.98 } : {}}
                  >
                    <div className="level-item-header">
                      <div className="level-item-icon">
                        {!level.isUnlocked ? (
                          <Lock size={16} className="text-gray-500" />
                        ) : level.isCompleted ? (
                          <CheckCircle size={16} className="text-green-400" />
                        ) : level.isMiniBoss ? (
                          <Crown size={16} className="text-yellow-400" />
                        ) : (
                          <div className="level-number">{level.id}</div>
                        )}
                      </div>
                      <div className="level-item-info">
                        <div className="level-item-name">{level.name}</div>
                        <div className="level-item-title">{level.title}</div>
                      </div>
                    </div>
                    
                    {level.id === currentLevel && (
                      <motion.div
                        className="current-indicator"
                        layoutId="currentLevel"
                        transition={{ type: 'spring', stiffness: 300, damping: 30 }}
                      />
                    )}
                  </motion.div>
                ))}
              </div>
              
              <div className="dropdown-footer">
                <div className="progress-summary">
                  <span className="completed-count">
                    {levels.filter(l => l.isCompleted).length} / 21
                  </span>
                  <span className="progress-text">Levels Completed</span>
                </div>
              </div>
            </motion.div>
          </>
        )}
      </AnimatePresence>
    </div>
  );
};

export default LevelSelector;