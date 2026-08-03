import React, { useState, useEffect } from 'react'
import { Window } from './Window'
import { classes } from '../utils/api'
import '../styles/ClassesWindow.css'

export const ClassesWindow = ({ onClose, onSelectClass }) => {
  const [classList, setClassList] = useState([])
  const [loading, setLoading] = useState(true)
  const [newClassName, setNewClassName] = useState('')
  const [newClassCode, setNewClassCode] = useState('')

  useEffect(() => {
    loadClasses()
  }, [])

  const loadClasses = async () => {
    try {
      setLoading(true)
      const data = await classes.list()
      setClassList(data)
    } catch (error) {
      console.error('Failed to load classes:', error)
    } finally {
      setLoading(false)
    }
  }

  const handleAddClass = async (e) => {
    e.preventDefault()
    if (!newClassName.trim()) return

    try {
      const newClass = await classes.create({
        name: newClassName,
        code: newClassCode,
        color: 'powder-petal',
      })
      setClassList([...classList, newClass])
      setNewClassName('')
      setNewClassCode('')
    } catch (error) {
      console.error('Failed to create class:', error)
    }
  }

  return (
    <Window
      id="classes"
      title="CLASSES"
      onClose={onClose}
      zIndex={100}
    >
      <div className="classes-window">
        <div className="classes-list">
          {loading ? (
            <p>Loading classes...</p>
          ) : classList.length === 0 ? (
            <p>No classes yet. Create one to get started!</p>
          ) : (
            classList.map((cls) => (
              <div
                key={cls.id}
                className="class-item"
                onClick={() => onSelectClass(cls)}
              >
                <h3>{cls.name}</h3>
                {cls.code && <p>{cls.code}</p>}
              </div>
            ))
          )}
        </div>

        <div className="add-class-form">
          <h4>NEW CLASS</h4>
          <form onSubmit={handleAddClass}>
            <input
              type="text"
              placeholder="Class name"
              value={newClassName}
              onChange={(e) => setNewClassName(e.target.value)}
            />
            <input
              type="text"
              placeholder="Course code (optional)"
              value={newClassCode}
              onChange={(e) => setNewClassCode(e.target.value)}
            />
            <button type="submit">ADD</button>
          </form>
        </div>
      </div>
    </Window>
  )
}
