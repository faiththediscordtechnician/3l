import { useEffect, useRef } from 'react'

export const useAutosave = (callback, delay = 3000) => {
  const timeoutRef = useRef(null)
  const isSavingRef = useRef(false)

  useEffect(() => {
    return () => {
      if (timeoutRef.current) {
        clearTimeout(timeoutRef.current)
      }
    }
  }, [])

  const autosave = (data) => {
    if (timeoutRef.current) {
      clearTimeout(timeoutRef.current)
    }

    timeoutRef.current = setTimeout(async () => {
      if (isSavingRef.current) return

      try {
        isSavingRef.current = true
        await callback(data)
      } catch (error) {
        console.error('Autosave failed:', error)
      } finally {
        isSavingRef.current = false
      }
    }, delay)
  }

  return { autosave, cancel: () => clearTimeout(timeoutRef.current) }
}
