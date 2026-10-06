"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { Home, Trophy, User as UserIcon, Settings } from "lucide-react";

export const MobileNav: React.FC = () => {
  const pathname = usePathname();

  const navItems = [
    { label: "Learn", href: "/learn", icon: Home },
    { label: "Ranks", href: "/leaderboard", icon: Trophy },
    { label: "Profile", href: "/profile", icon: UserIcon },
    { label: "Settings", href: "/settings", icon: Settings },
  ];

  return (
    <nav className="md:hidden fixed bottom-0 left-0 right-0 h-16 bg-white border-t-2 border-neutral-200 flex items-center justify-around px-2 z-40">
      {navItems.map((item) => {
        const isActive = pathname === item.href || (item.href === "/learn" && pathname === "/");
        const Icon = item.icon;

        return (
          <Link
            key={item.href}
            href={item.href}
            className={`flex flex-col items-center justify-center p-2 rounded-xl transition-all ${
              isActive ? "text-[#1cb0f6]" : "text-neutral-400"
            }`}
          >
            <Icon className="w-6 h-6" strokeWidth={isActive ? 2.5 : 2} />
            <span className="text-[10px] font-bold mt-0.5">{item.label}</span>
          </Link>
        );
      })}
    </nav>
  );
};
