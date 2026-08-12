export function CharacterJumping() {
  return (
    <svg className="character-jumping" viewBox="0 0 220 300" xmlns="http://www.w3.org/2000/svg">
      {/* Hair (flowing down, sideways view) */}
      <path d="M 80 50 Q 70 45 70 25 Q 70 15 90 12 Q 110 10 115 15 L 115 60" stroke="#d4a574" strokeWidth="9" fill="none" strokeLinecap="round"/>
      <path d="M 75 60 Q 70 100 75 140 Q 78 170 82 200" stroke="#d4a574" strokeWidth="8" fill="none" strokeLinecap="round"/>
      <path d="M 85 65 Q 82 110 88 150 Q 92 185 95 220" stroke="#d4a574" strokeWidth="7" fill="none" strokeLinecap="round"/>

      {/* Head (profile) */}
      <circle cx="100" cy="50" r="32" fill="#f4d4c8"/>

      {/* Eye */}
      <circle cx="115" cy="45" r="4" fill="#6b5b7f"/>
      <circle cx="116" cy="43" r="1.5" fill="white"/>

      {/* Nose */}
      <line x1="118" y1="50" x2="122" y2="52" stroke="#d9a5a1" strokeWidth="1.5" strokeLinecap="round"/>

      {/* Mouth (smile) */}
      <path d="M 108 60 Q 115 65 122 60" stroke="#d9a5a1" strokeWidth="2" fill="none" strokeLinecap="round"/>

      {/* Neck */}
      <rect x="98" y="78" width="12" height="8" fill="#f4d4c8"/>

      {/* Sweater Vest (Navy) */}
      <rect x="75" y="85" width="65" height="75" fill="#001f3f" rx="4"/>
      <line x1="92" y1="85" x2="92" y2="160" stroke="#1a3a52" strokeWidth="2"/>
      <line x1="125" y1="85" x2="125" y2="160" stroke="#1a3a52" strokeWidth="2"/>
      {/* Gold buttons */}
      <circle cx="100" cy="100" r="3" fill="#ffd700"/>
      <circle cx="100" cy="120" r="3" fill="#ffd700"/>
      <circle cx="100" cy="140" r="3" fill="#ffd700"/>

      {/* White shirt under vest */}
      <rect x="88" y="90" width="32" height="65" fill="#fffacd" rx="2"/>

      {/* Collar */}
      <path d="M 80 85 L 85 78 L 90 85" fill="#f4d4c8"/>

      {/* Skirt (Maroon) */}
      <path d="M 78 160 Q 72 180 75 220 L 140 220 Q 143 180 137 160" fill="#800020"/>
      <line x1="92" y1="160" x2="88" y2="220" stroke="#600018" strokeWidth="1"/>
      <line x1="108" y1="160" x2="108" y2="220" stroke="#600018" strokeWidth="1"/>
      <line x1="124" y1="160" x2="128" y2="220" stroke="#600018" strokeWidth="1"/>

      {/* Left Arm (down) */}
      <ellipse cx="72" cy="115" rx="8" ry="28" fill="#f4d4c8"/>
      <circle cx="68" cy="148" r="6" fill="#f4d4c8"/>

      {/* Right Arm (up, jumping) */}
      <ellipse cx="145" cy="100" rx="8" ry="30" fill="#f4d4c8" transform="rotate(-25 145 100)"/>
      <circle cx="155" cy="70" r="6" fill="#f4d4c8"/>

      {/* Left Leg (down) */}
      <line x1="92" y1="220" x2="88" y2="260" stroke="#f4d4c8" strokeWidth="7" strokeLinecap="round"/>
      <ellipse cx="88" cy="268" rx="7" ry="5" fill="#800020"/>

      {/* Right Leg (up, bent) */}
      <line x1="120" y1="220" x2="128" y2="190" stroke="#f4d4c8" strokeWidth="7" strokeLinecap="round"/>
      <ellipse cx="130" cy="185" rx="7" ry="5" fill="#001f3f"/>

      {/* Excitement lines */}
      <line x1="160" y1="50" x2="175" y2="45" stroke="#ffd700" strokeWidth="2" strokeLinecap="round"/>
      <line x1="165" y1="65" x2="182" y2="60" stroke="#ffd700" strokeWidth="2" strokeLinecap="round"/>
    </svg>
  );
}
