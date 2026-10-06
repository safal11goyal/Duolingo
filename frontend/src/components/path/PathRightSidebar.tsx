"use client";

import React from "react";
import Link from "next/link";
import { Target, Trophy, Heart, Sparkles, ArrowRight, CheckCircle2 } from "lucide-react";
import { UserProfile } from "@/lib/types";

interface PathRightSidebarProps {
  profile: UserProfile | null;
  onRefillClick?: () => void;
}

export const PathRightSidebar: React.FC<PathRightSidebarProps> = ({ profile, onRefillClick }) => {
  const dailyProgress = profile?.daily_goal_progress || 0;
  const dailyGoal = profile?.daily_goal || 20;
  const progressPercent = Math.min(100, Math.round((dailyProgress / Math.max(1, dailyGoal)) * 100));
  const isGoalCompleted = dailyProgress >= dailyGoal;

  return (
    <div className="hidden lg:flex flex-col w-80 space-y-6 select-none pl-6">
      {/* Daily Goal / Quest Card */}
      <div className="bg-white border-2 border-neutral-200 rounded-3xl p-5 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Target className="w-5 h-5 text-[#ff9600]" />
            <h3 className="font-extrabold text-sm uppercase tracking-wider text-neutral-700">
              Daily Goal
            </h3>
          </div>
          {isGoalCompleted && (
            <span className="flex items-center gap-1 text-xs font-black text-[#58cc02]">
              <CheckCircle2 className="w-4 h-4" />
              Done
            </span>
          )}
        </div>

        <p className="text-xs text-neutral-500 mb-3">
          Earn {dailyGoal} XP today to keep your daily streak alive!
        </p>

        {/* Progress bar */}
        <div className="w-full bg-neutral-200 h-4 rounded-full overflow-hidden p-0.5 mb-2">
          <div
            className={`h-full rounded-full transition-all duration-500 ${
              isGoalCompleted ? "bg-[#58cc02]" : "bg-[#ff9600]"
            }`}
            style={{ width: `${progressPercent}%` }}
          />
        </div>

        <div className="flex justify-between items-center text-xs font-black text-neutral-500">
          <span>{dailyProgress} XP</span>
          <span>{dailyGoal} XP</span>
        </div>
      </div>

      {/* Hearts / Practice Card */}
      <div className="bg-white border-2 border-neutral-200 rounded-3xl p-5 shadow-sm">
        <div className="flex items-center gap-2 mb-2">
          <Heart className="w-5 h-5 text-[#ff4b4b] fill-[#ff4b4b]" />
          <h3 className="font-extrabold text-sm uppercase tracking-wider text-neutral-700">
            Hearts: {profile?.hearts ?? 5} / 5
          </h3>
        </div>
        <p className="text-xs text-neutral-500 mb-4">
          Need more hearts to continue learning? Practice or refill instantly.
        </p>
        <button
          onClick={onRefillClick}
          className="btn-3d btn-duo-blue w-full py-2.5 text-xs flex items-center justify-center gap-1.5"
        >
          <Sparkles className="w-4 h-4 text-yellow-300 fill-yellow-300" />
          Refill Hearts
        </button>
      </div>

      {/* Leaderboard Sneak Peek */}
      <div className="bg-white border-2 border-neutral-200 rounded-3xl p-5 shadow-sm">
        <div className="flex items-center justify-between mb-3">
          <div className="flex items-center gap-2">
            <Trophy className="w-5 h-5 text-[#ffc800]" />
            <h3 className="font-extrabold text-sm uppercase tracking-wider text-neutral-700">
              {profile?.league || "Bronze"} League
            </h3>
          </div>
          <Link
            href="/leaderboard"
            className="text-xs font-black text-[#1cb0f6] hover:underline flex items-center gap-0.5"
          >
            View <ArrowRight className="w-3 h-3" />
          </Link>
        </div>
        <p className="text-xs text-neutral-500 mb-3">
          You are currently ranked #{profile?.rank || 5} with {profile?.xp || 0} XP!
        </p>
        <Link
          href="/leaderboard"
          className="btn-3d btn-duo-gray w-full py-2.5 text-xs text-center block"
        >
          Check Leaderboard
        </Link>
      </div>
    </div>
  );
};
