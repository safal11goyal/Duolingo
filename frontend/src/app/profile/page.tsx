"use client";

import React, { useState, useEffect } from "react";
import {
  Flame,
  Zap,
  Crown,
  BookOpen,
  Calendar,
  Trophy,
  Award,
  Clock,
  Sparkles,
  RotateCcw
} from "lucide-react";
import { User, UserProfile, Achievement } from "@/lib/types";
import { fetchCurrentUser, fetchUserProfile, fetchAchievements, simulateActivity, resetProgress } from "@/lib/api";
import { Sidebar } from "@/components/layout/Sidebar";
import { MobileNav } from "@/components/layout/MobileNav";
import { TopHeader } from "@/components/layout/TopHeader";

export default function ProfilePage() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [achievements, setAchievements] = useState<Achievement[]>([]);
  const [loading, setLoading] = useState(true);

  // Dev simulation tool states
  const [simDate, setSimDate] = useState(() => {
    const d = new Date();
    d.setDate(d.getDate() + 1);
    return d.toISOString().split("T")[0];
  });
  const [simLoading, setSimLoading] = useState(false);

  const loadData = async () => {
    try {
      setLoading(true);
      const [u, prof, achs] = await Promise.all([
        fetchCurrentUser(),
        fetchUserProfile(),
        fetchAchievements()
      ]);
      setUser(u);
      setProfile(prof);
      setAchievements(achs);
    } catch (err: any) {
      console.error("Failed to load profile:", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSimulateDate = async () => {
    try {
      setSimLoading(true);
      await simulateActivity(simDate, 20);
      alert(`Simulated activity on ${simDate}! Streak updated.`);
      await loadData();
    } catch (err: any) {
      alert(err.message || "Failed to simulate date");
    } finally {
      setSimLoading(false);
    }
  };

  const handleReset = async () => {
    if (!confirm("Are you sure you want to reset all learner progress back to 0 for demo?")) return;
    try {
      await resetProgress();
      await loadData();
      alert("Progress reset!");
    } catch (err: any) {
      alert(err.message || "Failed to reset");
    }
  };

  const getAchIcon = (iconName: string) => {
    switch (iconName) {
      case "flame":
        return <Flame className="w-6 h-6 text-[#ff9600]" />;
      case "award":
        return <Award className="w-6 h-6 text-[#ffc800]" />;
      case "book-open":
        return <BookOpen className="w-6 h-6 text-[#1cb0f6]" />;
      case "crown":
        return <Crown className="w-6 h-6 text-[#ce82ff]" />;
      case "calendar":
        return <Calendar className="w-6 h-6 text-[#58cc02]" />;
      default:
        return <Trophy className="w-6 h-6 text-[#ffc800]" />;
    }
  };

  return (
    <div className="min-h-screen bg-white md:bg-[#f7f7f7] flex select-none">
      <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader user={user} onUserUpdate={loadData} />

        <main className="flex-1 max-w-4xl mx-auto w-full px-4 sm:px-8 py-8 space-y-8">
          {/* User Card */}
          <div className="bg-white border-2 border-neutral-200 rounded-3xl p-6 sm:p-8 shadow-sm flex flex-col sm:flex-row items-center sm:items-start gap-6">
            <div className="w-24 h-24 sm:w-28 sm:h-28 rounded-full bg-gradient-to-tr from-[#58cc02] to-[#2ce308] border-4 border-white shadow-md flex items-center justify-center text-white font-black text-4xl">
              {profile?.display_name?.charAt(0) || "A"}
            </div>

            <div className="flex-1 text-center sm:text-left">
              <h1 className="text-2xl sm:text-3xl font-black text-neutral-800">
                {profile?.display_name || "Alex Rivera"}
              </h1>
              <p className="text-neutral-400 font-extrabold text-sm mb-3">
                @{profile?.username || "alex"} • Joined October 2026
              </p>

              <div className="flex flex-wrap items-center justify-center sm:justify-start gap-3">
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-orange-50 border border-orange-200 text-[#ff9600] font-black text-xs uppercase">
                  <Flame className="w-4 h-4 fill-[#ff9600]" />
                  {profile?.streak || 0} Day Streak
                </span>
                <span className="inline-flex items-center gap-1.5 px-3 py-1.5 rounded-full bg-purple-50 border border-purple-200 text-purple-700 font-black text-xs uppercase">
                  <Trophy className="w-4 h-4 text-purple-600" />
                  {profile?.league || "Bronze"} League
                </span>
              </div>
            </div>
          </div>

          {/* Statistics Grid */}
          <div className="space-y-3">
            <h2 className="text-xl font-black text-neutral-800">Statistics</h2>

            <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
              {/* Day Streak */}
              <div className="bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
                <Flame className="w-8 h-8 text-[#ff9600] fill-[#ff9600] shrink-0" />
                <div>
                  <span className="block text-xl font-black text-neutral-800">{profile?.streak || 0}</span>
                  <span className="text-xs font-bold text-neutral-400 uppercase">Day Streak</span>
                </div>
              </div>

              {/* Total XP */}
              <div className="bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
                <Zap className="w-8 h-8 text-[#ffc800] fill-[#ffc800] shrink-0" />
                <div>
                  <span className="block text-xl font-black text-neutral-800">{profile?.xp || 0}</span>
                  <span className="text-xs font-bold text-neutral-400 uppercase">Total XP</span>
                </div>
              </div>

              {/* Crowns */}
              <div className="bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
                <Crown className="w-8 h-8 text-[#ce82ff] fill-[#ce82ff] shrink-0" />
                <div>
                  <span className="block text-xl font-black text-neutral-800">{profile?.crowns_count || 0}</span>
                  <span className="text-xs font-bold text-neutral-400 uppercase">Crowns</span>
                </div>
              </div>

              {/* Lessons Completed */}
              <div className="bg-white border-2 border-neutral-200 rounded-2xl p-4 shadow-sm flex items-center gap-3">
                <BookOpen className="w-8 h-8 text-[#1cb0f6] shrink-0" />
                <div>
                  <span className="block text-xl font-black text-neutral-800">{profile?.completed_lessons_count || 0}</span>
                  <span className="text-xs font-bold text-neutral-400 uppercase">Lessons</span>
                </div>
              </div>
            </div>
          </div>

          {/* Achievements Section */}
          <div className="space-y-4">
            <h2 className="text-xl font-black text-neutral-800">Achievements</h2>

            <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
              {achievements.map((ach) => {
                const percent = Math.min(100, Math.round((ach.progress / Math.max(1, ach.requirement_value)) * 100));

                return (
                  <div
                    key={ach.id}
                    className={`bg-white border-2 rounded-2xl p-5 shadow-sm flex items-start gap-4 transition-all ${
                      ach.unlocked ? "border-[#ffc800]" : "border-neutral-200 opacity-80"
                    }`}
                  >
                    <div
                      className={`w-14 h-14 rounded-2xl flex items-center justify-center shrink-0 border-2 ${
                        ach.unlocked
                          ? "bg-yellow-50 border-[#ffc800]"
                          : "bg-neutral-100 border-neutral-200"
                      }`}
                    >
                      {getAchIcon(ach.icon)}
                    </div>

                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-1">
                        <h4 className="font-black text-base text-neutral-800">{ach.name}</h4>
                        {ach.unlocked && (
                          <span className="text-[10px] font-black uppercase text-[#58cc02] bg-green-50 px-2 py-0.5 rounded-full border border-green-200">
                            Unlocked
                          </span>
                        )}
                      </div>
                      <p className="text-xs text-neutral-500 mb-3">{ach.description}</p>

                      {/* Progress bar */}
                      <div className="w-full bg-neutral-100 h-2.5 rounded-full overflow-hidden p-0.5">
                        <div
                          className={`h-full rounded-full transition-all duration-300 ${
                            ach.unlocked ? "bg-[#ffc800]" : "bg-[#1cb0f6]"
                          }`}
                          style={{ width: `${percent}%` }}
                        />
                      </div>
                      <span className="text-[10px] font-bold text-neutral-400 mt-1 block text-right">
                        {ach.progress} / {ach.requirement_value}
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>

          {/* Interactive Developer & Evaluation Tools */}
          <div className="bg-amber-50 border-2 border-amber-200 rounded-3xl p-6 shadow-sm">
            <div className="flex items-center gap-2 mb-2">
              <Sparkles className="w-5 h-5 text-amber-600" />
              <h3 className="font-extrabold text-sm uppercase tracking-wider text-amber-900">
                Interviewer / Dev Testing Tools
              </h3>
            </div>
            <p className="text-xs text-amber-700 mb-4">
              Test date progression and streak mechanics directly without waiting for real calendar days:
            </p>

            <div className="flex flex-wrap items-center gap-3 mb-4">
              <input
                type="date"
                value={simDate}
                onChange={(e) => setSimDate(e.target.value)}
                className="px-3 py-2 rounded-xl border border-amber-300 font-bold text-xs text-neutral-700 bg-white"
              />
              <button
                disabled={simLoading}
                onClick={handleSimulateDate}
                className="btn-3d btn-duo-blue py-2.5 px-4 text-xs"
              >
                {simLoading ? "Simulating..." : "Simulate Activity on Date"}
              </button>
              <button
                onClick={handleReset}
                className="btn-3d btn-duo-gray py-2.5 px-4 text-xs text-red-600 border-red-200 hover:bg-red-50 flex items-center gap-1.5"
              >
                <RotateCcw className="w-3.5 h-3.5" />
                Reset Progress
              </button>
            </div>
          </div>
        </main>
      </div>

      <MobileNav />
    </div>
  );
}
