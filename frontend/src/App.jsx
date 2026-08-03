import { useState } from 'react'
import './App.css'

function App() {
  const [isLoggedIn, setIsLoggedIn] = useState(false)
  const [username, setUsername] = useState('')
  const [password, setPassword] = useState('')

  const handleLogin = (e) => {
    e.preventDefault()
    // TODO: Connect to backend auth
    setIsLoggedIn(true)
  }

  if (!isLoggedIn) {
    return (
      <div className="login-container">
        <div className="login-window window">
          <div className="window-header">
            <span>3L ACADEMIC HUB</span>
            <button className="window-close-btn">×</button>
          </div>
          <div className="window-content login-form">
            <h1>Welcome</h1>
            <form onSubmit={handleLogin}>
              <div className="form-group">
                <label>Username</label>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="Enter username"
                />
              </div>
              <div className="form-group">
                <label>Password</label>
                <input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Enter password"
                />
              </div>
              <button type="submit">LOGIN</button>
            </form>
          </div>
        </div>
      </div>
    )
  }

  return (
    <div className="app-container">
      <h1>3L Academic Hub - Dashboard</h1>
      <p>Coming soon...</p>
    </div>
  )
}

export default App
