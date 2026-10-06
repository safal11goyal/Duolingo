import React from "react";
import { BookOpen } from "lucide-react";

interface UnitHeaderProps {
  orderIndex: number;
  title: string;
  description: string;
}

export const UnitHeader: React.FC<UnitHeaderProps> = ({ orderIndex, title, description }) => {
  // Theme colors based on unit
  const colorStyles = [
    { bg: "bg-[#58cc02]", border: "border-[#46a302]" },
    { bg: "bg-[#1cb0f6]", border: "border-[#1899d6]" },
    { bg: "bg-[#ce82ff]", border: "border-[#a55eea]" },
  ][(orderIndex - 1) % 3];

  return (
    <div
      className={`w-full max-w-xl mx-auto rounded-2xl p-5 mb-8 text-white ${colorStyles.bg} shadow-md border-b-4 ${colorStyles.border} flex items-center justify-between select-none`}
    >
      <div>
        <span className="text-xs font-black uppercase tracking-widest opacity-90 block mb-1">
          {title.split(":")[0]}
        </span>
        <h2 className="text-xl font-black tracking-tight leading-snug">
          {title.split(":")[1]?.trim() || title}
        </h2>
        <p className="text-xs font-semibold opacity-90 mt-1 max-w-md">
          {description}
        </p>
      </div>

      <button
        onClick={() => alert(`Guidebook for ${title}`)}
        className="hidden sm:flex items-center gap-2 px-3 py-2 bg-white/20 hover:bg-white/30 rounded-xl text-xs font-black tracking-wider uppercase transition-all backdrop-blur-sm"
      >
        <BookOpen className="w-4 h-4" />
        Guide
      </button>
    </div>
  );
};
