"use client";

import React, { useState } from "react";
import Link from "next/link";
import { Check, Crown, Lock, Star, Play, Sparkles, X } from "lucide-react";
import { SkillSummary } from "@/lib/types";

interface SkillNodeProps {
  skill: SkillSummary;
  index: number;
}

export const SkillNode: React.FC<SkillNodeProps> = ({ skill, index }) => {
  const [showPopup, setShowPopup] = useState(false);

  // Snake curve offset calculation
  // Pattern: 0 -> 0, 1 -> 45px right, 2 -> 0, 3 -> -45px left
  const offsets = [
    "translate-x-0",
    "translate-x-10 sm:translate-x-14",
    "translate-x-0",
    "-translate-x-10 sm:-translate-x-14",
  ];
  const offsetClass = offsets[index % 4];

  const isLocked = skill.status === "locked";
  const isCompleted = skill.status === "completed";
  const isCurrent = skill.status === "available" || skill.status === "in_progress";

  // Next unfinished lesson id
  const nextLesson = skill.lessons.find(
    (_, lIdx) => lIdx >= skill.completed_lessons
  ) || skill.lessons[0];

  const handleNodeClick = () => {
    setShowPopup((prev) => !prev);
  };

  return (
    <div className={`relative flex flex-col items-center my-6 ${offsetClass} select-none`}>
      {/* Floating "START" hint bubble for active skill */}
      {isCurrent && (
        <div className="absolute -top-10 z-20 animate-bounce pointer-events-none">
          <div className="bg-white border-2 border-neutral-200 text-[#58cc02] font-black text-xs px-3 py-1.5 rounded-xl shadow-md uppercase tracking-wider relative flex items-center gap-1">
            <Sparkles className="w-3.5 h-3.5 text-[#ffc800] fill-[#ffc800]" />
            Start
            {/* Speech bubble beak */}
            <div className="w-2.5 h-2.5 bg-white border-r-2 border-b-2 border-neutral-200 transform rotate-45 absolute -bottom-1.5 left-1/2 -translate-x-1/2" />
          </div>
        </div>
      )}

      {/* Main Circular Node Button */}
      <button
        onClick={handleNodeClick}
        disabled={false}
        className={`relative w-20 h-20 rounded-full flex items-center justify-center transition-all duration-150 active:translate-y-1 ${
          isLocked
            ? "bg-[#e5e5e5] border-b-[6px] border-[#cecece] text-[#afafaf] cursor-not-allowed"
            : isCompleted
            ? "bg-[#ffc800] border-b-[6px] border-[#e5a500] text-white hover:brightness-105"
            : "bg-[#58cc02] border-b-[6px] border-[#46a302] text-white hover:brightness-105 animate-pulse-ring"
        }`}
      >
        {/* Inner icon */}
        {isLocked ? (
          <Lock className="w-8 h-8 stroke-[2.5]" />
        ) : isCompleted ? (
          <Check className="w-9 h-9 stroke-[3.5]" />
        ) : (
          <Star className="w-9 h-9 fill-white stroke-[2]" />
        )}

        {/* Crown Badge */}
        {skill.crown_level > 0 && (
          <div className="absolute -bottom-1 -right-1 bg-[#ffc800] border-2 border-white rounded-full p-1 shadow flex items-center justify-center">
            <Crown className="w-3.5 h-3.5 fill-white text-white" />
          </div>
        )}
      </button>

      {/* Label under node */}
      <span className="font-extrabold text-sm text-neutral-700 mt-2 text-center max-w-[120px] truncate">
        {skill.title}
      </span>

      {/* Popup Dialog on click */}
      {showPopup && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/40 animate-pop">
          <div className="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-2 border-neutral-200 relative text-center">
            <button
              onClick={() => setShowPopup(false)}
              className="absolute top-4 right-4 p-2 text-neutral-400 hover:text-neutral-700 rounded-full hover:bg-neutral-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex justify-center mb-3">
              <div
                className={`w-16 h-16 rounded-full flex items-center justify-center ${
                  isLocked
                    ? "bg-neutral-200 text-neutral-500"
                    : isCompleted
                    ? "bg-[#ffc800] text-white"
                    : "bg-[#58cc02] text-white"
                }`}
              >
                {isLocked ? (
                  <Lock className="w-8 h-8" />
                ) : isCompleted ? (
                  <Crown className="w-8 h-8 fill-white" />
                ) : (
                  <Star className="w-8 h-8 fill-white" />
                )}
              </div>
            </div>

            <h3 className="text-xl font-black text-neutral-800 mb-1">{skill.title}</h3>
            <p className="text-xs text-neutral-500 mb-4">{skill.description}</p>

            {/* Progress indicators */}
            <div className="bg-neutral-50 rounded-2xl p-3 mb-5 border border-neutral-100 flex items-center justify-around text-xs font-bold text-neutral-600">
              <div>
                <span className="block text-neutral-400 uppercase text-[10px]">Crowns</span>
                <span className="text-base font-black text-[#ffc800]">{skill.crown_level}</span>
              </div>
              <div className="h-6 w-px bg-neutral-200" />
              <div>
                <span className="block text-neutral-400 uppercase text-[10px]">Lessons</span>
                <span className="text-base font-black text-[#58cc02]">
                  {skill.completed_lessons} / {skill.total_lessons}
                </span>
              </div>
            </div>

            {/* Action Button */}
            {isLocked ? (
              <div className="p-3 bg-neutral-100 rounded-2xl text-xs font-bold text-neutral-500">
                🔒 Complete previous skills on your path to unlock this skill.
              </div>
            ) : nextLesson ? (
              <Link
                href={`/lesson/${nextLesson.id}`}
                className="btn-3d btn-duo-green w-full py-3.5 text-sm flex items-center justify-center gap-2"
              >
                <Play className="w-4 h-4 fill-white" />
                START +{nextLesson.xp_reward} XP
              </Link>
            ) : (
              <div className="text-sm font-bold text-neutral-400">No lessons available.</div>
            )}
          </div>
        </div>
      )}
    </div>
  );
};
