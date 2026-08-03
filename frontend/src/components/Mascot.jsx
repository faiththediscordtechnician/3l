import React from 'react'
import '../styles/Mascot.css'

export const Mascot = ({ state = 'idle' }) => {
  return (
    <div className={`mascot mascot-${state}`}>
      <svg viewBox="0 0 100 120" xmlns="http://www.w3.org/2000/svg">
        {/* Head */}
        <circle cx="50" cy="35" r="25" fill="#f4d5b8" stroke="#9d8189" strokeWidth="2" />

        {/* Hair */}
        <path
          d="M 25 30 Q 20 10, 50 8 Q 80 10, 75 30"
          fill="#f4c78d"
          stroke="#d4a560"
          strokeWidth="2"
        />

        {/* Eyes */}
        <circle cx="40" cy="32" r="3" fill="#9d8189" />
        <circle cx="60" cy="32" r="3" fill="#9d8189" />

        {/* Smile */}
        <path
          d="M 40 40 Q 50 45, 60 40"
          fill="none"
          stroke="#9d8189"
          strokeWidth="2"
          strokeLinecap="round"
        />

        {/* Body (Navy Suit) */}
        <path
          d="M 30 55 L 25 90 L 75 90 L 70 55 Q 50 60, 30 55 Z"
          fill="#1a3a52"
          stroke="#9d8189"
          strokeWidth="2"
        />

        {/* Shirt */}
        <path
          d="M 35 60 L 40 85 L 60 85 L 65 60"
          fill="#fff"
          stroke="#9d8189"
          strokeWidth="1"
        />

        {/* Gold Necklace */}
        <circle cx="50" cy="65" r="3" fill="#ffd700" stroke="#d4a560" strokeWidth="1" />
        <circle cx="50" cy="72" r="2" fill="#ffd700" stroke="#d4a560" strokeWidth="1" />

        {/* Arms */}
        <rect x="20" y="60" width="10" height="25" rx="5" fill="#f4d5b8" stroke="#9d8189" strokeWidth="2" />
        <rect x="70" y="60" width="10" height="25" rx="5" fill="#f4d5b8" stroke="#9d8189" strokeWidth="2" />

        {/* Shoes */}
        <rect x="30" y="90" width="8" height="12" rx="2" fill="#1a1a1a" stroke="#9d8189" strokeWidth="1" />
        <rect x="62" y="90" width="8" height="12" rx="2" fill="#1a1a1a" stroke="#9d8189" strokeWidth="1" />
      </svg>

      {state === 'happy' && <div className="mascot-sparkle" />}
      {state === 'celebrating' && (
        <div className="mascot-celebration">
          <div className="confetti" />
          <div className="confetti" style={{ animationDelay: '0.1s' }} />
          <div className="confetti" style={{ animationDelay: '0.2s' }} />
        </div>
      )}
    </div>
  )
}
