"use client";

import React, { useEffect } from "react";
import { Check, X, ArrowRight } from "lucide-react";
import { AnswerResponse } from "@/lib/types";

interface FeedbackBarProps {
  status: "idle" | "correct" | "incorrect";
  hasSelection: boolean;
  result: AnswerResponse | null;
  onCheck: () => void;
  onContinue: () => void;
  isChecking: boolean;
}

export const FeedbackBar: React.FC<FeedbackBarProps> = ({
  status,
  hasSelection,
  result,
  onCheck,
  onContinue,
  isChecking
}) => {
  // Support Enter key shortcut to check or continue
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === "Enter") {
        e.preventDefault();
        if (status === "idle" && hasSelection && !isChecking) {
          onCheck();
        } else if (status !== "idle") {
          onContinue();
        }
      }
    };
    window.addEventListener("keydown", handleKeyDown);
    return () => window.removeEventListener("keydown", handleKeyDown);
  }, [status, hasSelection, isChecking, onCheck, onContinue]);

  return (
    <footer
      className={`fixed bottom-0 left-0 right-0 border-t-2 select-none transition-colors duration-200 z-40 ${
        status === "correct"
          ? "bg-[#d7ffb8] border-[#b8f28b]"
          : status === "incorrect"
          ? "bg-[#ffdfe0] border-[#fbc2c4] animate-shake"
          : "bg-white border-neutral-200"
      }`}
    >
      <div className="w-full max-w-4xl mx-auto px-4 sm:px-8 py-5 flex items-center justify-between gap-4">
        {/* Left Feedback Banner Message */}
        <div className="flex-1">
          {status === "correct" && (
            <div className="flex items-center gap-3">
              <div className="w-12 h-12 rounded-full bg-[#58cc02] text-white flex items-center justify-center shrink-0 shadow">
                <Check className="w-7 h-7 stroke-[3.5]" />
              </div>
              <div>
                <h4 className="text-xl sm:text-2xl font-black text-[#58cc02]">
                  Nicely done!
                </h4>
                {result?.explanation && (
                  <p className="text-xs font-bold text-neutral-600 mt-0.5">
                    {result.explanation}
                  </p>
                )}
              </div>
            </div>
          )}

          {status === "incorrect" && (
            <div className="flex items-start gap-3">
              <div className="w-12 h-12 rounded-full bg-[#ff4b4b] text-white flex items-center justify-center shrink-0 shadow">
                <X className="w-7 h-7 stroke-[3.5]" />
              </div>
              <div>
                <h4 className="text-xl sm:text-2xl font-black text-[#ff4b4b]">
                  Correct solution:
                </h4>
                <p className="text-base sm:text-lg font-extrabold text-[#ea2b2b] mt-0.5">
                  {result?.correct_answer}
                </p>
                {result?.explanation && (
                  <p className="text-xs font-bold text-neutral-600 mt-1">
                    {result.explanation}
                  </p>
                )}
              </div>
            </div>
          )}
        </div>

        {/* Right Action Button */}
        <div>
          {status === "idle" ? (
            <button
              disabled={!hasSelection || isChecking}
              onClick={onCheck}
              className="btn-3d btn-duo-green px-8 sm:px-12 py-3.5 text-base sm:text-lg tracking-wider"
            >
              {isChecking ? "CHECKING..." : "CHECK"}
            </button>
          ) : (
            <button
              onClick={onContinue}
              className={`btn-3d px-8 sm:px-12 py-3.5 text-base sm:text-lg tracking-wider flex items-center gap-2 ${
                status === "correct" ? "btn-duo-green" : "btn-duo-red"
              }`}
            >
              <span>CONTINUE</span>
              <ArrowRight className="w-5 h-5 stroke-[2.5]" />
            </button>
          )}
        </div>
      </div>
    </footer>
  );
};
