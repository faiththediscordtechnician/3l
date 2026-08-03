import { notes, readings, todos, classes as classesApi } from './api'

class SyncManager {
  constructor() {
    this.pendingChanges = []
    this.isSyncing = false
    this.lastSyncTime = null
    this.syncInterval = null
  }

  startAutoSync(intervalMs = 5000) {
    this.syncInterval = setInterval(() => {
      this.syncAll()
    }, intervalMs)
  }

  stopAutoSync() {
    if (this.syncInterval) {
      clearInterval(this.syncInterval)
      this.syncInterval = null
    }
  }

  addPendingChange(type, id, data) {
    const existingIndex = this.pendingChanges.findIndex(
      (c) => c.type === type && c.id === id
    )

    if (existingIndex >= 0) {
      this.pendingChanges[existingIndex] = { type, id, data, timestamp: Date.now() }
    } else {
      this.pendingChanges.push({ type, id, data, timestamp: Date.now() })
    }
  }

  async saveNote(noteId, noteData) {
    this.addPendingChange('note', noteId, noteData)
    try {
      const result = await notes.update(noteId, noteData)
      this.removePendingChange('note', noteId)
      this.lastSyncTime = Date.now()
      return result
    } catch (error) {
      console.error('Note save failed:', error)
      throw error
    }
  }

  async saveReading(readingId, readingData) {
    this.addPendingChange('reading', readingId, readingData)
    try {
      const result = await readings.update(readingId, readingData)
      this.removePendingChange('reading', readingId)
      this.lastSyncTime = Date.now()
      return result
    } catch (error) {
      console.error('Reading save failed:', error)
      throw error
    }
  }

  async saveTodo(todoId, todoData) {
    this.addPendingChange('todo', todoId, todoData)
    try {
      const result = await todos.update(todoId, todoData)
      this.removePendingChange('todo', todoId)
      this.lastSyncTime = Date.now()
      return result
    } catch (error) {
      console.error('Todo save failed:', error)
      throw error
    }
  }

  async syncAll() {
    if (this.isSyncing || this.pendingChanges.length === 0) {
      return
    }

    this.isSyncing = true
    const changesToSync = [...this.pendingChanges]

    try {
      for (const change of changesToSync) {
        try {
          switch (change.type) {
            case 'note':
              await notes.update(change.id, change.data)
              break
            case 'reading':
              await readings.update(change.id, change.data)
              break
            case 'todo':
              await todos.update(change.id, change.data)
              break
            default:
              console.warn(`Unknown sync type: ${change.type}`)
          }
          this.removePendingChange(change.type, change.id)
        } catch (error) {
          console.error(`Failed to sync ${change.type} ${change.id}:`, error)
        }
      }
      this.lastSyncTime = Date.now()
    } finally {
      this.isSyncing = false
    }
  }

  removePendingChange(type, id) {
    this.pendingChanges = this.pendingChanges.filter(
      (c) => !(c.type === type && c.id === id)
    )
  }

  getPendingChangesCount() {
    return this.pendingChanges.length
  }

  getLastSyncTime() {
    return this.lastSyncTime
  }

  getIsSyncing() {
    return this.isSyncing
  }
}

export const syncManager = new SyncManager()
