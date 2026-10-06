import React from "react";

interface DuoMascotProps {
  expression?: "happy" | "cheering" | "thinking" | "sad" | "celebrate";
  size?: number;
  className?: string;
}

export const DuoMascot: React.FC<DuoMascotProps> = ({
  expression = "happy",
  size = 120,
  className = ""
}) => {
  return (
    <div
      className={`inline-block select-none relative ${className}`}
      style={{ width: size, height: size }}
    >
      <svg
        viewBox="0 0 160 160"
        width={size}
        height={size}
        fill="none"
        xmlns="http://www.w3.org/2000/svg"
        className="w-full h-full drop-shadow-md transition-transform duration-300 hover:scale-105"
      >
        {/* Party Hat for celebrate */}
        {expression === "celebrate" && (
          <g transform="translate(68, 5) rotate(10)">
            <polygon points="12,0 0,35 24,35" fill="#ff4b4b" />
            <polygon points="12,0 8,35 16,35" fill="#ffc800" />
            <circle cx="12" cy="0" r="4" fill="#ffd900" />
          </g>
        )}

        {/* Feet */}
        <ellipse cx="60" cy="142" rx="14" ry="7" fill="#ff9600" />
        <ellipse cx="100" cy="142" rx="14" ry="7" fill="#ff9600" />

        {/* Body (Emerald / Vibrant green) */}
        <path
          d="M80 20C46 20 30 46 30 85C30 120 48 140 80 140C112 140 130 120 130 85C130 46 114 20 80 20Z"
          fill="#58cc02"
        />

        {/* Feather shading on top */}
        <path
          d="M80 20C55 20 40 38 35 60C45 45 62 35 80 35C98 35 115 45 125 60C120 38 105 20 80 20Z"
          fill="#46a302"
        />

        {/* Chest Feather patch */}
        <path
          d="M80 85C66 85 55 96 55 112C55 126 67 135 80 135C93 135 105 126 105 112C105 96 94 85 80 85Z"
          fill="#79e016"
        />

        {/* Wings */}
        {expression === "cheering" || expression === "celebrate" ? (
          <>
            {/* Raised wings */}
            <path
              d="M32 75C20 60 10 40 20 30C28 22 42 42 38 68Z"
              fill="#46a302"
            />
            <path
              d="M128 75C140 60 150 40 140 30C132 22 118 42 122 68Z"
              fill="#46a302"
            />
          </>
        ) : (
          <>
            {/* Resting wings */}
            <path
              d="M30 75C24 85 24 105 32 115C36 105 37 90 35 75Z"
              fill="#46a302"
            />
            <path
              d="M130 75C136 85 136 105 128 115C124 105 123 90 125 75Z"
              fill="#46a302"
            />
          </>
        )}

        {/* Eyes White Base */}
        <circle cx="60" cy="65" r="19" fill="#ffffff" />
        <circle cx="100" cy="65" r="19" fill="#ffffff" />

        {/* Eye Details & Pupils */}
        {expression === "sad" ? (
          <>
            {/* Sad / watery eyes */}
            <circle cx="60" cy="67" r="10" fill="#2b475c" />
            <circle cx="100" cy="67" r="10" fill="#2b475c" />
            <circle cx="63" cy="64" r="4" fill="#ffffff" />
            <circle cx="103" cy="64" r="4" fill="#ffffff" />
            {/* Tear */}
            <path
              d="M52 82C52 85 54 87 56 87C58 87 60 85 60 82C60 79 56 74 56 74C56 74 52 79 52 82Z"
              fill="#1cb0f6"
            />
            {/* Sad eyebrows */}
            <path d="M48 48Q58 54 68 50" stroke="#46a302" strokeWidth="4" strokeLinecap="round" fill="none" />
            <path d="M92 50Q102 54 112 48" stroke="#46a302" strokeWidth="4" strokeLinecap="round" fill="none" />
          </>
        ) : expression === "thinking" ? (
          <>
            {/* Looking up / thoughtful */}
            <circle cx="60" cy="60" r="10" fill="#2b475c" />
            <circle cx="100" cy="60" r="10" fill="#2b475c" />
            <circle cx="63" cy="58" r="4" fill="#ffffff" />
            <circle cx="103" cy="58" r="4" fill="#ffffff" />
            {/* Inquisitive eyebrow */}
            <path d="M48 48Q58 44 68 50" stroke="#46a302" strokeWidth="4" strokeLinecap="round" fill="none" />
            <path d="M92 46Q102 42 112 44" stroke="#46a302" strokeWidth="4" strokeLinecap="round" fill="none" />
          </>
        ) : (
          <>
            {/* Happy / Cheerful pupils */}
            <circle cx="60" cy="65" r="11" fill="#2b475c" />
            <circle cx="100" cy="65" r="11" fill="#2b475c" />
            <circle cx="64" cy="62" r="4" fill="#ffffff" />
            <circle cx="104" cy="62" r="4" fill="#ffffff" />
            {/* Happy eyebrows */}
            <path d="M48 46Q58 42 68 46" stroke="#46a302" strokeWidth="4" strokeLinecap="round" fill="none" />
            <path d="M92 46Q102 42 112 46" stroke="#46a302" strokeWidth="4" strokeLinecap="round" fill="none" />
          </>
        )}

        {/* Beak */}
        <polygon points="80,68 70,82 90,82" fill="#ff9600" />
        <polygon points="80,87 73,82 87,82" fill="#e07b00" />
      </svg>
    </div>
  );
};
