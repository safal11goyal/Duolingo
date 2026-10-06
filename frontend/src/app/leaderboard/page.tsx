"use client";

import React, { useState, useEffect } from "react";
import { Trophy, Shield, Sparkles } from "lucide-react";
import { User, LeaderboardEntry } from "@/lib/types";
import { fetchCurrentUser, fetchLeaderboard } from "@/lib/api";
import { Sidebar } from "@/components/layout/Sidebar";
import { MobileNav } from "@/components/layout/MobileNav";
import { TopHeader } from "@/components/layout/TopHeader";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";

export default function LeaderboardPage() {
  const [user, setUser] = useState<User | null>(null);
  const [leaderboard, setLeaderboard] = useState<LeaderboardEntry[]>([]);
  const [loading, setLoading] = useState(true);

  const loadData = async () => {
    try {
      setLoading(true);
      const [u, lb] = await Promise.all([
        fetchCurrentUser(),
        fetchLeaderboard()
      ]);
      setUser(u);
      setLeaderboard(lb);
    } catch (err: any) {
      console.error("Failed to load leaderboard:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const getRankBadge = (rank: number) => {
    if (rank === 1) return <span className="text-2xl" title="1st Place">🥇</span>;
    if (rank === 2) return <span className="text-2xl" title="2nd Place">🥈</span>;
    if (rank === 3) return <span className="text-2xl" title="3rd Place">🥉</span>;
    return <span className="w-8 text-center font-black text-neutral-400 text-base">{rank}</span>;
  };

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-white md:bg-[#f7f7f7] flex select-none">
        <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader user={user} onUserUpdate={loadData} />

        <main className="flex-1 max-w-2xl mx-auto w-full px-4 sm:px-6 py-8">
          {/* League Tier Header */}
          <div className="bg-gradient-to-r from-purple-600 to-indigo-600 rounded-3xl p-6 text-white shadow-md mb-8 text-center relative overflow-hidden">
            <div className="flex justify-center mb-2">
              <div className="w-16 h-16 rounded-full bg-white/20 backdrop-blur-md flex items-center justify-center border-2 border-white/40 shadow-inner">
                <Shield className="w-9 h-9 text-yellow-300 fill-yellow-300" />
              </div>
            </div>
            <h1 className="text-2xl sm:text-3xl font-black tracking-tight">
              Obsidian League
            </h1>
            <p className="text-xs sm:text-sm text-purple-200 mt-1 max-w-sm mx-auto">
              Top 3 advance to Diamond League! Complete lessons to earn XP and rise through the ranks.
            </p>
          </div>

          {/* Leaderboard List */}
          <div className="bg-white border-2 border-neutral-200 rounded-3xl shadow-sm overflow-hidden">
            <div className="px-6 py-4 border-b-2 border-neutral-100 flex items-center justify-between text-xs font-black text-neutral-400 uppercase tracking-wider">
              <span>Rank & Learner</span>
              <span>Total XP</span>
            </div>

            {loading ? (
              <div className="py-16 flex flex-col items-center justify-center">
                <div className="w-10 h-10 border-4 border-[#1cb0f6] border-t-transparent rounded-full animate-spin mb-3" />
                <p className="text-xs font-bold text-neutral-400">Loading standings...</p>
              </div>
            ) : (
              <div className="divide-y-2 divide-neutral-100">
                {leaderboard.map((entry) => (
                  <div
                    key={entry.user_id}
                    className={`px-6 py-4 flex items-center justify-between transition-colors ${
                      entry.is_current_user
                        ? "bg-[#ddf4ff] font-extrabold border-l-4 border-l-[#1cb0f6]"
                        : "hover:bg-neutral-50"
                    }`}
                  >
                    {/* Rank & User */}
                    <div className="flex items-center gap-4">
                      <div className="w-8 flex items-center justify-center">
                        {getRankBadge(entry.rank)}
                      </div>

                      {/* Avatar */}
                      <div
                        className={`w-11 h-11 rounded-full flex items-center justify-center font-black text-white text-base shadow-sm ${
                          entry.is_current_user
                            ? "bg-gradient-to-tr from-[#58cc02] to-[#2ce308]"
                            : "bg-gradient-to-tr from-neutral-400 to-neutral-500"
                        }`}
                      >
                        {entry.display_name.charAt(0)}
                      </div>

                      <div>
                        <div className="flex items-center gap-2">
                          <span
                            className={`text-base ${
                              entry.is_current_user
                                ? "text-[#1899d6] font-black"
                                : "text-neutral-800 font-extrabold"
                            }`}
                          >
                            {entry.display_name}
                          </span>
                          {entry.is_current_user && (
                            <span className="text-[10px] font-black uppercase px-2 py-0.5 rounded-full bg-[#1cb0f6] text-white">
                              You
                            </span>
                          )}
                        </div>
                        <span className="text-xs text-neutral-400 font-semibold">
                          @{entry.username}
                        </span>
                      </div>
                    </div>

                    {/* XP Score */}
                    <div className="text-right">
                      <span className="font-black text-base text-neutral-700">
                        {entry.xp.toLocaleString()} XP
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </main>
      </div>

        <MobileNav />
      </div>
    </ProtectedRoute>
  );
}
