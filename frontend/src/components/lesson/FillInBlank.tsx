"use client";

import React from "react";
import { Exercise } from "@/lib/types";
import { sounds } from "@/lib/sound";
import { DuoMascot } from "../ui/DuoMascot";

interface FillInBlankProps {
  exercise: Exercise;
  selectedAnswer: string;
  onSelectAnswer: (val: string) => void;
  disabled: boolean;
}

export const FillInBlank: React.FC<FillInBlankProps> = ({
  exercise,
  selectedAnswer,
  onSelectAnswer,
  disabled
}) => {
  // Sentence with blank ___
  const parts = exercise.question.split("___");
  const options = exercise.options;

  return (
    <div className="w-full max-w-xl mx-auto select-none">
      <h2 className="text-xl sm:text-2xl font-black text-neutral-800 mb-6">
        Fill in the blank
      </h2>

      {/* Sentence with blank slot */}
      <div className="flex items-end gap-4 mb-10">
        <DuoMascot size={80} expression="happy" />

        <div className="bg-white border-2 border-neutral-200 rounded-2xl p-5 shadow-sm text-xl font-bold text-neutral-800 leading-relaxed flex items-center flex-wrap gap-2">
          <span>{parts[0]}</span>
          <span
            className={`px-3 py-1 min-w-[70px] text-center border-b-4 border-dashed rounded-lg transition-all ${
              selectedAnswer
                ? "border-[#1cb0f6] text-[#1cb0f6] bg-[#ddf4ff] border-solid"
                : "border-neutral-400 text-neutral-400"
            }`}
          >
            {selectedAnswer || "_____"}
          </span>
          <span>{parts[1] || ""}</span>
        </div>
      </div>

      {/* Option Chips */}
      <div className="flex flex-wrap gap-3 justify-center">
        {options.map((opt) => {
          const isSelected = selectedAnswer === opt.text;

          return (
            <button
              key={opt.id}
              disabled={disabled}
              onClick={() => {
                sounds.playClick();
                onSelectAnswer(opt.text);
              }}
              className={`px-6 py-3.5 rounded-2xl font-black text-lg border-2 transition-all active:scale-95 ${
                isSelected
                  ? "bg-[#ddf4ff] border-[#1cb0f6] text-[#1899d6] border-b-4 shadow-sm"
                  : "bg-white border-neutral-200 border-b-4 hover:bg-neutral-50 text-neutral-700"
              }`}
            >
              {opt.text}
            </button>
          );
        })}
      </div>
    </div>
  );
};
