"use client";

import React, { useState, useEffect } from "react";
import { User, UserProfile, LearningPath } from "@/lib/types";
import { fetchCurrentUser, fetchUserProfile, fetchLearningPath } from "@/lib/api";
import { Sidebar } from "@/components/layout/Sidebar";
import { MobileNav } from "@/components/layout/MobileNav";
import { TopHeader } from "@/components/layout/TopHeader";
import { UnitHeader } from "@/components/path/UnitHeader";
import { SkillNode } from "@/components/path/SkillNode";
import { PathRightSidebar } from "@/components/path/PathRightSidebar";

export default function LearnPage() {
  const [user, setUser] = useState<User | null>(null);
  const [profile, setProfile] = useState<UserProfile | null>(null);
  const [pathData, setPathData] = useState<LearningPath | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const loadData = async () => {
    try {
      setLoading(true);
      setError(null);
      const [u, prof, p] = await Promise.all([
        fetchCurrentUser(),
        fetchUserProfile(),
        fetchLearningPath()
      ]);
      setUser(u);
      setProfile(prof);
      setPathData(p);
    } catch (err: any) {
      setError(err.message || "Failed to load learning path.");
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  return (
    <div className="min-h-screen bg-white md:bg-[#f7f7f7] flex">
      {/* Desktop Left Sidebar */}
      <Sidebar />

      {/* Main Content Area */}
      <div className="flex-1 md:ml-64 flex flex-col min-h-screen pb-20 md:pb-8">
        {/* Top Header */}
        <TopHeader user={user} onUserUpdate={loadData} />

        {/* Learning Path and Right Sidebar Grid */}
        <div className="flex-1 max-w-6xl mx-auto w-full px-4 sm:px-6 py-8 flex justify-center">
          {loading ? (
            <div className="flex-1 flex flex-col items-center justify-center py-20">
              <div className="w-14 h-14 border-4 border-[#58cc02] border-t-transparent rounded-full animate-spin mb-4" />
              <p className="font-extrabold text-neutral-600">Loading your path...</p>
            </div>
          ) : error ? (
            <div className="flex-1 flex flex-col items-center justify-center py-20 text-center">
              <div className="w-14 h-14 rounded-full bg-red-100 text-[#ff4b4b] flex items-center justify-center text-xl font-black mb-3">
                !
              </div>
              <h3 className="text-xl font-black text-neutral-800 mb-1">Error Loading Course</h3>
              <p className="text-sm text-neutral-500 mb-4">{error}</p>
              <button onClick={loadData} className="btn-3d btn-duo-green px-6 py-2.5 text-xs">
                RETRY
              </button>
            </div>
          ) : (
            <>
              {/* Vertical Learning Path Column */}
              <div className="flex-1 max-w-xl flex flex-col items-center">
                {pathData?.units.map((unit) => (
                  <div key={unit.id} className="w-full mb-12 flex flex-col items-center">
                    {/* Unit Banner */}
                    <UnitHeader
                      orderIndex={unit.order_index}
                      title={unit.title}
                      description={unit.description}
                    />

                    {/* Skill Nodes in Curved Snake Formation */}
                    <div className="w-full flex flex-col items-center py-4">
                      {unit.skills.map((skill, sIdx) => (
                        <SkillNode
                          key={skill.id}
                          skill={skill}
                          index={sIdx}
                        />
                      ))}
                    </div>
                  </div>
                ))}
              </div>

              {/* Right Sidebar Widgets */}
              <PathRightSidebar
                profile={profile}
                onRefillClick={() => {
                  loadData();
                }}
              />
            </>
          )}
        </div>
      </div>

      {/* Mobile Bottom Navigation */}
      <MobileNav />
    </div>
  );
}
