import React, { useState } from 'react'
import { Window } from './Window'

export const WindowManager = () => {
  const [windows, setWindows] = useState([
    { id: 'dashboard', title: 'DASHBOARD', content: 'Dashboard content' },
  ])
  const [focusedWindow, setFocusedWindow] = useState('dashboard')
  const [nextZIndex, setNextZIndex] = useState(100)

  const openWindow = (id, title, content) => {
    if (!windows.find(w => w.id === id)) {
      setWindows([...windows, { id, title, content }])
    }
    focusWindow(id)
  }

  const closeWindow = (id) => {
    if (windows.length > 1) {
      setWindows(windows.filter(w => w.id !== id))
      if (focusedWindow === id) {
        setFocusedWindow(windows[0]?.id)
      }
    }
  }

  const focusWindow = (id) => {
    setFocusedWindow(id)
    setNextZIndex(nextZIndex + 1)
  }

  const getZIndex = (windowId) => {
    return focusedWindow === windowId ? nextZIndex : nextZIndex - 1
  }

  return (
    <div className="window-manager">
      {windows.map((window) => (
        <Window
          key={window.id}
          id={window.id}
          title={window.title}
          onClose={closeWindow}
          onFocus={focusWindow}
          zIndex={getZIndex(window.id)}
        >
          {window.content}
        </Window>
      ))}
    </div>
  )
}
