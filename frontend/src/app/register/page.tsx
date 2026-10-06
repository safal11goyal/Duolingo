"use client";

import React, { useState, useEffect } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import { Eye, EyeOff, AlertCircle } from "lucide-react";
import { DuoMascot } from "@/components/ui/DuoMascot";
import { useAuth } from "@/context/AuthContext";

export default function RegisterPage() {
  const router = useRouter();
  const { register, isAuthenticated, isLoading } = useAuth();

  const [username, setUsername] = useState("");
  const [displayName, setDisplayName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
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
    setError(null);

    // Client-side validations
    if (username.trim().length < 3) {
      setError("Username must be at least 3 characters.");
      return;
    }
    if (!displayName.trim()) {
      setError("Please provide a display name.");
      return;
    }
    if (!email.trim() || !email.includes("@")) {
      setError("Please enter a valid email address.");
      return;
    }
    if (password.length < 6) {
      setError("Password must be at least 6 characters long.");
      return;
    }
    if (password !== confirmPassword) {
      setError("Passwords do not match.");
      return;
    }

    setSubmitting(true);
    try {
      await register({
        username: username.trim(),
        display_name: displayName.trim(),
        email: email.trim(),
        password: password,
      });
      router.push("/learn");
    } catch (err: any) {
      setError(err.message || "Failed to create account. Please check your details.");
    } finally {
      setSubmitting(false);
    }
  };

  if (isLoading) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center">
        <DuoMascot size={90} expression="cheering" className="animate-bounce" />
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-white md:bg-[#f7f7f7] flex flex-col justify-center items-center px-4 py-8 select-none">
      <div className="w-full max-w-md bg-white md:border-2 md:border-neutral-200 md:rounded-3xl p-6 sm:p-8 md:shadow-sm">
        {/* Mascot & Brand Header */}
        <div className="flex flex-col items-center mb-6 text-center">
          <DuoMascot size={80} expression="cheering" />
          <span className="text-2xl font-black text-[#58cc02] tracking-tight mt-2">
            duolingo
          </span>
          <h1 className="text-2xl font-black text-neutral-800 mt-2">
            Get started!
          </h1>
          <p className="text-xs sm:text-sm text-neutral-500 font-bold mt-1">
            Create your account to start learning Spanish
          </p>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="mb-4 p-3 rounded-2xl bg-red-50 border border-red-200 flex items-center gap-2.5 text-red-700 text-xs font-bold animate-shake">
            <AlertCircle className="w-4 h-4 shrink-0 text-red-500" />
            <span>{error}</span>
          </div>
        )}

        {/* Registration Form */}
        <form onSubmit={handleSubmit} className="space-y-3.5">
          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1">
              Username
            </label>
            <input
              id="register-username"
              type="text"
              required
              autoComplete="username"
              placeholder="e.g. maria_learner"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              className="w-full px-4 py-2.5 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1">
              Display Name
            </label>
            <input
              id="register-display-name"
              type="text"
              required
              autoComplete="name"
              placeholder="e.g. Maria Gonzalez"
              value={displayName}
              onChange={(e) => setDisplayName(e.target.value)}
              className="w-full px-4 py-2.5 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1">
              Email
            </label>
            <input
              id="register-email"
              type="email"
              required
              autoComplete="email"
              placeholder="maria@example.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full px-4 py-2.5 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
            />
          </div>

          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1">
              Password
            </label>
            <div className="relative">
              <input
                id="register-password"
                type={showPassword ? "text" : "password"}
                required
                autoComplete="new-password"
                placeholder="At least 6 characters"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-4 py-2.5 pr-11 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
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

          <div>
            <label className="block text-xs font-black uppercase tracking-wider text-neutral-500 mb-1">
              Confirm Password
            </label>
            <input
              id="register-confirm-password"
              type={showPassword ? "text" : "password"}
              required
              autoComplete="new-password"
              placeholder="Repeat your password"
              value={confirmPassword}
              onChange={(e) => setConfirmPassword(e.target.value)}
              className="w-full px-4 py-2.5 rounded-2xl border-2 border-neutral-200 focus:border-[#1cb0f6] focus:outline-none font-bold text-neutral-800 text-sm placeholder:text-neutral-300 transition-colors bg-neutral-50 focus:bg-white"
            />
          </div>

          <button
            id="register-submit-button"
            type="submit"
            disabled={submitting}
            className="btn-3d btn-duo-green w-full py-3.5 text-sm uppercase tracking-wider font-black mt-3 flex items-center justify-center gap-2"
          >
            {submitting ? "Creating account..." : "CREATE ACCOUNT"}
          </button>
        </form>

        {/* Footer Link */}
        <div className="mt-6 text-center border-t border-neutral-200 pt-5">
          <p className="text-xs font-extrabold text-neutral-500">
            Already have an account?{" "}
            <Link
              href="/login"
              className="text-[#1cb0f6] hover:underline font-black uppercase ml-1"
            >
              Log in
            </Link>
          </p>
        </div>
      </div>
    </div>
  );
}
