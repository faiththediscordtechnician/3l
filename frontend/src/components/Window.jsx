import React, { useRef, useState } from 'react'
import '../styles/Window.css'

export const Window = ({ id, title, children, onClose, onFocus, zIndex, minWidth = 300, minHeight = 200 }) => {
  const windowRef = useRef(null)
  const headerRef = useRef(null)
  const [isBeingDragged, setIsBeingDragged] = useState(false)
  const [offset, setOffset] = useState({ x: 0, y: 0 })
  const [pos, setPos] = useState({ x: 100 + Math.random() * 200, y: 100 + Math.random() * 200 })
  const [size, setSize] = useState({ width: minWidth, height: minHeight })

  const handleMouseDown = (e) => {
    if (headerRef.current && headerRef.current.contains(e.target)) {
      setIsBeingDragged(true)
      setOffset({
        x: e.clientX - pos.x,
        y: e.clientY - pos.y,
      })
      onFocus && onFocus(id)
    }
  }

  const handleMouseMove = (e) => {
    if (isBeingDragged) {
      setPos({
        x: e.clientX - offset.x,
        y: e.clientY - offset.y,
      })
    }
  }

  const handleMouseUp = () => {
    setIsBeingDragged(false)
  }

  React.useEffect(() => {
    if (isBeingDragged) {
      document.addEventListener('mousemove', handleMouseMove)
      document.addEventListener('mouseup', handleMouseUp)
      return () => {
        document.removeEventListener('mousemove', handleMouseMove)
        document.removeEventListener('mouseup', handleMouseUp)
      }
    }
  }, [isBeingDragged, offset])

  return (
    <div
      ref={windowRef}
      className="window"
      style={{
        position: 'absolute',
        left: `${pos.x}px`,
        top: `${pos.y}px`,
        width: `${size.width}px`,
        minHeight: `${size.height}px`,
        zIndex: zIndex,
      }}
    >
      <div
        ref={headerRef}
        className="window-header"
        onMouseDown={handleMouseDown}
        style={{ cursor: isBeingDragged ? 'grabbing' : 'grab' }}
      >
        <span className="window-title">{title}</span>
        <button
          className="window-close-btn"
          onClick={() => onClose && onClose(id)}
          title="Close"
        >
          ×
        </button>
      </div>
      <div className="window-content">
        {children}
      </div>
    </div>
  )
}
