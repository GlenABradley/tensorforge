import React from 'react';
import { motion } from 'framer-motion';
import { Play, Square, TrendingUp, Target, CheckCircle, XCircle } from 'lucide-react';

const TrainingPanel = ({ 
  onStartTraining, 
  isTraining, 
  results, 
  canTrain, 
  trainingDataCount,
  level = 1
}) => {
  const formatAccuracy = (accuracy) => {
    return `${Math.round(accuracy * 100)}%`;
  };

  const getAccuracyColor = (accuracy) => {
    if (accuracy >= 0.9) return '#10b981'; // Green
    if (accuracy >= 0.7) return '#f59e0b'; // Yellow
    return '#ef4444'; // Red
  };

  const getTrainingMessage = () => {
    if (level === 1) {
      if (trainingDataCount === 0) {
        return "Draw some shapes first!";
      } else if (trainingDataCount < 3) {
        return `Need ${3 - trainingDataCount} more drawings`;
      } else if (!canTrain) {
        return "Add AI components first!";
      } else {
        return "Ready to train!";
      }
    } else if (level === 2) {
      if (trainingDataCount === 0) {
        return "Add AI components first!";
      } else if (trainingDataCount < 3) {
        return `Need ${3 - trainingDataCount} more components`;
      } else {
        return "Ready to simulate!";
      }
    }
    return "Ready to proceed!";
  };

  const getStatsLabel = () => {
    return level === 1 ? "Training Examples" : "Components Built";
  };

  const getButtonText = () => {
    if (isTraining) {
      return level === 1 ? "Training Neural Network..." : "Running Simulation...";
    }
    if (canTrain) {
      return level === 1 ? "Start Training" : "Run Simulation";
    }
    return getTrainingMessage();
  };

  return (
    <div className="training-panel">
      <h3>
        <TrendingUp size={20} />
        AI Training
      </h3>
      
      {isTraining && (
        <motion.div
          initial={{ opacity: 0, y: -10 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            marginBottom: '1rem',
            padding: '1rem',
            background: 'rgba(251, 191, 36, 0.1)',
            borderRadius: '8px',
            border: '1px solid rgba(251, 191, 36, 0.3)',
            textAlign: 'center'
          }}
        >
          <motion.div
            animate={{ scale: [1, 1.1, 1] }}
            transition={{ duration: 1, repeat: Infinity }}
            style={{ color: '#fbbf24', marginBottom: '0.5rem' }}
          >
            🧠 Training Neural Network...
          </motion.div>
          <div style={{ fontSize: '0.85rem', color: '#cbd5e1', lineHeight: 1.4 }}>
            Your AI is learning to recognize shapes by studying your drawings. 
            This involves adjusting thousands of connections in the neural network!
          </div>
        </motion.div>
      )}
      
      <div className="training-stats">
        <div className="stat-item">
          <span className="stat-label">{getStatsLabel()}</span>
          <motion.span 
            className="stat-value"
            animate={{ scale: trainingDataCount > 0 ? [1, 1.1, 1] : 1 }}
            transition={{ duration: 0.3 }}
          >
            {trainingDataCount}
          </motion.span>
        </div>
        
        <div className="stat-item">
          <span className="stat-label">Target Accuracy</span>
          <span className="stat-value">{level === 1 ? "80%" : "85%"}</span>
        </div>
        
        {results && (
          <motion.div
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="stat-item"
          >
            <span className="stat-label">AI Confidence</span>
            <span 
              className="stat-value"
              style={{ color: getAccuracyColor(results.score) }}
            >
              {formatAccuracy(results.score)}
            </span>
          </motion.div>
        )}
      </div>

      <motion.button
        className={`training-button ${isTraining ? 'training' : ''}`}
        onClick={onStartTraining}
        disabled={!canTrain || isTraining}
        whileHover={canTrain && !isTraining ? { scale: 1.02 } : {}}
        whileTap={canTrain && !isTraining ? { scale: 0.98 } : {}}
        animate={isTraining ? { 
          background: [
            'linear-gradient(135deg, #f59e0b, #d97706)',
            'linear-gradient(135deg, #fbbf24, #f59e0b)',
            'linear-gradient(135deg, #f59e0b, #d97706)'
          ],
          boxShadow: [
            '0 0 20px rgba(245, 158, 11, 0.3)',
            '0 0 30px rgba(245, 158, 11, 0.5)',
            '0 0 20px rgba(245, 158, 11, 0.3)'
          ]
        } : {}}
        transition={{ duration: 1, repeat: isTraining ? Infinity : 0 }}
      >
        {isTraining ? (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            >
              <TrendingUp size={16} />
            </motion.div>
            Training Neural Network...
          </>
        ) : (
          <>
            <Play size={16} />
            {canTrain ? 'Start Training' : getTrainingMessage()}
          </>
        )}
      </motion.button>

      {results && (
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          className={`training-results ${results.success ? '' : 'failed'}`}
        >
          <div className="results-header">
            {results.success ? (
              <CheckCircle size={20} className="text-green-400" />
            ) : (
              <XCircle size={20} className="text-red-400" />
            )}
            <span className={`results-title ${results.success ? '' : 'failed'}`}>
              {results.success ? 'Training Successful!' : 'Training Failed'}
            </span>
          </div>
          
          <p className="results-message">
            {results.message}
          </p>
          
          <motion.div
            className="accuracy-display"
            animate={{ 
              borderColor: getAccuracyColor(results.score),
              boxShadow: `0 0 20px ${getAccuracyColor(results.score)}30`
            }}
            transition={{ duration: 0.5 }}
          >
            <div className="accuracy-label">Final Accuracy</div>
            <motion.div
              className="accuracy-value"
              style={{ color: getAccuracyColor(results.score) }}
              animate={{ scale: [1, 1.2, 1] }}
              transition={{ duration: 0.5 }}
            >
              {formatAccuracy(results.score)}
            </motion.div>
          </motion.div>
          
          {results.visual_data && results.visual_data.training_history && (
            <motion.div
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ delay: 0.5 }}
              style={{
                marginTop: '1rem',
                padding: '0.75rem',
                background: 'rgba(59, 130, 246, 0.1)',
                borderRadius: '6px',
                border: '1px solid rgba(59, 130, 246, 0.2)'
              }}
            >
              <div style={{ 
                fontSize: '0.8rem', 
                color: '#60a5fa',
                marginBottom: '0.5rem'
              }}>
                Training Progress
              </div>
              <div style={{ 
                fontSize: '0.75rem', 
                color: '#cbd5e1',
                lineHeight: 1.3
              }}>
                Trained for {results.visual_data.training_history.length} epochs
                <br />
                Final loss: {results.visual_data.training_history[results.visual_data.training_history.length - 1]?.loss.toFixed(4)}
              </div>
            </motion.div>
          )}
          
          {results.success && (
            <motion.div
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: 1 }}
              style={{
                marginTop: '1rem',
                padding: '1rem',
                background: 'linear-gradient(135deg, rgba(34, 197, 94, 0.1), rgba(16, 185, 129, 0.1))',
                borderRadius: '8px',
                border: '1px solid rgba(34, 197, 94, 0.3)',
                textAlign: 'center'
              }}
            >
              <div style={{ 
                fontSize: '1rem',
                color: '#10b981',
                fontWeight: '600',
                marginBottom: '0.5rem'
              }}>
                🎉 Congratulations!
              </div>
              <div style={{ 
                fontSize: '0.85rem',
                color: '#cbd5e1',
                lineHeight: 1.4
              }}>
                Your AI successfully learned to recognize shapes! 
                It can now tell the difference between circles, squares, and triangles.
              </div>
            </motion.div>
          )}
        </motion.div>
      )}
    </div>
  );
};

export default TrainingPanel;