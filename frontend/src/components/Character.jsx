export function CharacterJumping() {
  return (
    <svg className="character-jumping" viewBox="0 0 200 280" xmlns="http://www.w3.org/2000/svg">
      {/* Head */}
      <circle cx="100" cy="50" r="28" fill="#f4d4c8" stroke="#b8a0b8" strokeWidth="2"/>

      {/* Eyes */}
      <circle cx="90" cy="45" r="4" fill="#6b5b7f"/>
      <circle cx="110" cy="45" r="4" fill="#6b5b7f"/>

      {/* Smile */}
      <path d="M 92 58 Q 100 64 108 58" stroke="#d9a5a1" strokeWidth="2.5" fill="none" strokeLinecap="round"/>

      {/* Body/Sweater Vest (Navy) */}
      <rect x="70" y="75" width="60" height="65" fill="#001f3f" rx="6"/>

      {/* Collar edges */}
      <path d="M 85 75 L 82 68 L 88 75" fill="#f4d4c8"/>
      <path d="M 115 75 L 118 68 L 112 75" fill="#f4d4c8"/>

      {/* White shirt center */}
      <rect x="88" y="80" width="24" height="58" fill="#fffacd" rx="2"/>

      {/* Gold buttons */}
      <circle cx="100" cy="95" r="3.5" fill="#ffd700"/>
      <circle cx="100" cy="115" r="3.5" fill="#ffd700"/>
      <circle cx="100" cy="135" r="3.5" fill="#ffd700"/>

      {/* Left Arm */}
      <rect x="65" y="95" width="10" height="40" fill="#f4d4c8" rx="5"/>
      <circle cx="70" cy="138" r="7" fill="#f4d4c8"/>

      {/* Right Arm */}
      <rect x="125" y="95" width="10" height="40" fill="#f4d4c8" rx="5"/>
      <circle cx="130" cy="138" r="7" fill="#f4d4c8"/>

      {/* Left Leg */}
      <rect x="82" y="138" width="9" height="45" fill="#f4d4c8" rx="4.5"/>
      <ellipse cx="86.5" cy="188" rx="6" ry="5" fill="#001f3f" stroke="#b8a0b8" strokeWidth="1"/>

      {/* Right Leg */}
      <rect x="109" y="138" width="9" height="45" fill="#f4d4c8" rx="4.5"/>
      <ellipse cx="113.5" cy="188" rx="6" ry="5" fill="#001f3f" stroke="#b8a0b8" strokeWidth="1"/>

      {/* Accent sparkles */}
      <circle cx="140" cy="35" r="2" fill="#ffd700"/>
      <circle cx="150" cy="50" r="1.5" fill="#ffd700"/>
    </svg>
  );
}
