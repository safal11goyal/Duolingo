"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Trophy, User as UserIcon, Settings, Sparkles, LogOut } from "lucide-react";
import { DuoMascot } from "../ui/DuoMascot";
import { useAuth } from "@/context/AuthContext";

export const Sidebar: React.FC = () => {
  const { user, logout } = useAuth();
  const pathname = usePathname();

  const navItems = [
    { label: "LEARN", href: "/learn", icon: Home },
    { label: "LEADERBOARDS", href: "/leaderboard", icon: Trophy },
    { label: "PROFILE", href: "/profile", icon: UserIcon },
    { label: "SETTINGS", href: "/settings", icon: Settings },
  ];

  return (
    <aside className="hidden md:flex flex-col w-64 h-screen fixed left-0 top-0 border-r-2 border-neutral-200 bg-white px-4 py-6 z-40 select-none">
      {/* Brand Header */}
      <Link href="/learn" className="flex items-center gap-3 px-3 mb-8 group">
        <DuoMascot size={42} expression="happy" />
        <span className="text-2xl font-black tracking-tight text-[#58cc02] group-hover:scale-105 transition-transform">
          duolingo
        </span>
      </Link>

      {/* Navigation List */}
      <nav className="flex-1 space-y-2">
        {navItems.map((item) => {
          const isActive = pathname === item.href || (item.href === "/learn" && pathname === "/");
          const Icon = item.icon;

          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center gap-4 px-4 py-3.5 rounded-2xl font-bold text-sm tracking-wide transition-all border-2 ${
                isActive
                  ? "bg-[#ddf4ff] text-[#1cb0f6] border-[#84d8ff]"
                  : "text-neutral-500 border-transparent hover:bg-neutral-100"
              }`}
            >
              <Icon
                className={`w-6 h-6 ${
                  isActive ? "text-[#1cb0f6]" : "text-neutral-400"
                }`}
                strokeWidth={2.5}
              />
              {item.label}
            </Link>
          );
        })}
      </nav>

      {/* Super Duolingo Badge */}
      <div className="mt-auto p-4 rounded-2xl bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-sm">
        <div className="flex items-center gap-2 mb-1.5">
          <Sparkles className="w-5 h-5 text-yellow-300 fill-yellow-300" />
          <span className="font-extrabold text-sm tracking-wide">SUPER DUO</span>
        </div>
        <p className="text-xs text-indigo-100 mb-3">
          Unlimited hearts & personalized practice!
        </p>
        <button
          onClick={() => alert("Super Duolingo is active for demo!")}
          className="w-full py-2 px-3 bg-white text-indigo-600 rounded-xl font-bold text-xs uppercase tracking-wider hover:bg-neutral-50 active:scale-95 transition-all shadow"
        >
          Active
        </button>
      </div>

      {/* User Info & Logout Button */}
      {user && (
        <div className="mt-3 pt-3 border-t border-neutral-200 flex items-center justify-between">
          <Link href="/profile" className="flex items-center gap-2.5 overflow-hidden group">
            <div className="w-8 h-8 rounded-full bg-gradient-to-tr from-[#58cc02] to-[#2ce308] border border-white shadow-sm flex items-center justify-center text-white font-black text-xs shrink-0 group-hover:scale-105 transition-transform">
              {user.display_name ? user.display_name.charAt(0) : "A"}
            </div>
            <div className="overflow-hidden">
              <span className="block font-black text-xs text-neutral-800 truncate group-hover:text-[#1cb0f6] transition-colors">
                {user.display_name}
              </span>
              <span className="block text-[10px] font-bold text-neutral-400 truncate">
                @{user.username}
              </span>
            </div>
          </Link>
          <button
            onClick={() => {
              if (confirm("Are you sure you want to log out?")) {
                logout();
              }
            }}
            title="Log out"
            aria-label="Log out"
            className="p-1.5 text-neutral-400 hover:text-[#ff4b4b] hover:bg-red-50 rounded-xl transition-colors shrink-0"
          >
            <LogOut className="w-4 h-4" />
          </button>
        </div>
      )}
    </aside>
  );
};
