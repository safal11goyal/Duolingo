"use client";

import React, { useEffect } from "react";
import { Exercise } from "@/lib/types";
import { sounds } from "@/lib/sound";

interface MultipleChoiceProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (val: string) => void;
  disabled: boolean;
}

export const MultipleChoice: React.FC<MultipleChoiceProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled
}) => {
  // Listen for keyboard 1, 2, 3, 4 shortcuts
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (disabled) return;
      const num = parseInt(e.key);
      if (num >= 1 && num <= exercise.options.length) {
        const opt = exercise.options[num - 1];
        if (opt) {
          sounds.playClick();
          onSelectAnswer(opt.text);
        }
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [disabled, exercise.options, onSelectAnswer]);

  return (
    <div className="w-full max-w-xl mx-auto select-none">
      <h2 className="text-2xl sm:text-3xl font-black text-neutral-800 mb-8 leading-snug">
        {exercise.question}
      </h2>

      <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
        {exercise.options.map((option, idx) => {
          const isSelected = selectedAnswer === option.text;

          return (
            <button
              key={option.id}
              disabled={disabled}
              onClick={() => {
                sounds.playClick();
                onSelectAnswer(option.text);
              }}
              className={`p-5 rounded-2xl font-bold text-left text-lg flex items-center justify-between border-2 transition-all active:scale-[0.98] ${
                isSelected
                  ? "bg-[#ddf4ff] border-[#1cb0f6] text-[#1899d6] border-b-4 shadow-sm"
                  : "bg-white border-neutral-200 border-b-4 hover:bg-neutral-50 text-neutral-700"
              }`}
            >
              <span className="font-extrabold">{option.text}</span>
              <span className="text-xs font-black px-2 py-1 rounded-lg border border-neutral-200 text-neutral-400 bg-neutral-50 hidden sm:inline">
                {idx + 1}
              </span>
            </button>
          );
        })}
      </div>
    </div>
  );
};
