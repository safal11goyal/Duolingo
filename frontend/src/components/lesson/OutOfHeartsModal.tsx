"use client";

import React, { useState } from "react";
import { useRouter } from "next/navigation";
import { Heart, Sparkles, Plus, LogOut } from "lucide-react";
import { DuoMascot } from "../ui/DuoMascot";
import { refillHearts, practiceHearts } from "@/lib/api";

interface OutOfHeartsModalProps {
  onRefilled: (hearts: number) => void;
}

export const OutOfHeartsModal: React.FC<OutOfHeartsModalProps> = ({ onRefilled }) => {
  const router = useRouter();
  const [loading, setLoading] = useState(false);

  const handleRefill = async () => {
    setLoading(true);
    try {
      const res = await refillHearts();
      onRefilled(res.hearts);
    } catch (err: any) {
      alert(err.message || "Failed to refill hearts");
    } finally {
      setLoading(false);
    }
  };

  const handlePractice = async () => {
    setLoading(true);
    try {
      const res = await practiceHearts();
      onRefilled(res.hearts);
    } catch (err: any) {
      alert(err.message || "Failed to practice");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/60 backdrop-blur-sm flex items-center justify-center p-4 animate-pop select-none">
      <div className="bg-white rounded-3xl max-w-md w-full p-8 text-center shadow-2xl border-2 border-neutral-200">
        {/* Sad Duo Mascot */}
        <div className="flex justify-center mb-4">
          <DuoMascot size={110} expression="sad" />
        </div>

        <div className="inline-flex items-center gap-2 px-3 py-1 bg-red-100 text-[#ff4b4b] rounded-full text-xs font-black uppercase tracking-wider mb-3">
          <Heart className="w-4 h-4 fill-[#ff4b4b]" />
          0 Hearts Left
        </div>

        <h3 className="text-2xl sm:text-3xl font-black text-neutral-800 mb-2">
          You ran out of hearts!
        </h3>
        <p className="text-neutral-500 text-sm mb-8 max-w-xs mx-auto">
          You made a few mistakes along the way. Practice or refill your hearts to keep learning right now.
        </p>

        <div className="space-y-3">
          <button
            disabled={loading}
            onClick={handleRefill}
            className="btn-3d btn-duo-green w-full py-4 text-base flex items-center justify-center gap-2"
          >
            <Sparkles className="w-5 h-5 text-yellow-300 fill-yellow-300" />
            Super Refill (Full 5 Hearts)
          </button>

          <button
            disabled={loading}
            onClick={handlePractice}
            className="btn-3d btn-duo-blue w-full py-3.5 text-sm flex items-center justify-center gap-2"
          >
            <Plus className="w-5 h-5" />
            Quick Practice (+1 Heart)
          </button>

          <button
            onClick={() => router.push("/learn")}
            className="btn-3d btn-duo-gray w-full py-3 text-xs flex items-center justify-center gap-2"
          >
            <LogOut className="w-4 h-4" />
            Return to Learning Path
          </button>
        </div>
      </div>
    </div>
  );
};
