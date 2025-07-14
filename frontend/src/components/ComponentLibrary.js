import React from 'react';
import { motion } from 'framer-motion';
import { Brain, Zap, Layers, Plus, Lightbulb } from 'lucide-react';

const ComponentLibrary = ({ components, onAddComponent, disabled, level = 1 }) => {
  const getComponentIcon = (iconName) => {
    const icons = {
      brain: Brain,
      zap: Zap,
      layers: Layers,
      plus: Plus,
      lightbulb: Lightbulb
    };
    
    const IconComponent = icons[iconName] || Brain;
    return <IconComponent size={20} />;
  };

  const handleAddComponent = (component) => {
    if (disabled) return;
    onAddComponent(component);
  };

  return (
    <div className="component-library">
      <h3>
        <Layers size={20} />
        AI Components
      </h3>
      
      <div style={{
        marginBottom: '1rem',
        padding: '0.75rem',
        background: 'rgba(34, 197, 94, 0.1)',
        borderRadius: '6px',
        border: '1px solid rgba(34, 197, 94, 0.2)',
        fontSize: '0.85rem',
        color: '#86efac',
        lineHeight: 1.4
      }}>
        🧠 <strong>Build Your AI Brain:</strong><br/>
        1. Add a <strong>Neural Layer</strong> first (this recognizes patterns)<br/>
        2. Add an <strong>Activation Function</strong> (this helps it remember)<br/>
        3. Draw shapes to teach your AI!
      </div>
      
      <div className="components-grid">
        {components.map((component, index) => (
          <motion.div
            key={component.id}
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: index * 0.1 }}
            className={`component-item ${disabled ? 'disabled' : ''}`}
            onClick={() => handleAddComponent(component)}
            whileHover={disabled ? {} : { 
              scale: 1.02,
              boxShadow: '0 8px 25px rgba(59, 130, 246, 0.3)'
            }}
            whileTap={disabled ? {} : { scale: 0.98 }}
          >
            <div className="component-header">
              <div className="component-icon">
                {getComponentIcon(component.icon)}
              </div>
              <div className="component-name">
                {component.name}
              </div>
            </div>
            
            <div className="component-description">
              {component.description}
            </div>
            
            {component.educational_note && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: 'auto' }}
                style={{
                  marginTop: '0.75rem',
                  padding: '0.5rem',
                  background: 'rgba(34, 197, 94, 0.1)',
                  borderRadius: '4px',
                  border: '1px solid rgba(34, 197, 94, 0.2)',
                  fontSize: '0.8rem',
                  color: '#86efac',
                  lineHeight: 1.3
                }}
              >
                💡 {component.educational_note}
              </motion.div>
            )}
            
            {!disabled && (
              <motion.div
                className="add-indicator"
                initial={{ opacity: 0 }}
                whileHover={{ opacity: 1 }}
                style={{
                  position: 'absolute',
                  top: '0.5rem',
                  right: '0.5rem',
                  background: 'rgba(34, 197, 94, 0.8)',
                  borderRadius: '50%',
                  width: '24px',
                  height: '24px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontSize: '0.8rem'
                }}
              >
                +
              </motion.div>
            )}
          </motion.div>
        ))}
      </div>
    </div>
  );
};

export default ComponentLibrary;