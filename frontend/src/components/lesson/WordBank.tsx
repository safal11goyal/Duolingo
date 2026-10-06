"use client";

import React, { useState, useEffect } from "react";
import { Volume2 } from "lucide-react";
import { Exercise } from "@/lib/types";
import { sounds } from "@/lib/sound";
import { DuoMascot } from "../ui/DuoMascot";

interface WordBankProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (val: string) => void;
  disabled: boolean;
}

export const WordBank: React.FC<WordBankProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled
}) => {
  // Tokens list from metadata
  const initialTokens: string[] = exercise.metadata?.tokens || [];
  
  // Track selected token indices
  const [selectedIndices, setSelectedIndices] = useState<number[]>([]);

  // Keep parent answer string synchronized
  const handleToggleToken = (index: number) => {
    if (disabled) return;
    sounds.playClick();

    if (selectedIndices.includes(index)) {
      // Remove from selected
      const updated = selectedIndices.filter((i) => i !== index);
      setSelectedIndices(updated);
      const sentence = updated.map((i) => initialTokens[i]).join(" ");
      onSelectAnswer(sentence);
    } else {
      // Add to selected
      const updated = [...selectedIndices, index];
      setSelectedIndices(updated);
      const sentence = updated.map((i) => initialTokens[i]).join(" ");
      onSelectAnswer(sentence);
    }
  };

  // Reset indices if exercise changes
  useEffect(() => {
    setSelectedIndices([]);
  }, [exercise.id]);

  const cleanQuestion = exercise.question.replace(/^Build the sentence:\s*/i, "").replace(/^Build:\s*/i, "").replace(/['"]/g, "");

  return (
    <div className="w-full max-w-xl mx-auto select-none">
      <h2 className="text-xl sm:text-2xl font-black text-neutral-800 mb-6">
        Build this sentence
      </h2>

      {/* Mascot Prompt */}
      <div className="flex items-end gap-4 mb-6">
        <DuoMascot size={80} expression="thinking" />

        <div className="relative bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
          <button
            onClick={() => sounds.speak(cleanQuestion, "en-US")}
            className="p-2.5 rounded-xl bg-[#1cb0f6] text-white hover:bg-[#1899d6] transition-colors shadow-sm"
            title="Listen"
          >
            <Volume2 className="w-5 h-5" />
          </button>
          <span className="text-xl font-bold text-neutral-800">{cleanQuestion}</span>
        </div>
      </div>

      {/* Answer Slots Area */}
      <div className="min-h-[72px] p-3 rounded-2xl border-2 border-dashed border-neutral-300 bg-neutral-50 mb-8 flex flex-wrap gap-2 items-center">
        {selectedIndices.length === 0 ? (
          <span className="text-neutral-400 font-bold text-sm ml-2">
            Tap the word tiles below to build the sentence
          </span>
        ) : (
          selectedIndices.map((tokenIdx) => (
            <button
              key={`selected-${tokenIdx}`}
              disabled={disabled}
              onClick={() => handleToggleToken(tokenIdx)}
              className="px-4 py-2.5 rounded-2xl bg-white border-2 border-neutral-200 border-b-4 font-extrabold text-neutral-800 shadow-sm hover:bg-neutral-50 active:scale-95 transition-all animate-pop"
            >
              {initialTokens[tokenIdx]}
            </button>
          ))
        )}
      </div>

      {/* Word Bank Pool */}
      <div className="flex flex-wrap gap-2.5 justify-center pt-4 border-t-2 border-neutral-100">
        {initialTokens.map((token, idx) => {
          const isUsed = selectedIndices.includes(idx);

          return (
            <div key={`bank-slot-${idx}`} className="relative">
              {/* Ghost shadow placeholder */}
              <div
                className={`px-4 py-2.5 rounded-2xl border-2 border-neutral-200 bg-neutral-200/50 font-extrabold text-transparent select-none ${
                  isUsed ? "opacity-100" : "opacity-0"
                }`}
              >
                {token}
              </div>

              {/* Active Chip */}
              {!isUsed && (
                <button
                  disabled={disabled}
                  onClick={() => handleToggleToken(idx)}
                  className="absolute inset-0 px-4 py-2.5 rounded-2xl bg-white border-2 border-neutral-200 border-b-4 font-extrabold text-neutral-800 shadow-sm hover:bg-neutral-50 active:scale-95 transition-all"
                >
                  {token}
                </button>
              )}
            </div>
          );
        })}
      </div>
    </div>
  );
};
