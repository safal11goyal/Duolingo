"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, Sparkles, AlertCircle } from "lucide-react";
import { DuoMascot } from "@/components/ui/DuoMascot";
import { useAuth } from "@/context/AuthContext";

export default function LoginPage() {
  const router = useRouter();
  const { login, isAuthenticated, isLoading } = useAuth();

  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    if (!isLoading && isAuthenticated) {
      router.replace("/learn");
    }
  }, [isLoading, isAuthenticated, router]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!email.trim() || !password) {
      setError("Please enter both email and password.");
      return;
    }

    setError(null);
    setSubmitting(true);
    try {
      await login(email.trim(), password);
      router.push("/learn");
    } catch (err: any) {
      setError(err.message || "Invalid email or password.");
    } finally {
      setSubmitting(false);
    }
  };

  const handleDemoFill = () => {
    setEmail("demo@example.com");
    setPassword("Demo123!");
    setError(null);
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center">
        <DuoMascot size={90} expression="happy" className="animate-bounce" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white md:bg-[#f7f7f7] flex flex-col justify-center items-center px-4 py-8 select-none">
      <div className="w-full max-w-md bg-white md:border-2 md:border-neutral-200 md:rounded-3xl p-6 sm:p-8 md:shadow-sm">
        {/* Mascot & Brand Header */}
        <div className="flex flex-col items-center mb-6 text-center">
          <DuoMascot size={80} expression="happy" />
          <span className="text-2xl font-black text-[#58cc02] tracking-tight mt-2">
            duolingo
          </span>
          <h1 className="text-2xl font-black text-neutral-800 mt-2">
            Welcome back!
          </h1>
          <p className="text-xs sm:text-sm text-neutral-500 font-bold mt-1">
            Log in to continue your streak and lessons
          </p>
        </div>

        {/* Demo Quick-Fill Pill */}
        <div className="mb-5 p-3 rounded-2xl bg-amber-50 border border-amber-200 flex items-center justify-between">
          <div className="flex items-center gap-2">
            <Sparkles className="w-4 h-4 text-amber-600 fill-amber-500" />
            <span className="text-xs font-extrabold text-amber-900">
              Demo Account Available
            </span>
          </div>
          <button
            type="button"
            onClick={handleDemoFill}
            className="text-xs font-black text-amber-800 underline hover:text-amber-900 uppercase tracking-wide cursor-pointer"
          >
            Fill Demo (Alex)
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3 rounded-2xl bg-red-50 border border-red-200 flex items-center gap-2.5 text-red-700 text-xs font-bold animate-shake">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Login Form */}
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1.5">
              Email
            </label>
            <input
              id="login-email"
              type="email"
              required
              autoComplete="email"
              placeholder="alex@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-3 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1.5">
              Password
            </label>
            <div className="relative">
              <input
                id="login-password"
                type={showPassword ? "text" : "password"}
                required
                autoComplete="current-password"
                placeholder="••••••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-3 pr-11 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
              />
              <button
                type="button"
                onClick={() => setShowPassword(!showPassword)}
                className="absolute right-3.5 top-1/2 -translate-y-1/2 text-neutral-400 hover:text-neutral-600 transition-colors"
                tabIndex={-1}
                aria-label={showPassword ? "Hide password" : "Show password"}
              >
                {showPassword ? <EyeOff className="w-5 h-5" /> : <Eye className="w-5 h-5" />}
              </button>
            </div>
          </div>

          <button
            id="login-submit-button"
            type="submit"
            disabled={submitting}
            className="btn-3d btn-duo-green w-full py-3.5 text-sm uppercase tracking-wider font-black mt-2 flex items-center justify-center gap-2"
          >
            {submitting ? "Logging in..." : "LOG IN"}
          </button>
        </form>

        {/* Footer Link */}
        <div className="mt-6 text-center border-t border-neutral-200 pt-5">
          <p className="text-xs font-extrabold text-neutral-500">
            Don&apos;t have an account?{" "}
            <Link
              href="/register"
              className="text-[#1cb0f6] hover:underline font-black uppercase ml-1"
            >
              Create one
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
