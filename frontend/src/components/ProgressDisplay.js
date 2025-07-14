import React from 'react';
import { motion } from 'framer-motion';
import { Target, Trophy, Star, Zap } from 'lucide-react';

const ProgressDisplay = ({ level, phase, score }) => {
  const getPhaseIcon = () => {
    switch (phase) {
      case 'building':
        return <Target size={16} className="text-blue-400" />;
      case 'training':
        return (
          <motion.div
            animate={{ rotate: 360 }}
            transition={{ duration: 2, repeat: Infinity, ease: 'linear' }}
          >
            <Zap size={16} className="text-yellow-400" />
          </motion.div>
        );
      case 'complete':
        return <Trophy size={16} className="text-green-400" />;
      default:
        return <Target size={16} className="text-gray-400" />;
    }
  };

  const getPhaseText = () => {
    switch (phase) {
      case 'building':
        return 'Building AI';
      case 'training':
        return 'Training...';
      case 'complete':
        return 'Complete!';
      default:
        return 'Ready';
    }
  };

  const getProgressBarWidth = () => {
    switch (phase) {
      case 'building':
        return '33%';
      case 'training':
        return '66%';
      case 'complete':
        return '100%';
      default:
        return '0%';
    }
  };

  const getScoreStars = () => {
    if (!score) return 0;
    if (score >= 0.9) return 3;
    if (score >= 0.7) return 2;
    return 1;
  };

  return (
    <div className="progress-display">
      <div className="level-info">
        <span className="level-badge">
          Level {level}
        </span>
        
        <div className="phase-indicator">
          {getPhaseIcon()}
          <span className="phase-text">{getPhaseText()}</span>
        </div>
      </div>

      <div className="progress-bar-container">
        <div className="progress-bar-background">
          <motion.div
            className="progress-bar-fill"
            initial={{ width: '0%' }}
            animate={{ width: getProgressBarWidth() }}
            transition={{ duration: 0.8, ease: 'easeOut' }}
          />
        </div>
      </div>

      {score !== null && score !== undefined && (
        <motion.div
          initial={{ opacity: 0, scale: 0.8 }}
          animate={{ opacity: 1, scale: 1 }}
          className="score-display"
        >
          <div className="score-stars">
            {[...Array(3)].map((_, i) => (
              <motion.div
                key={i}
                initial={{ opacity: 0, scale: 0 }}
                animate={{ 
                  opacity: i < getScoreStars() ? 1 : 0.3,
                  scale: i < getScoreStars() ? 1 : 0.7
                }}
                transition={{ delay: i * 0.1 }}
              >
                <Star 
                  size={14} 
                  className={i < getScoreStars() ? 'text-yellow-400' : 'text-gray-500'}
                  fill={i < getScoreStars() ? 'currentColor' : 'none'}
                />
              </motion.div>
            ))}
          </div>
          <span className="score-text">
            {Math.round(score * 100)}%
          </span>
        </motion.div>
      )}
    </div>
  );
};

export default ProgressDisplay;