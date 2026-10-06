"use client";

import React, { useRef, useEffect } from "react";
import { Exercise } from "@/lib/types";
import { sounds } from "@/lib/sound";
import { DuoMascot } from "../ui/DuoMascot";

interface TypeAnswerProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (val: string) => void;
  disabled: boolean;
  onSubmit: () => void;
}

export const TypeAnswer: React.FC<TypeAnswerProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled,
  onSubmit
}) => {
  const inputRef = useRef<HTMLInputElement>(null);
  const accents = ["á", "é", "í", "ó", "ú", "ñ", "¿", "¡"];

  useEffect(() => {
    inputRef.current?.focus();
  }, [exercise.id]);

  const handleAccentClick = (char: string) => {
    if (disabled) return;
    sounds.playClick();
    onSelectAnswer(selectedAnswer + char);
    inputRef.current?.focus();
  };

  const handleKeyDown = (e: React.KeyboardEvent) => {
    if (e.key === "Enter" && selectedAnswer.trim() && !disabled) {
      e.preventDefault();
      onSubmit();
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto select-none">
      <h2 className="text-xl sm:text-2xl font-black text-neutral-800 mb-6">
        Type the answer in Spanish
      </h2>

      <div className="flex items-end gap-4 mb-8">
        <DuoMascot size={80} expression="thinking" />

        <div className="bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm text-xl font-bold text-neutral-800">
          {exercise.question}
        </div>
      </div>

      {/* Input Field */}
      <div className="mb-4">
        <input
          ref={inputRef}
          disabled={disabled}
          type="text"
          value={selectedAnswer}
          onChange={(e) => onSelectAnswer(e.target.value)}
          onKeyDown={handleKeyDown}
          placeholder="Type here..."
          className="w-full p-4 rounded-2xl border-2 border-neutral-200 bg-neutral-50 focus:bg-white focus:border-[#1cb0f6] focus:outline-none font-bold text-lg text-neutral-800 transition-all shadow-inner"
        />
      </div>

      {/* Accents Bar */}
      <div className="flex flex-wrap gap-2">
        {accents.map((char) => (
          <button
            key={char}
            type="button"
            disabled={disabled}
            onClick={() => handleAccentClick(char)}
            className="w-10 h-10 rounded-xl border-2 border-neutral-200 bg-white font-extrabold text-neutral-700 hover:bg-neutral-50 active:scale-95 transition-all"
          >
            {char}
          </button>
        ))}
      </div>
    </div>
  );
};
