import React, { useRef, useEffect, useState } from 'react';
import { motion } from 'framer-motion';
import { Brush, RotateCcw, Save } from 'lucide-react';

const DrawingCanvas = ({ onDrawingComplete, disabled, drawings }) => {
  const canvasRef = useRef(null);
  const [isDrawing, setIsDrawing] = useState(false);
  const [currentPath, setCurrentPath] = useState([]);
  const [selectedShape, setSelectedShape] = useState('circle');
  const [canvasSize] = useState({ width: 300, height: 300 });

  useEffect(() => {
    const canvas = canvasRef.current;
    if (!canvas) return;

    const ctx = canvas.getContext('2d');
    ctx.lineCap = 'round';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#1e40af';
    
    // Set canvas size
    canvas.width = canvasSize.width;
    canvas.height = canvasSize.height;
    
    // Clear canvas
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
  }, [canvasSize]);

  const getMousePos = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    return {
      x: (e.clientX - rect.left) * scaleX,
      y: (e.clientY - rect.top) * scaleY
    };
  };

  const getTouchPos = (e) => {
    const canvas = canvasRef.current;
    const rect = canvas.getBoundingClientRect();
    const scaleX = canvas.width / rect.width;
    const scaleY = canvas.height / rect.height;
    
    return {
      x: (e.touches[0].clientX - rect.left) * scaleX,
      y: (e.touches[0].clientY - rect.top) * scaleY
    };
  };

  const startDrawing = (e) => {
    if (disabled) return;
    
    e.preventDefault();
    setIsDrawing(true);
    
    const pos = e.touches ? getTouchPos(e) : getMousePos(e);
    setCurrentPath([pos]);
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.beginPath();
    ctx.moveTo(pos.x, pos.y);
  };

  const draw = (e) => {
    if (!isDrawing || disabled) return;
    
    e.preventDefault();
    const pos = e.touches ? getTouchPos(e) : getMousePos(e);
    
    setCurrentPath(prev => [...prev, pos]);
    
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.lineTo(pos.x, pos.y);
    ctx.stroke();
  };

  const stopDrawing = (e) => {
    if (!isDrawing || disabled) return;
    
    e.preventDefault();
    setIsDrawing(false);
    
    if (currentPath.length > 5) { // Minimum points for a valid drawing
      onDrawingComplete(currentPath, selectedShape);
    }
    
    setCurrentPath([]);
  };

  const clearCanvas = () => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext('2d');
    ctx.fillStyle = '#f8fafc';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    setCurrentPath([]);
  };

  const shapes = [
    { id: 'circle', name: 'Circle', emoji: '⭕' },
    { id: 'square', name: 'Square', emoji: '⬜' },
    { id: 'triangle', name: 'Triangle', emoji: '🔺' }
  ];

  return (
    <div className="drawing-canvas">
      <h3>
        <Brush size={20} />
        Draw Training Examples
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
        ✏️ <strong>Draw by Hand:</strong> Use your mouse or finger to draw shapes on the canvas below. Your AI will learn from your drawings!
      </div>
      
      <div className="drawing-controls">
        <div className="shape-selector">
          {shapes.map(shape => (
            <button
              key={shape.id}
              className={`shape-button ${selectedShape === shape.id ? 'active' : ''}`}
              onClick={() => setSelectedShape(shape.id)}
              disabled={disabled}
            >
              {shape.emoji} {shape.name}
            </button>
          ))}
        </div>
      </div>

      <motion.div 
        className="canvas-container"
        whileHover={{ scale: disabled ? 1 : 1.02 }}
        transition={{ duration: 0.2 }}
      >
        <canvas
          ref={canvasRef}
          onMouseDown={startDrawing}
          onMouseMove={draw}
          onMouseUp={stopDrawing}
          onMouseLeave={stopDrawing}
          onTouchStart={startDrawing}
          onTouchMove={draw}
          onTouchEnd={stopDrawing}
          style={{
            width: '100%',
            height: 'auto',
            cursor: disabled ? 'not-allowed' : 'crosshair',
            opacity: disabled ? 0.6 : 1,
            transition: 'opacity 0.3s ease'
          }}
        />
      </motion.div>

      <div className="canvas-actions">
        <button 
          onClick={clearCanvas}
          className="small-button"
          disabled={disabled}
        >
          <RotateCcw size={14} />
          Clear Canvas
        </button>
        
        <div className="drawing-hint">
          <span style={{ color: '#60a5fa', fontSize: '0.85rem' }}>
            👆 Draw a {selectedShape} above, then it will be saved automatically!
          </span>
        </div>
      </div>

      {drawings.length > 0 && (
        <motion.div
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          className="drawings-summary"
          style={{
            marginTop: '1rem',
            padding: '1rem',
            background: 'rgba(59, 130, 246, 0.1)',
            borderRadius: '8px',
            border: '1px solid rgba(59, 130, 246, 0.2)'
          }}
        >
          <div style={{ color: '#60a5fa', fontSize: '0.9rem', marginBottom: '0.5rem' }}>
            ✅ Saved Training Examples: {drawings.length}
          </div>
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap' }}>
            {drawings.map(drawing => (
              <span
                key={drawing.id}
                style={{
                  background: 'rgba(34, 197, 94, 0.2)',
                  padding: '0.25rem 0.5rem',
                  borderRadius: '4px',
                  fontSize: '0.8rem',
                  color: '#86efac'
                }}
              >
                {shapes.find(s => s.id === drawing.label)?.emoji} {drawing.label}
              </span>
            ))}
          </div>
        </motion.div>
      )}
    </div>
  );
};

export default DrawingCanvas;