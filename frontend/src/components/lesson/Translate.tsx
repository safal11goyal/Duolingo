"use client";

import React from "react";
import { Volume2 } from "lucide-react";
import { Exercise } from "@/lib/types";
import { sounds } from "@/lib/sound";
import { DuoMascot } from "../ui/DuoMascot";

interface TranslateProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (val: string) => void;
  disabled: boolean;
}

export const Translate: React.FC<TranslateProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled
}) => {
  const accents = ["á", "é", "í", "ó", "ú", "ñ", "¿", "¡"];

  const handleAccentClick = (char: string) => {
    if (disabled) return;
    sounds.playClick();
    onSelectAnswer(selectedAnswer + char);
  };

  const cleanQuestion = exercise.question.replace(/^Translate:\s*/i, "").replace(/['"]/g, "");

  return (
    <div className="w-full max-w-xl mx-auto select-none">
      <h2 className="text-xl sm:text-2xl font-black text-neutral-800 mb-6">
        Translate this sentence
      </h2>

      {/* Mascot Prompt with Speech Bubble */}
      <div className="flex items-end gap-4 mb-8">
        <DuoMascot size={80} expression="happy" />

        <div className="relative bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
          <button
            onClick={() => sounds.speak(cleanQuestion, "es-ES")}
            className="p-2.5 rounded-xl bg-[#1cb0f6] text-white hover:bg-[#1899d6] transition-colors shadow-sm"
            title="Listen"
          >
            <Volume2 className="w-5 h-5" />
          </button>
          <span className="text-xl font-bold text-neutral-800">{cleanQuestion}</span>
        </div>
      </div>

      {/* Text Area */}
      <div className="mb-4">
        <textarea
          disabled={disabled}
          value={selectedAnswer}
          onChange={(e) => onSelectAnswer(e.target.value)}
          placeholder="Type in Spanish..."
          rows={3}
          className="w-full p-4 rounded-2xl border-2 border-neutral-200 bg-neutral-50 focus:bg-white focus:border-[#1cb0f6] focus:outline-none font-bold text-lg text-neutral-800 resize-none transition-all"
        />
      </div>

      {/* Accent helpers toolbar */}
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
