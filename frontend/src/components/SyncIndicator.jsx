import React, { useState, useEffect } from 'react'
import { syncManager } from '../utils/syncManager'
import '../styles/SyncIndicator.css'

export const SyncIndicator = () => {
  const [syncStatus, setSyncStatus] = useState('synced')
  const [pendingCount, setPendingCount] = useState(0)
  const [lastSync, setLastSync] = useState(null)

  useEffect(() => {
    const interval = setInterval(() => {
      const pending = syncManager.getPendingChangesCount()
      const isSyncing = syncManager.getIsSyncing()

      setPendingCount(pending)

      if (isSyncing) {
        setSyncStatus('syncing')
      } else if (pending > 0) {
        setSyncStatus('pending')
      } else {
        setSyncStatus('synced')
      }

      if (syncManager.getLastSyncTime()) {
        setLastSync(new Date(syncManager.getLastSyncTime()).toLocaleTimeString())
      }
    }, 500)

    return () => clearInterval(interval)
  }, [])

  return (
    <div className={`sync-indicator sync-${syncStatus}`}>
      <div className="sync-dot" />
      <span className="sync-text">
        {syncStatus === 'syncing' && '⟳ Syncing...'}
        {syncStatus === 'pending' && `✎ ${pendingCount} pending`}
        {syncStatus === 'synced' && '✓ Synced'}
      </span>
      {lastSync && <span className="sync-time">{lastSync}</span>}
    </div>
  )
}
