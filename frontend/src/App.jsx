import { useState, useEffect, useRef } from 'react'
import './index.css'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function App() {
  const [notes, setNotes] = useState([])
  const [selectedNoteId, setSelectedNoteId] = useState(null)
  const [isSyncing, setIsSyncing] = useState(false)
  const autoSaveTimerRef = useRef(null)

  const selectedNote = notes.find(n => n.id === selectedNoteId)

  // Load notes from backend on mount
  useEffect(() => {
    fetchNotes()
  }, [])

  // Auto-sync every 30 seconds
  useEffect(() => {
    const syncInterval = setInterval(syncNotes, 30000)
    return () => clearInterval(syncInterval)
  }, [notes])

  const fetchNotes = async () => {
    try {
      const response = await fetch(`${API_URL}/notes/`)
      if (response.ok) {
        const data = await response.json()
        setNotes(data)
        if (data.length > 0 && !selectedNoteId) {
          setSelectedNoteId(data[0].id)
        }
      }
    } catch (error) {
      console.error('Failed to fetch notes:', error)
    }
  }

  const syncNotes = async () => {
    if (notes.length === 0) return
    setIsSyncing(true)
    try {
      for (const note of notes) {
        await fetch(`${API_URL}/notes/${note.id}`, {
          method: 'PUT',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({
            title: note.title,
            content: note.content,
            pinned: note.pinned
          })
        })
      }
    } catch (error) {
      console.error('Sync failed:', error)
    } finally {
      setIsSyncing(false)
    }
  }

  const createNote = async () => {
    try {
      const response = await fetch(`${API_URL}/notes/`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          title: 'Untitled Note',
          content: '',
          pinned: false
        })
      })
      if (response.ok) {
        const newNote = await response.json()
        setNotes([newNote, ...notes])
        setSelectedNoteId(newNote.id)
      }
    } catch (error) {
      console.error('Failed to create note:', error)
    }
  }

  const deleteNote = async (noteId) => {
    if (!confirm('Delete this note?')) return
    try {
      await fetch(`${API_URL}/notes/${noteId}`, { method: 'DELETE' })
      setNotes(notes.filter(n => n.id !== noteId))
      if (selectedNoteId === noteId) {
        setSelectedNoteId(notes.length > 1 ? notes[0].id : null)
      }
    } catch (error) {
      console.error('Failed to delete note:', error)
    }
  }

  const updateNote = (field, value) => {
    setNotes(notes.map(n =>
      n.id === selectedNoteId ? { ...n, [field]: value } : n
    ))

    // Debounced auto-save
    if (autoSaveTimerRef.current) {
      clearTimeout(autoSaveTimerRef.current)
    }
    autoSaveTimerRef.current = setTimeout(syncNotes, 1000)
  }

  const togglePin = () => {
    updateNote('pinned', !selectedNote.pinned)
  }

  const formatDate = (dateString) => {
    const date = new Date(dateString)
    return date.toLocaleDateString('en-US', {
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <div className="app-container">
      <div className="header">
        <h1>✧ QUICK NOTES ✧</h1>
      </div>

      <div className="content">
        <div className="notes-list">
          <h2>Notes ({notes.length})</h2>
          {notes.length === 0 ? (
            <div style={{ textAlign: 'center', color: '#999', fontSize: '11px', marginTop: '16px' }}>
              No notes yet. Create one!
            </div>
          ) : (
            notes.map(note => (
              <div
                key={note.id}
                className={`note-item ${selectedNoteId === note.id ? 'active' : ''} ${note.pinned ? 'pinned' : ''}`}
                onClick={() => setSelectedNoteId(note.id)}
              >
                {note.pinned && <span style={{ marginRight: '4px' }}>📌</span>}
                <div className="note-item-title">{note.title}</div>
                <div className="note-item-preview">{note.content || '(empty)'}</div>
                <div className="note-item-meta">{formatDate(note.updated_at)}</div>
              </div>
            ))
          )}
        </div>

        <div className={`editor ${!selectedNote ? 'empty' : ''}`}>
          {!selectedNote ? (
            <div className="editor-empty-state">
              <h2>No Note Selected</h2>
              <p>Create or select a note to start writing</p>
            </div>
          ) : (
            <>
              <div className="editor-header">
                <input
                  type="text"
                  className="editor-title-input"
                  value={selectedNote.title}
                  onChange={(e) => updateNote('title', e.target.value)}
                  placeholder="Note title..."
                />
                <div className="editor-actions">
                  <button
                    className={`icon-btn ${selectedNote.pinned ? 'active' : ''}`}
                    onClick={togglePin}
                    title="Pin note"
                  >
                    📌
                  </button>
                  <button
                    className="icon-btn"
                    onClick={() => deleteNote(selectedNote.id)}
                    title="Delete note"
                  >
                    🗑️
                  </button>
                  <div style={{ fontSize: '10px', color: isSyncing ? '#D46B8B' : '#999', paddingRight: '8px', display: 'flex', alignItems: 'center' }}>
                    {isSyncing ? '💾' : '✓'}
                  </div>
                </div>
              </div>
              <div className="editor-content">
                <textarea
                  className="editor-textarea"
                  value={selectedNote.content}
                  onChange={(e) => updateNote('content', e.target.value)}
                  placeholder="Start typing..."
                />
              </div>
              <div className="editor-meta">
                Updated {formatDate(selectedNote.updated_at)}
              </div>
            </>
          )}
        </div>
      </div>

      <button className="fab" onClick={createNote} title="New note">
        +
      </button>
    </div>
  )
}

export default App
