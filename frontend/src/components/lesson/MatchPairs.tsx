"use client";

import React, { useState, useEffect } from "react";
import { Check } from "lucide-react";
import { Exercise } from "@/lib/types";
import { sounds } from "@/lib/sound";

interface MatchPairsProps {
  exercise: Exercise;
  selectedAnswer: any;
  onSelectAnswer: (val: any) => void;
  disabled: boolean;
}

export const MatchPairs: React.FC<MatchPairsProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled
}) => {
  const leftItems: string[] = exercise.metadata?.left_items || [];
  const rightItems: string[] = exercise.metadata?.right_items || [];

  // Track active selections
  const [selectedLeft, setSelectedLeft] = useState<string | null>(null);
  const [selectedRight, setSelectedRight] = useState<string | null>(null);

  // Completed pair map { "Hello": "Hola" }
  const [matchedPairs, setMatchedPairs] = useState<{ [key: string]: string }>({});

  useEffect(() => {
    setSelectedLeft(null);
    setSelectedRight(null);
    setMatchedPairs({});
  }, [exercise.id]);

  const handleSelectLeft = (item: string) => {
    if (disabled || matchedPairs[item]) return;
    sounds.playClick();

    if (selectedLeft === item) {
      setSelectedLeft(null);
      return;
    }

    setSelectedLeft(item);

    // If a right item was already selected, record pair
    if (selectedRight) {
      const updated = { ...matchedPairs, [item]: selectedRight };
      setMatchedPairs(updated);
      setSelectedLeft(null);
      setSelectedRight(null);
      onSelectAnswer(updated);
    }
  };

  const handleSelectRight = (item: string) => {
    if (disabled || Object.values(matchedPairs).includes(item)) return;
    sounds.playClick();

    if (selectedRight === item) {
      setSelectedRight(null);
      return;
    }

    setSelectedRight(item);

    // If a left item was already selected, record pair
    if (selectedLeft) {
      const updated = { ...matchedPairs, [selectedLeft]: item };
      setMatchedPairs(updated);
      setSelectedLeft(null);
      setSelectedRight(null);
      onSelectAnswer(updated);
    }
  };

  return (
    <div className="w-full max-w-xl mx-auto select-none">
      <h2 className="text-2xl sm:text-3xl font-black text-neutral-800 mb-2">
        Tap the matching pairs
      </h2>
      <p className="text-sm font-semibold text-neutral-500 mb-8">
        Match English words with their Spanish translation
      </p>

      <div className="grid grid-cols-2 gap-4">
        {/* Left Column */}
        <div className="space-y-3">
          {leftItems.map((item) => {
            const isMatched = !!matchedPairs[item];
            const isSelected = selectedLeft === item;

            return (
              <button
                key={`left-${item}`}
                disabled={disabled || isMatched}
                onClick={() => handleSelectLeft(item)}
                className={`w-full p-4 rounded-2xl font-bold text-base sm:text-lg flex items-center justify-between border-2 transition-all active:scale-[0.98] ${
                  isMatched
                    ? "bg-[#e5e5e5] border-[#cecece] text-neutral-400 opacity-60 cursor-default"
                    : isSelected
                    ? "bg-[#ddf4ff] border-[#1cb0f6] text-[#1899d6] border-b-4"
                    : "bg-white border-neutral-200 border-b-4 hover:bg-neutral-50 text-neutral-700"
                }`}
              >
                <span>{item}</span>
                {isMatched && <Check className="w-4 h-4 text-[#58cc02]" />}
              </button>
            );
          })}
        </div>

        {/* Right Column */}
        <div className="space-y-3">
          {rightItems.map((item) => {
            const isMatched = Object.values(matchedPairs).includes(item);
            const isSelected = selectedRight === item;

            return (
              <button
                key={`right-${item}`}
                disabled={disabled || isMatched}
                onClick={() => handleSelectRight(item)}
                className={`w-full p-4 rounded-2xl font-bold text-base sm:text-lg flex items-center justify-between border-2 transition-all active:scale-[0.98] ${
                  isMatched
                    ? "bg-[#e5e5e5] border-[#cecece] text-neutral-400 opacity-60 cursor-default"
                    : isSelected
                    ? "bg-[#ddf4ff] border-[#1cb0f6] text-[#1899d6] border-b-4"
                    : "bg-white border-neutral-200 border-b-4 hover:bg-neutral-50 text-neutral-700"
                }`}
              >
                <span>{item}</span>
                {isMatched && <Check className="w-4 h-4 text-[#58cc02]" />}
              </button>
            );
          })}
        </div>
      </div>
    </div>
  );
};
