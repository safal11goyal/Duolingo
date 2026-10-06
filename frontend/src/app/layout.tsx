import type { Metadata } from "next";
import "./globals.css";
import { AuthProvider } from "@/context/AuthContext";

export const metadata: Metadata = {
  title: "Duolingo - Learn Spanish with Fun, Interactive Lessons",
  description: "A production-quality Duolingo clone featuring interactive exercises, gamified learning path, streak tracking, and hearts system.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className="h-full antialiased">
      <body className="min-h-full flex flex-col font-sans bg-white text-neutral-800">
        <AuthProvider>
          {children}
        </AuthProvider>
      </body>
    </html>
  );
}
