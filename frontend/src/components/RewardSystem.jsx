import React, { useState } from 'react'
import '../styles/RewardSystem.css'

export const RewardSystem = ({ wordCount = 0, onMilestone }) => {
  const [milestones, setMilestones] = useState([])
  const [showCelebration, setShowCelebration] = useState(false)

  const getMilestones = () => {
    return [
      { words: 100, icon: '⭐', name: 'First Star' },
      { words: 500, icon: '🌟', name: 'Gold Star' },
      { words: 1000, icon: '✨', name: 'Platinum Star' },
      { words: 2500, icon: '💎', name: 'Diamond Achievement' },
      { words: 5000, icon: '👑', name: 'Legendary Scholar' },
    ]
  }

  const checkMilestones = (count) => {
    const newMilestones = getMilestones().filter(
      (m) => count >= m.words && !milestones.some((existing) => existing.words === m.words)
    )

    if (newMilestones.length > 0) {
      newMilestones.forEach((milestone) => {
        setMilestones((prev) => [...prev, milestone])
        setShowCelebration(true)
        if (onMilestone) onMilestone(milestone)
        setTimeout(() => setShowCelebration(false), 1000)
      })
    }
  }

  React.useEffect(() => {
    checkMilestones(wordCount)
  }, [wordCount])

  return (
    <div className="reward-system">
      <div className="milestone-tracker">
        <div className="milestone-bar">
          <div className="milestone-progress" style={{ width: `${Math.min((wordCount / 5000) * 100, 100)}%` }} />
        </div>
        <p className="word-count">{wordCount} / 5000 words</p>
      </div>

      <div className="achievements">
        {getMilestones().map((milestone) => (
          <div
            key={milestone.words}
            className={`achievement ${milestones.some((m) => m.words === milestone.words) ? 'unlocked' : 'locked'}`}
            title={milestone.name}
          >
            {milestone.icon}
          </div>
        ))}
      </div>

      {showCelebration && (
        <div className="celebration-popup">
          {milestones[milestones.length - 1]?.icon && (
            <div className="popup-content">
              <div className="popup-icon">{milestones[milestones.length - 1].icon}</div>
              <p>{milestones[milestones.length - 1].name}!</p>
            </div>
          )}
        </div>
      )}
    </div>
  )
}
