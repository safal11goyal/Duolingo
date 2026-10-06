"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { X, Heart } from "lucide-react";

interface LessonHeaderProps {
  currentIndex: number;
  totalExercises: number;
  hearts: number;
}

export const LessonHeader: React.FC<LessonHeaderProps> = ({
  currentIndex,
  totalExercises,
  hearts
}) => {
  const router = useRouter();
  const [showExitModal, setShowExitModal] = useState(false);

  const progressPercent = Math.min(100, Math.round((currentIndex / Math.max(1, totalExercises)) * 100));

  return (
    <>
      <header className="w-full max-w-4xl mx-auto px-4 py-6 flex items-center justify-between gap-4 select-none">
        {/* Close Button */}
        <button
          onClick={() => setShowExitModal(true)}
          className="text-neutral-400 hover:text-neutral-600 p-2 rounded-xl hover:bg-neutral-100 transition-colors"
          title="Exit lesson"
        >
          <X className="w-7 h-7 stroke-[2.5]" />
        </button>

        {/* Progress Bar */}
        <div className="flex-1 bg-neutral-200 h-4 rounded-full overflow-hidden p-0.5 relative">
          <div
            className="h-full bg-[#58cc02] rounded-full transition-all duration-300 ease-out"
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        {/* Hearts Indicator */}
        <div className="flex items-center gap-1.5 font-black text-lg text-[#ff4b4b]">
          <Heart className="w-7 h-7 fill-[#ff4b4b] animate-pulse" />
          <span>{hearts}</span>
        </div>
      </header>

      {/* Exit Confirmation Modal */}
      {showExitModal && (
        <div className="fixed inset-0 z-50 bg-black/50 flex items-center justify-center p-4 animate-pop">
          <div className="bg-white rounded-3xl max-w-sm w-full p-6 text-center shadow-2xl border-2 border-neutral-200">
            <h3 className="text-2xl font-black text-neutral-800 mb-2">Are you sure?</h3>
            <p className="text-neutral-500 text-sm mb-6">
              All your progress in this current lesson will be lost if you leave now.
            </p>
            <div className="space-y-3">
              <button
                onClick={() => setShowExitModal(false)}
                className="btn-3d btn-duo-blue w-full py-3 text-sm"
              >
                KEEP LEARNING
              </button>
              <button
                onClick={() => router.push("/learn")}
                className="btn-3d btn-duo-red w-full py-3 text-sm"
              >
                END LESSON
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
