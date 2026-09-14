import { useState, useEffect, useRef } from 'react'
import './index.css'

const API_URL = import.meta.env.VITE_API_URL || '/api'

function RichTextToolbar({ onBold, onItalic, onUnderline, onHighlight, onExportPDF }) {
  return (
    <div className="toolbar">
      <button className="toolbar-btn" onClick={onBold} title="Bold (Ctrl+B)">
        <strong>B</strong>
      </button>
      <button className="toolbar-btn" onClick={onItalic} title="Italic (Ctrl+I)">
        <em>I</em>
      </button>
      <button className="toolbar-btn" onClick={onUnderline} title="Underline (Ctrl+U)">
        <u>U</u>
      </button>
      <button className="toolbar-btn highlight-btn" onClick={onHighlight} title="Highlight">
        🎨
      </button>
      <div className="toolbar-separator"></div>
      <button className="toolbar-btn" onClick={onExportPDF} title="Export as PDF">
        📄 PDF
      </button>
    </div>
  )
}

function App() {
  const [notes, setNotes] = useState([])
  const [selectedNoteId, setSelectedNoteId] = useState(null)
  const [isSyncing, setIsSyncing] = useState(false)
  const autoSaveTimerRef = useRef(null)
  const editorRef = useRef(null)

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

  // Update editor content when selected note changes
  useEffect(() => {
    if (selectedNote && editorRef.current) {
      editorRef.current.innerHTML = selectedNote.content
    }
  }, [selectedNoteId])

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

  const handleEditorInput = () => {
    if (editorRef.current) {
      updateNote('content', editorRef.current.innerHTML)
    }
  }

  const applyFormat = (command, value = null) => {
    document.execCommand(command, false, value)
    editorRef.current?.focus()
  }

  const applyHighlight = () => {
    const selectedColor = prompt('Enter highlight color (hex or name):', '#FFFF00')
    if (selectedColor) {
      applyFormat('backColor', selectedColor)
    }
  }

  const exportPDF = () => {
    if (!selectedNote) return

    const element = document.createElement('div')
    element.innerHTML = `
      <h1 style="font-family: 'Press Start 2P', cursive; font-size: 20px; margin-bottom: 20px;">
        ${selectedNote.title}
      </h1>
      <div style="font-family: 'VT323', monospace; line-height: 1.6; white-space: pre-wrap;">
        ${selectedNote.content}
      </div>
      <p style="font-size: 10px; color: #999; margin-top: 20px;">
        Exported from Quick Notes on ${new Date().toLocaleDateString()}
      </p>
    `

    const opt = {
      margin: 10,
      filename: `${selectedNote.title}.pdf`,
      image: { type: 'jpeg', quality: 0.98 },
      html2canvas: { scale: 2 },
      jsPDF: { unit: 'mm', format: 'a4', orientation: 'portrait' }
    }

    import('html2pdf.js').then(module => {
      const html2pdf = module.default
      html2pdf().set(opt).from(element).save()
    })
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
                <div className="note-item-preview">
                  {selectedNote?.id === note.id ? note.content.replace(/<[^>]*>/g, '') : note.content.replace(/<[^>]*>/g, '') || '(empty)'}
                </div>
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
              <RichTextToolbar
                onBold={() => applyFormat('bold')}
                onItalic={() => applyFormat('italic')}
                onUnderline={() => applyFormat('underline')}
                onHighlight={applyHighlight}
                onExportPDF={exportPDF}
              />
              <div className="editor-content">
                <div
                  ref={editorRef}
                  className="editor-richtext"
                  contentEditable
                  onInput={handleEditorInput}
                  onBlur={handleEditorInput}
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
