import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Network, X, ArrowDown, Brain, Zap, Layers } from 'lucide-react';

const NetworkBuilder = ({ components, onRemoveComponent, disabled }) => {
  const getComponentIcon = (iconName) => {
    const icons = {
      brain: Brain,
      zap: Zap,
      layers: Layers,
      repeat: ArrowDown
    };
    
    const IconComponent = icons[iconName] || Brain;
    return <IconComponent size={20} />;
  };

  const getConnectionLine = (index) => {
    if (index === components.length - 1) return null;
    
    return (
      <motion.div
        initial={{ scaleY: 0 }}
        animate={{ scaleY: 1 }}
        transition={{ delay: 0.2 }}
        style={{
          width: '2px',
          height: '20px',
          background: 'linear-gradient(to bottom, #60a5fa, #3b82f6)',
          margin: '0 auto',
          position: 'relative'
        }}
      >
        <motion.div
          animate={{ y: [0, 10, 0] }}
          transition={{ duration: 2, repeat: Infinity }}
          style={{
            position: 'absolute',
            top: '50%',
            left: '50%',
            transform: 'translate(-50%, -50%)',
            width: '6px',
            height: '6px',
            background: '#60a5fa',
            borderRadius: '50%',
            boxShadow: '0 0 10px rgba(96, 165, 250, 0.8)'
          }}
        />
      </motion.div>
    );
  };

  return (
    <div className="network-builder">
      <h3>
        <Network size={20} />
        Your AI Network
      </h3>
      
      <div className={`build-area ${components.length === 0 ? 'empty' : ''}`}>
        {components.length === 0 ? (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{
              textAlign: 'center',
              color: '#64748b',
              fontSize: '0.95rem'
            }}
          >
            <Brain size={48} style={{ margin: '0 auto 1rem', opacity: 0.3 }} />
            <div>Your AI network will appear here</div>
            <div style={{ fontSize: '0.8rem', marginTop: '0.5rem' }}>
              Add components from the library to get started
            </div>
          </motion.div>
        ) : (
          <AnimatePresence>
            {components.map((component, index) => (
              <React.Fragment key={component.id}>
                <motion.div
                  initial={{ opacity: 0, y: 20, scale: 0.9 }}
                  animate={{ opacity: 1, y: 0, scale: 1 }}
                  exit={{ opacity: 0, y: -20, scale: 0.9 }}
                  transition={{ 
                    type: 'spring',
                    stiffness: 300,
                    damping: 25,
                    delay: index * 0.1 
                  }}
                  className="build-component"
                  whileHover={{ scale: 1.02 }}
                >
                  <div className="build-component-info">
                    <motion.div
                      className="component-icon"
                      animate={{ 
                        rotate: component.name === 'Training Loop' ? 360 : 0,
                        scale: [1, 1.1, 1]
                      }}
                      transition={{ 
                        rotate: { duration: 3, repeat: Infinity, ease: 'linear' },
                        scale: { duration: 2, repeat: Infinity }
                      }}
                    >
                      {getComponentIcon(component.icon)}
                    </motion.div>
                    <div>
                      <div className="build-component-name">
                        {component.name}
                      </div>
                      <div style={{ 
                        fontSize: '0.8rem', 
                        color: '#94a3b8',
                        marginTop: '0.25rem'
                      }}>
                        {component.description}
                      </div>
                    </div>
                  </div>
                  
                  {!disabled && (
                    <motion.button
                      className="remove-component"
                      onClick={() => onRemoveComponent(component.id)}
                      whileHover={{ scale: 1.1, rotate: 90 }}
                      whileTap={{ scale: 0.9 }}
                    >
                      <X size={14} />
                    </motion.button>
                  )}
                </motion.div>
                
                {getConnectionLine(index)}
              </React.Fragment>
            ))}
          </AnimatePresence>
        )}
      </div>
      
      {components.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.3 }}
          style={{
            marginTop: '1rem',
            padding: '1rem',
            background: 'rgba(34, 197, 94, 0.1)',
            borderRadius: '8px',
            border: '1px solid rgba(34, 197, 94, 0.2)',
            textAlign: 'center'
          }}
        >
          <div style={{ 
            color: '#86efac', 
            fontSize: '0.9rem',
            fontWeight: '600',
            marginBottom: '0.5rem'
          }}>
            🎉 Great! Your AI has {components.length} component{components.length > 1 ? 's' : ''}
          </div>
          <div style={{ 
            color: '#cbd5e1', 
            fontSize: '0.8rem',
            lineHeight: 1.4
          }}>
            {components.length === 1 && "Add more components or start training with drawings!"}
            {components.length === 2 && "Your AI is getting smarter! Try adding training data."}
            {components.length >= 3 && "This AI looks powerful! Ready to train it?"}
          </div>
        </motion.div>
      )}
      
      {disabled && (
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          style={{
            position: 'absolute',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            background: 'rgba(0, 0, 0, 0.3)',
            borderRadius: '12px',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            color: '#60a5fa',
            fontSize: '0.9rem',
            fontWeight: '600'
          }}
        >
          🧠 AI is training...
        </motion.div>
      )}
    </div>
  );
};

export default NetworkBuilder;