import React, { useState } from 'react'
import { setup } from '../utils/api'
import { Window } from './Window'
import '../styles/SetupWizard.css'

export const SetupWizard = ({ onComplete }) => {
  const [step, setStep] = useState('welcome')
  const [loading, setLoading] = useState(false)
  const [createdClasses, setCreatedClasses] = useState([])

  const handleSeedClasses = async () => {
    setLoading(true)
    try {
      const result = await setup.seedClasses()
      setCreatedClasses(result.classes)
      setStep('complete')
    } catch (error) {
      console.error('Failed to seed classes:', error)
      alert('Failed to create classes. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Window id="setup" title="WELCOME TO 3L HUB" onClose={onComplete} zIndex={200}>
      <div className="setup-wizard">
        {step === 'welcome' && (
          <div className="setup-step">
            <h2>Welcome to Your 3L Academic Hub! 📚</h2>
            <p>Let's get your course schedule set up so you can start managing your readings and notes.</p>

            <div className="setup-info">
              <h3>Your 5 Courses:</h3>
              <ul>
                <li><strong>CML 2320</strong> - Mediation Theory and Practice (Emilia Péch)</li>
                <li><strong>CML 3233</strong> - Labour Law I (Ravi A. Malhotra)</li>
                <li><strong>CML 4104</strong> - Studies in Public Law (Andres Drew)</li>
                <li><strong>CML 4108</strong> - Studies in International Law (Aram Kerkonian)</li>
                <li><strong>CML 4150</strong> - Globalization and Law (Errol Mendes)</li>
              </ul>
            </div>

            <button
              className="setup-btn setup-btn-primary"
              onClick={handleSeedClasses}
              disabled={loading}
            >
              {loading ? 'Creating Classes...' : 'Create My Courses'}
            </button>
          </div>
        )}

        {step === 'complete' && (
          <div className="setup-step">
            <h2>✨ Your Courses Are Ready!</h2>
            <p>Successfully created {createdClasses.length} courses:</p>

            <div className="created-classes">
              {createdClasses.map((cls) => (
                <div key={cls.id} className="class-badge">
                  <strong>{cls.code}</strong>
                  <p>{cls.name}</p>
                  <small>{cls.instructor}</small>
                </div>
              ))}
            </div>

            <p className="setup-hint">
              You can now start adding readings, notes, and todos for each class!
              Click on a class to get started. 🎓
            </p>

            <button
              className="setup-btn setup-btn-primary"
              onClick={onComplete}
            >
              Start Using the Hub
            </button>
          </div>
        )}
      </div>
    </Window>
  )
}
