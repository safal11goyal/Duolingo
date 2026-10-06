"use client";

import React, { useState, useEffect } from "react";
import { Volume2, Target, Globe, Trash2, Check } from "lucide-react";
import { User } from "@/lib/types";
import { fetchCurrentUser, updateDailyGoal, resetProgress } from "@/lib/api";
import { Sidebar } from "@/components/layout/Sidebar";
import { MobileNav } from "@/components/layout/MobileNav";
import { TopHeader } from "@/components/layout/TopHeader";
import { ProtectedRoute } from "@/components/auth/ProtectedRoute";
import { useAuth } from "@/context/AuthContext";
import { sounds } from "@/lib/sound";

export default function SettingsPage() {
  const { logout } = useAuth();
  const [user, setUser] = useState<User | null>(null);
  const [soundEnabled, setSoundEnabled] = useState(true);
  const [goal, setGoal] = useState(20);
  const [savingGoal, setSavingGoal] = useState(false);
  const [savedGoalSuccess, setSavedGoalSuccess] = useState(false);

  useEffect(() => {
    fetchCurrentUser().then((u) => {
      setUser(u);
      setGoal(u.daily_goal);
    }).catch(console.error);
  }, []);

  const handleToggleSound = () => {
    sounds.enabled = !soundEnabled;
    setSoundEnabled(!soundEnabled);
    if (!soundEnabled) {
      sounds.playClick();
    }
  };

  const handleGoalChange = async (newGoal: number) => {
    setGoal(newGoal);
    setSavingGoal(true);
    try {
      await updateDailyGoal(newGoal);
      setSavedGoalSuccess(true);
      setTimeout(() => setSavedGoalSuccess(false), 2000);
    } catch (err: any) {
      alert(err.message || "Failed to update daily goal");
    } finally {
      setSavingGoal(false);
    }
  };

  const handleReset = async () => {
    if (!confirm("Are you sure you want to reset all your progress?")) return;
    try {
      await resetProgress();
      alert("Progress reset to 0!");
      window.location.href = "/learn";
    } catch (err: any) {
      alert(err.message || "Failed to reset");
    }
  };

  const goalOptions = [
    { label: "Casual", xp: 10, time: "5 mins / day" },
    { label: "Regular", xp: 20, time: "10 mins / day" },
    { label: "Serious", xp: 30, time: "15 mins / day" },
    { label: "Intense", xp: 50, time: "25 mins / day" },
  ];

  return (
    <ProtectedRoute>
      <div className="min-h-screen bg-white md:bg-[#f7f7f7] flex select-none">
        <Sidebar />

      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        <TopHeader user={user} />

        <main className="flex-1 max-w-2xl mx-auto w-full px-4 sm:px-6 py-8 space-y-8">
          <h1 className="text-2xl sm:text-3xl font-black text-neutral-800">Settings</h1>

          {/* Daily Goal Selection */}
          <div className="bg-white border-2 border-neutral-200 rounded-3xl p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-2">
              <Target className="w-6 h-6 text-[#ff9600]" />
              <h2 className="text-lg font-black text-neutral-800">Daily Learning Goal</h2>
            </div>
            <p className="text-xs text-neutral-500 mb-6">
              Set how much XP you want to earn each day. Your goal helps you stay committed.
            </p>

            <div className="space-y-3">
              {goalOptions.map((opt) => {
                const isSelected = goal === opt.xp;
                return (
                  <button
                    key={opt.xp}
                    onClick={() => handleGoalChange(opt.xp)}
                    className={`w-full p-4 rounded-2xl border-2 flex items-center justify-between transition-all ${
                      isSelected
                        ? "bg-[#ddf4ff] border-[#1cb0f6] border-b-4 text-[#1899d6]"
                        : "bg-white border-neutral-200 border-b-4 hover:bg-neutral-50 text-neutral-700"
                    }`}
                  >
                    <div className="text-left">
                      <span className="font-extrabold text-base block">{opt.label}</span>
                      <span className="text-xs font-semibold text-neutral-400">{opt.time}</span>
                    </div>
                    <span className="font-black text-base">
                      {opt.xp} XP / day
                    </span>
                  </button>
                );
              })}
            </div>

            {savedGoalSuccess && (
              <p className="text-xs font-black text-[#58cc02] mt-3 flex items-center gap-1">
                <Check className="w-4 h-4" /> Daily goal updated successfully!
              </p>
            )}
          </div>

          {/* Sound & Audio */}
          <div className="bg-white border-2 border-neutral-200 rounded-3xl p-6 shadow-sm">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-3">
                <Volume2 className="w-6 h-6 text-[#1cb0f6]" />
                <div>
                  <h3 className="text-base font-black text-neutral-800">Sound Effects</h3>
                  <p className="text-xs text-neutral-500">Play audio chimes during lessons</p>
                </div>
              </div>
              <button
                onClick={handleToggleSound}
                className={`w-14 h-8 rounded-full p-1 transition-colors ${
                  soundEnabled ? "bg-[#58cc02]" : "bg-neutral-300"
                }`}
              >
                <div
                  className={`w-6 h-6 rounded-full bg-white shadow-sm transform transition-transform ${
                    soundEnabled ? "translate-x-6" : "translate-x-0"
                  }`}
                />
              </button>
            </div>
          </div>

          {/* Language Course */}
          <div className="bg-white border-2 border-neutral-200 rounded-3xl p-6 shadow-sm">
            <div className="flex items-center gap-3 mb-2">
              <Globe className="w-6 h-6 text-[#58cc02]" />
              <h3 className="text-base font-black text-neutral-800">Active Course</h3>
            </div>
            <p className="text-xs text-neutral-500 mb-4">
              Spanish (from English) - Other languages coming soon!
            </p>
            <div className="flex items-center gap-3 p-3 bg-neutral-50 rounded-2xl border border-neutral-200">
              <div className="w-7 h-5 rounded overflow-hidden flex flex-col border border-neutral-300">
                <div className="h-1/4 bg-[#aa151b]" />
                <div className="h-2/4 bg-[#f1bf00]" />
                <div className="h-1/4 bg-[#aa151b]" />
              </div>
              <span className="font-extrabold text-sm text-neutral-700">Spanish</span>
              <span className="ml-auto text-xs font-black text-[#58cc02] uppercase">Active</span>
            </div>
          </div>

          {/* Account & Logout */}
          <div className="bg-white border-2 border-neutral-200 rounded-3xl p-6 shadow-sm">
            <h3 className="text-base font-black text-neutral-800 mb-1">Account</h3>
            <p className="text-xs text-neutral-500 mb-4">
              Signed in as <span className="font-extrabold text-neutral-700">{user?.email || user?.username}</span>
            </p>
            <button
              onClick={() => {
                if (confirm("Are you sure you want to log out?")) {
                  logout();
                }
              }}
              className="btn-3d btn-duo-gray py-2.5 px-6 text-xs text-red-600 border-red-200 hover:bg-red-50 uppercase font-black tracking-wide"
            >
              Log Out
            </button>
          </div>

          {/* Reset Danger Zone */}
          <div className="bg-red-50 border-2 border-red-200 rounded-3xl p-6 shadow-sm">
            <div className="flex items-center gap-2 mb-2">
              <Trash2 className="w-5 h-5 text-red-600" />
              <h3 className="font-extrabold text-sm uppercase tracking-wider text-red-900">
                Danger Zone
              </h3>
            </div>
            <p className="text-xs text-red-700 mb-4">
              Reset all learner progress back to zero. Useful for demoing from scratch.
            </p>
            <button
              onClick={handleReset}
              className="btn-3d btn-duo-red py-2.5 px-6 text-xs"
            >
              Reset Learner Progress
            </button>
          </div>
        </main>
      </div>

      <MobileNav />
    </div>
    </ProtectedRoute>
  );
}
