"use client";

import React, { useState, useRef, useEffect } from "react";
import Link from "next/link";
import { Flame, Gem, Heart, Plus, Sparkles, X, User as UserIcon, Settings, LogOut } from "lucide-react";
import { User } from "@/lib/types";
import { refillHearts, practiceHearts } from "@/lib/api";
import { useAuth } from "@/context/AuthContext";

interface TopHeaderProps {
  user: User | null;
  onUserUpdate?: () => void;
}

export const TopHeader: React.FC<TopHeaderProps> = ({ user, onUserUpdate }) => {
  const { logout } = useAuth();
  const [showHeartsModal, setShowHeartsModal] = useState(false);
  const [showUserMenu, setShowUserMenu] = useState(false);
  const [loadingAction, setLoadingAction] = useState(false);
  const menuRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (menuRef.current && !menuRef.current.contains(event.target as Node)) {
        setShowUserMenu(false);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleRefill = async () => {
    setLoadingAction(true);
    try {
      await refillHearts();
      if (onUserUpdate) onUserUpdate();
      setShowHeartsModal(false);
    } catch (err: any) {
      alert(err.message || "Failed to refill hearts");
    } finally {
      setLoadingAction(false);
    }
  };

  const handlePractice = async () => {
    setLoadingAction(true);
    try {
      await practiceHearts();
      if (onUserUpdate) onUserUpdate();
      setShowHeartsModal(false);
    } catch (err: any) {
      alert(err.message || "Failed to practice");
    } finally {
      setLoadingAction(false);
    }
  };

  return (
    <>
      <header className="sticky top-0 bg-white/95 backdrop-blur-sm border-b-2 border-neutral-200 z-30 px-4 md:px-8 py-3 flex items-center justify-between select-none">
        {/* Left: Language Indicator */}
        <div className="flex items-center gap-2.5">
          <div className="w-8 h-6 rounded-md shadow-sm overflow-hidden flex flex-col border border-neutral-300">
            <div className="h-1/4 bg-[#aa151b]" />
            <div className="h-2/4 bg-[#f1bf00] flex items-center justify-center">
              <div className="w-1.5 h-1.5 bg-[#aa151b] rounded-full" />
            </div>
            <div className="h-1/4 bg-[#aa151b]" />
          </div>
          <span className="font-extrabold text-xs uppercase tracking-wider text-neutral-600 hidden sm:inline">
            Spanish
          </span>
        </div>

        {/* Right: Gamification Badges */}
        <div className="flex items-center gap-3 sm:gap-6">
          {/* Streak */}
          <div
            className="flex items-center gap-1.5 font-extrabold text-sm sm:text-base text-[#ff9600] cursor-pointer hover:opacity-80 transition-opacity"
            title={`${user?.streak || 0} day streak`}
          >
            <Flame className="w-6 h-6 fill-[#ff9600] animate-bounce-gentle" />
            <span>{user?.streak || 0}</span>
          </div>

          {/* Gems */}
          <div
            className="flex items-center gap-1.5 font-extrabold text-sm sm:text-base text-[#1cb0f6] cursor-pointer hover:opacity-80 transition-opacity"
            title={`${user?.gems || 500} gems`}
          >
            <Gem className="w-6 h-6 fill-[#1cb0f6]" />
            <span>{user?.gems || 500}</span>
          </div>

          {/* Hearts */}
          <button
            onClick={() => setShowHeartsModal(true)}
            className="flex items-center gap-1.5 font-extrabold text-sm sm:text-base text-[#ff4b4b] hover:scale-105 active:scale-95 transition-all p-1 rounded-xl"
            title="Hearts remaining - Click to refill"
          >
            <Heart className="w-6 h-6 fill-[#ff4b4b]" />
            <span>{user?.hearts ?? 5}</span>
          </button>

          {/* Profile Avatar & Dropdown */}
          <div className="relative" ref={menuRef}>
            <button
              onClick={() => setShowUserMenu(!showUserMenu)}
              className="w-9 h-9 rounded-full bg-gradient-to-tr from-[#58cc02] to-[#2ce308] border-2 border-white shadow flex items-center justify-center text-white font-black text-sm hover:scale-105 transition-transform cursor-pointer focus:outline-none"
              title={user?.display_name || "Profile menu"}
              aria-label="User menu"
            >
              {user?.display_name ? user.display_name.charAt(0) : "A"}
            </button>

            {showUserMenu && (
              <div className="absolute right-0 mt-2 w-52 bg-white rounded-2xl shadow-xl border-2 border-neutral-200 py-2 z-50 animate-pop">
                <div className="px-4 py-2 border-b border-neutral-100">
                  <p className="font-black text-sm text-neutral-800 truncate">
                    {user?.display_name || "Learner"}
                  </p>
                  <p className="font-bold text-xs text-neutral-400 truncate">
                    {user?.email || `@${user?.username || "user"}`}
                  </p>
                </div>

                <div className="py-1">
                  <Link
                    href="/profile"
                    onClick={() => setShowUserMenu(false)}
                    className="flex items-center gap-3 px-4 py-2.5 text-xs font-black text-neutral-700 hover:bg-neutral-100 transition-colors"
                  >
                    <UserIcon className="w-4 h-4 text-[#1cb0f6]" />
                    Profile
                  </Link>

                  <Link
                    href="/settings"
                    onClick={() => setShowUserMenu(false)}
                    className="flex items-center gap-3 px-4 py-2.5 text-xs font-black text-neutral-700 hover:bg-neutral-100 transition-colors"
                  >
                    <Settings className="w-4 h-4 text-neutral-500" />
                    Settings
                  </Link>
                </div>

                <div className="border-t border-neutral-100 pt-1">
                  <button
                    onClick={() => {
                      setShowUserMenu(false);
                      if (confirm("Are you sure you want to log out?")) {
                        logout();
                      }
                    }}
                    className="w-full flex items-center gap-3 px-4 py-2.5 text-xs font-black text-[#ff4b4b] hover:bg-red-50 transition-colors text-left"
                  >
                    <LogOut className="w-4 h-4 text-[#ff4b4b]" />
                    Log Out
                  </button>
                </div>
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Hearts Dialog Modal */}
      {showHeartsModal && (
        <div className="fixed inset-0 bg-black/50 z-50 flex items-center justify-center p-4 animate-pop">
          <div className="bg-white rounded-3xl max-w-sm w-full p-6 shadow-2xl border-2 border-neutral-200 relative text-center">
            <button
              onClick={() => setShowHeartsModal(false)}
              className="absolute top-4 right-4 p-2 text-neutral-400 hover:text-neutral-700 rounded-full hover:bg-neutral-100 transition-colors"
            >
              <X className="w-5 h-5" />
            </button>

            <div className="flex justify-center mb-4">
              <div className="relative">
                <Heart className="w-20 h-20 text-[#ff4b4b] fill-[#ff4b4b] animate-pulse" />
                <span className="absolute inset-0 flex items-center justify-center text-white font-black text-2xl pt-1">
                  {user?.hearts ?? 5}
                </span>
              </div>
            </div>

            <h3 className="text-2xl font-black text-neutral-800 mb-2">Hearts Status</h3>
            <p className="text-neutral-500 text-sm mb-6">
              You lose hearts when answering incorrectly. Practice or use your gems to restore them!
            </p>

            <div className="space-y-3">
              <button
                disabled={loadingAction || (user?.hearts ?? 0) >= 5}
                onClick={handleRefill}
                className="btn-3d btn-duo-green w-full py-3 text-sm flex items-center justify-center gap-2"
              >
                <Sparkles className="w-5 h-5 text-yellow-300 fill-yellow-300" />
                Refill to Full (5 Hearts)
              </button>

              <button
                disabled={loadingAction || (user?.hearts ?? 0) >= 5}
                onClick={handlePractice}
                className="btn-3d btn-duo-blue w-full py-3 text-sm flex items-center justify-center gap-2"
              >
                <Plus className="w-5 h-5" />
                Practice for +1 Heart
              </button>
            </div>
          </div>
        </div>
      )}
    </>
  );
};
