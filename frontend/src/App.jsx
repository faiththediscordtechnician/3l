import { useState, useEffect } from 'react'
import { auth, setAuthToken, getAuthToken, setup } from './utils/api'
import { syncManager } from './utils/syncManager'
import { Window } from './components/Window'
import { Mascot } from './components/Mascot'
import { SyncIndicator } from './components/SyncIndicator'
import { SetupWizard } from './components/SetupWizard'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(!!getAuthToken())
  const [username, setUsername] = useState('marie')
  const [password, setPassword] = useState('jdorbust')
  const [error, setError] = useState('')
  const [loading, setLoading] = useState(false)
  const [mascotState, setMascotState] = useState('idle')
  const [windows, setWindows] = useState({
    dashboard: { open: true, title: '3L ACADEMIC HUB' },
  })
  const [showSetup, setShowSetup] = useState(false)
  const [setupChecked, setSetupChecked] = useState(false)

  useEffect(() => {
    if (isLoggedIn) {
      syncManager.startAutoSync(5000)
      checkSetupStatus()
      return () => syncManager.stopAutoSync()
    }
  }, [isLoggedIn])

  const checkSetupStatus = async () => {
    try {
      const status = await setup.getStatus()
      if (!status.is_setup) {
        setShowSetup(true)
      }
      setSetupChecked(true)
    } catch (error) {
      console.error('Failed to check setup:', error)
      setSetupChecked(true)
    }
  }

  const handleLogin = async (e) => {
    e.preventDefault()
    setError('')
    setLoading(true)
    setMascotState('concentrating')

    try {
      const response = await auth.login(username, password)
      setAuthToken(response.access_token)
      setIsLoggedIn(true)
      setMascotState('happy')
      setTimeout(() => setMascotState('idle'), 600)
    } catch (err) {
      setError('Login failed. Please check your credentials.')
      setMascotState('idle')
    } finally {
      setLoading(false)
    }
  }

  const handleLogout = () => {
    setAuthToken(null)
    setIsLoggedIn(false)
    setUsername('')
    setPassword('')
    setWindows({})
    setMascotState('idle')
  }

  const toggleWindow = (windowId) => {
    setWindows((prev) => ({
      ...prev,
      [windowId]: {
        ...prev[windowId],
        open: !prev[windowId]?.open,
      },
    }))
  }

  const closeWindow = (windowId) => {
    if (windowId !== 'dashboard') {
      setWindows((prev) => ({
        ...prev,
        [windowId]: { ...prev[windowId], open: false },
      }))
    }
  }

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <div className="login-window window" style={{ animation: 'bounce 0.6s ease-out' }}>
          <div className="window-header">
            <span>3L ACADEMIC HUB</span>
            <div style={{ width: '20px' }} />
          </div>
          <div className="window-content login-form">
            <div className="mascot-container">
              <Mascot state={mascotState} />
            </div>
            <h1>Welcome</h1>
            <p className="login-subtitle">Login to your personal academic hub</p>

            <form onSubmit={handleLogin}>
              {error && <div className="error-message">{error}</div>}

              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username"
                  disabled={loading}
                />
              </div>

              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password"
                  disabled={loading}
                />
              </div>

              <button type="submit" disabled={loading}>
                {loading ? 'LOGGING IN...' : 'LOGIN'}
              </button>
            </form>

            <p className="login-hint">✧ Press START! Try: marie / jdorbust ✧</p>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      <div className="header-bar">
        <div className="header-left">
          <div className="mascot-mini">
            <Mascot state={mascotState} />
          </div>
          <h1 className="app-title">3L ACADEMIC HUB</h1>
        </div>
        <div className="header-center">
          <SyncIndicator />
        </div>
        <div className="header-right">
          <button className="logout-btn" onClick={handleLogout}>LOGOUT</button>
        </div>
      </div>

      <div className="windows-container">
        {showSetup && setupChecked && (
          <SetupWizard onComplete={() => setShowSetup(false)} />
        )}

        {windows.dashboard?.open && (
          <Window
            id="dashboard"
            title="DASHBOARD"
            onClose={() => {}}
            zIndex={100}
          >
            <div className="dashboard-content">
              <h2>Your Classes</h2>
              <p>Classes section coming soon...</p>

              <div className="quick-actions">
                <button className="action-btn">NEW CLASS</button>
                <button className="action-btn">NEW READING</button>
                <button className="action-btn">NEW TODO</button>
              </div>

              <h3>Recent Activity</h3>
              <p>No activity yet. Start by creating a class!</p>
            </div>
          </Window>
        )}
      </div>
    </div>
  )
}

export default App
