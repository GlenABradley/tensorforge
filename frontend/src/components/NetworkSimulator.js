import React, { useState, useEffect } from 'react';
import { motion } from 'framer-motion';
import { Cpu, ArrowRight, Zap, Database, TrendingUp } from 'lucide-react';

const NetworkSimulator = ({ components, disabled, simulationData }) => {
  const [dataFlow, setDataFlow] = useState([]);
  const [currentStep, setCurrentStep] = useState(0);
  const [isProcessing, setIsProcessing] = useState(false);

  // Sample input data for the network
  const sampleInputs = [
    { id: 1, data: [0.8, 0.2, 0.9, 0.1], label: "Pattern A" },
    { id: 2, data: [0.3, 0.7, 0.4, 0.6], label: "Pattern B" },
    { id: 3, data: [0.9, 0.1, 0.8, 0.3], label: "Pattern C" }
  ];

  const [selectedInput, setSelectedInput] = useState(sampleInputs[0]);

  useEffect(() => {
    if (components.length > 0) {
      // Simulate data flow through the network
      const flow = components.map((comp, index) => ({
        layer: index + 1,
        name: comp.name,
        type: comp.type,
        inputSize: index === 0 ? 4 : Math.max(2, 8 - index * 2),
        outputSize: Math.max(2, 8 - index * 2),
        activation: Math.random() * 0.8 + 0.2
      }));
      setDataFlow(flow);
    }
  }, [components]);

  const processData = () => {
    setIsProcessing(true);
    setCurrentStep(0);
    
    // Animate through each layer
    const animateStep = (step) => {
      if (step < dataFlow.length) {
        setCurrentStep(step);
        setTimeout(() => animateStep(step + 1), 800);
      } else {
        setIsProcessing(false);
      }
    };
    
    animateStep(0);
  };

  const getLayerColor = (type) => {
    switch (type) {
      case 'layer': return '#3b82f6';
      case 'function': return '#8b5cf6';
      case 'regularization': return '#f59e0b';
      default: return '#6b7280';
    }
  };

  if (components.length === 0) {
    return (
      <div className="network-simulator">
        <h3>
          <Cpu size={20} />
          Network Simulator
        </h3>
        
        <div style={{
          padding: '2rem',
          textAlign: 'center',
          background: 'rgba(59, 130, 246, 0.1)',
          borderRadius: '8px',
          border: '1px solid rgba(59, 130, 246, 0.2)',
          marginTop: '1rem'
        }}>
          <Database size={48} className="text-blue-400" style={{ marginBottom: '1rem' }} />
          <h4 style={{ color: '#60a5fa', marginBottom: '0.5rem' }}>Build Your Network First!</h4>
          <p style={{ color: '#cbd5e1', fontSize: '0.9rem' }}>
            Add components from the library to see how data flows through your neural network.
          </p>
        </div>
      </div>
    );
  }

  return (
    <div className="network-simulator">
      <h3>
        <Cpu size={20} />
        Network Simulator
      </h3>
      
      <div style={{
        marginBottom: '1rem',
        padding: '0.75rem',
        background: 'rgba(59, 130, 246, 0.1)',
        borderRadius: '6px',
        border: '1px solid rgba(59, 130, 246, 0.2)',
        fontSize: '0.85rem',
        color: '#60a5fa',
        lineHeight: 1.4
      }}>
        🔄 <strong>Network Processing:</strong> Watch how your {components.length}-layer network transforms input data through each layer!
      </div>
      
      {/* Success Criteria Explanation */}
      <div style={{
        marginBottom: '1rem',
        padding: '0.75rem',
        background: 'rgba(245, 158, 11, 0.1)',
        borderRadius: '6px',
        border: '1px solid rgba(245, 158, 11, 0.2)',
        fontSize: '0.85rem',
        color: '#fbbf24',
        lineHeight: 1.4
      }}>
        🎯 <strong>To Pass Level 2:</strong> Build a network with 85%+ efficiency by including:
        <br />• Neural Layer (essential for processing)
        <br />• Dense Layer(s) (for deeper learning)
        <br />• Activation Function (for non-linearity)
        <br />• Optional: Dropout (prevents overfitting)
      </div>

      {/* Input Data Selection */}
      <div style={{ marginBottom: '1rem' }}>
        <h4 style={{ color: '#e2e8f0', fontSize: '0.9rem', marginBottom: '0.5rem' }}>Input Data:</h4>
        <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1rem' }}>
          {sampleInputs.map((input) => (
            <button
              key={input.id}
              onClick={() => setSelectedInput(input)}
              disabled={disabled || isProcessing}
              style={{
                padding: '0.5rem 0.75rem',
                borderRadius: '4px',
                border: selectedInput.id === input.id ? '2px solid #3b82f6' : '1px solid #374151',
                background: selectedInput.id === input.id ? 'rgba(59, 130, 246, 0.2)' : 'rgba(55, 65, 81, 0.5)',
                color: selectedInput.id === input.id ? '#60a5fa' : '#cbd5e1',
                fontSize: '0.8rem',
                cursor: disabled || isProcessing ? 'not-allowed' : 'pointer',
                opacity: disabled || isProcessing ? 0.5 : 1
              }}
            >
              {input.label}
            </button>
          ))}
        </div>
        
        <div style={{
          padding: '0.75rem',
          background: 'rgba(17, 24, 39, 0.5)',
          borderRadius: '4px',
          border: '1px solid #374151',
          fontSize: '0.8rem',
          color: '#9ca3af'
        }}>
          <strong>{selectedInput.label}:</strong> [{selectedInput.data.map(d => d.toFixed(1)).join(', ')}]
        </div>
      </div>

      {/* Network Visualization */}
      <div style={{
        background: 'rgba(17, 24, 39, 0.5)',
        borderRadius: '8px',
        border: '1px solid #374151',
        padding: '1rem',
        marginBottom: '1rem'
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '1rem' }}>
          <h4 style={{ color: '#e2e8f0', fontSize: '0.9rem', margin: 0 }}>Network Architecture:</h4>
          <span style={{ color: '#6b7280', fontSize: '0.8rem' }}>
            {dataFlow.length} layers
          </span>
        </div>
        
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', overflowX: 'auto', paddingBottom: '0.5rem' }}>
          {/* Input */}
          <div style={{
            minWidth: '80px',
            padding: '0.75rem 0.5rem',
            background: 'rgba(34, 197, 94, 0.2)',
            borderRadius: '6px',
            border: '1px solid rgba(34, 197, 94, 0.3)',
            textAlign: 'center'
          }}>
            <div style={{ color: '#86efac', fontSize: '0.7rem', marginBottom: '0.25rem' }}>INPUT</div>
            <div style={{ color: '#10b981', fontSize: '0.8rem', fontWeight: 'bold' }}>
              {selectedInput.data.length}
            </div>
          </div>
          
          {dataFlow.map((layer, index) => (
            <React.Fragment key={layer.layer}>
              <ArrowRight size={16} style={{ color: '#6b7280' }} />
              <motion.div
                style={{
                  minWidth: '100px',
                  padding: '0.75rem 0.5rem',
                  background: currentStep >= index && isProcessing 
                    ? `rgba(${getLayerColor(layer.type).replace('#', '').match(/.{2}/g).map(x => parseInt(x, 16)).join(', ')}, 0.4)`
                    : 'rgba(55, 65, 81, 0.5)',
                  borderRadius: '6px',
                  border: currentStep >= index && isProcessing 
                    ? `2px solid ${getLayerColor(layer.type)}`
                    : '1px solid #374151',
                  textAlign: 'center'
                }}
                animate={currentStep >= index && isProcessing ? { scale: [1, 1.05, 1] } : {}}
                transition={{ duration: 0.3 }}
              >
                <div style={{ color: '#cbd5e1', fontSize: '0.7rem', marginBottom: '0.25rem' }}>
                  {layer.name.toUpperCase()}
                </div>
                <div style={{ color: '#e2e8f0', fontSize: '0.8rem', fontWeight: 'bold' }}>
                  {layer.outputSize}
                </div>
                {currentStep >= index && isProcessing && (
                  <motion.div
                    style={{
                      marginTop: '0.25rem',
                      fontSize: '0.7rem',
                      color: getLayerColor(layer.type)
                    }}
                    animate={{ opacity: [0.5, 1, 0.5] }}
                    transition={{ duration: 0.5, repeat: Infinity }}
                  >
                    Processing...
                  </motion.div>
                )}
              </motion.div>
            </React.Fragment>
          ))}
          
          <ArrowRight size={16} style={{ color: '#6b7280' }} />
          
          {/* Output */}
          <div style={{
            minWidth: '80px',
            padding: '0.75rem 0.5rem',
            background: currentStep >= dataFlow.length && isProcessing 
              ? 'rgba(245, 158, 11, 0.2)' 
              : 'rgba(55, 65, 81, 0.5)',
            borderRadius: '6px',
            border: currentStep >= dataFlow.length && isProcessing 
              ? '2px solid #f59e0b' 
              : '1px solid #374151',
            textAlign: 'center'
          }}>
            <div style={{ color: '#fbbf24', fontSize: '0.7rem', marginBottom: '0.25rem' }}>OUTPUT</div>
            <div style={{ color: '#f59e0b', fontSize: '0.8rem', fontWeight: 'bold' }}>
              {dataFlow.length > 0 ? dataFlow[dataFlow.length - 1].outputSize : 1}
            </div>
          </div>
        </div>
      </div>

      {/* Process Button */}
      <motion.button
        onClick={processData}
        disabled={disabled || isProcessing}
        style={{
          width: '100%',
          padding: '0.75rem',
          background: isProcessing 
            ? 'linear-gradient(135deg, #f59e0b, #d97706)'
            : 'linear-gradient(135deg, #3b82f6, #2563eb)',
          border: 'none',
          borderRadius: '6px',
          color: 'white',
          fontSize: '0.9rem',
          fontWeight: '600',
          cursor: disabled || isProcessing ? 'not-allowed' : 'pointer',
          opacity: disabled || isProcessing ? 0.7 : 1,
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          gap: '0.5rem'
        }}
        whileHover={!disabled && !isProcessing ? { scale: 1.02 } : {}}
        whileTap={!disabled && !isProcessing ? { scale: 0.98 } : {}}
      >
        {isProcessing ? (
          <>
            <motion.div
              animate={{ rotate: 360 }}
              transition={{ duration: 1, repeat: Infinity, ease: 'linear' }}
            >
              <TrendingUp size={16} />
            </motion.div>
            Processing Data...
          </>
        ) : (
          <>
            <Zap size={16} />
            Process Data Through Network
          </>
        )}
      </motion.button>

      {/* Processing Results */}
      {simulationData && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          style={{
            marginTop: '1rem',
            padding: '1rem',
            background: 'rgba(34, 197, 94, 0.1)',
            borderRadius: '8px',
            border: '1px solid rgba(34, 197, 94, 0.2)'
          }}
        >
          <h4 style={{ color: '#86efac', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            🎯 Processing Complete!
          </h4>
          <p style={{ color: '#cbd5e1', fontSize: '0.85rem', margin: 0 }}>
            Your network successfully processed the input data through {components.length} layers 
            with {simulationData.score ? `${Math.round(simulationData.score * 100)}%` : '90%'} efficiency.
          </p>
        </motion.div>
      )}
    </div>
  );
};

export default NetworkSimulator;