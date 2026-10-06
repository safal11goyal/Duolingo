"use client";

import React, { useEffect } from "react";
import { useRouter } from "next/navigation";
import confetti from "canvas-confetti";
import { Flame, Heart, Zap, Crown, ArrowRight, Award } from "lucide-react";
import { LessonCompleteResponse } from "@/lib/types";
import { DuoMascot } from "../ui/DuoMascot";
import { sounds } from "@/lib/sound";

interface LessonCompleteModalProps {
  summary: LessonCompleteResponse;
}

export const LessonCompleteModal: React.FC<LessonCompleteModalProps> = ({ summary }) => {
  const router = useRouter();

  useEffect(() => {
    // Play celebratory sound
    sounds.playComplete();

    // Trigger confetti
    try {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 }
      });
      setTimeout(() => {
        confetti({
          particleCount: 60,
          angle: 60,
          spread: 55,
          origin: { x: 0 }
        });
        confetti({
          particleCount: 60,
          angle: 120,
          spread: 55,
          origin: { x: 1 }
        });
      }, 300);
    } catch {}
  }, []);

  return (
    <div className="fixed inset-0 z-50 bg-white flex flex-col items-center justify-between p-6 sm:p-10 select-none animate-pop overflow-y-auto">
      <div className="w-full max-w-xl mx-auto flex-1 flex flex-col items-center justify-center text-center">
        {/* Celebrating Duo Mascot */}
        <div className="mb-6">
          <DuoMascot size={140} expression="celebrate" />
        </div>

        <h1 className="text-3xl sm:text-4xl font-black text-[#58cc02] mb-2 tracking-tight">
          Lesson Complete!
        </h1>
        <p className="text-neutral-500 font-bold text-base mb-8">
          You made great progress today!
        </p>

        {/* Stats Grid */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 w-full mb-8">
          {/* Total XP Earned */}
          <div className="bg-[#ffc800]/10 border-2 border-[#ffc800] rounded-2xl p-4 flex flex-col items-center">
            <div className="w-8 h-8 rounded-full bg-[#ffc800] text-white flex items-center justify-center mb-2 shadow-sm">
              <Zap className="w-5 h-5 fill-white" />
            </div>
            <span className="text-xs font-black uppercase text-[#e5a500] tracking-wider">TOTAL XP</span>
            <span className="text-2xl font-black text-[#e5a500] mt-0.5">+{summary.xp_earned}</span>
          </div>

          {/* Daily Streak */}
          <div className="bg-[#ff9600]/10 border-2 border-[#ff9600] rounded-2xl p-4 flex flex-col items-center">
            <div className="w-8 h-8 rounded-full bg-[#ff9600] text-white flex items-center justify-center mb-2 shadow-sm">
              <Flame className="w-5 h-5 fill-white" />
            </div>
            <span className="text-xs font-black uppercase text-[#e07b00] tracking-wider">STREAK</span>
            <span className="text-2xl font-black text-[#e07b00] mt-0.5">{summary.streak} DAYS</span>
          </div>

          {/* Hearts Remaining */}
          <div className="bg-[#ff4b4b]/10 border-2 border-[#ff4b4b] rounded-2xl p-4 flex flex-col items-center">
            <div className="w-8 h-8 rounded-full bg-[#ff4b4b] text-white flex items-center justify-center mb-2 shadow-sm">
              <Heart className="w-5 h-5 fill-white" />
            </div>
            <span className="text-xs font-black uppercase text-[#ea2b2b] tracking-wider">HEARTS</span>
            <span className="text-2xl font-black text-[#ea2b2b] mt-0.5">{summary.hearts_remaining}</span>
          </div>

          {/* Crowns */}
          <div className="bg-[#ce82ff]/10 border-2 border-[#ce82ff] rounded-2xl p-4 flex flex-col items-center">
            <div className="w-8 h-8 rounded-full bg-[#ce82ff] text-white flex items-center justify-center mb-2 shadow-sm">
              <Crown className="w-5 h-5 fill-white" />
            </div>
            <span className="text-xs font-black uppercase text-[#a55eea] tracking-wider">CROWN</span>
            <span className="text-2xl font-black text-[#a55eea] mt-0.5">LV {summary.skill_progress.crown_level}</span>
          </div>
        </div>

        {/* Unlocked Achievements banner if any */}
        {summary.achievements_unlocked && summary.achievements_unlocked.length > 0 && (
          <div className="w-full bg-[#ddf4ff] border-2 border-[#1cb0f6] rounded-2xl p-4 mb-6 flex items-center gap-3 text-left">
            <Award className="w-8 h-8 text-[#1cb0f6] shrink-0" />
            <div>
              <span className="text-xs font-black uppercase text-[#1899d6] tracking-wider">
                Achievement Unlocked!
              </span>
              <p className="font-extrabold text-neutral-800 text-sm">
                {summary.achievements_unlocked.join(", ")}
              </p>
            </div>
          </div>
        )}

        {summary.next_skill_unlocked && (
          <div className="w-full bg-[#d7ffb8] border-2 border-[#58cc02] rounded-2xl p-3 mb-6 font-black text-[#46a302] text-sm">
            ✨ Next skill unlocked on your learning path!
          </div>
        )}
      </div>

      {/* Bottom Button */}
      <div className="w-full max-w-xl mx-auto pt-4 border-t-2 border-neutral-100">
        <button
          onClick={() => router.push("/learn")}
          className="btn-3d btn-duo-green w-full py-4 text-lg tracking-wider flex items-center justify-center gap-2"
        >
          <span>CONTINUE</span>
          <ArrowRight className="w-6 h-6 stroke-[2.5]" />
        </button>
      </div>
    </div>
  );
};
