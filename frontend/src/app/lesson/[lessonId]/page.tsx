"use client";

import React, { useState, useEffect } from "react";
import { useParams, useRouter } from "next/navigation";
import { LessonDetail, Exercise, AnswerResponse, LessonCompleteResponse } from "@/lib/types";
import { fetchLesson, startLesson, submitAnswer, completeLesson, fetchCurrentUser } from "@/lib/api";
import { LessonHeader } from "@/components/lesson/LessonHeader";
import { MultipleChoice } from "@/components/lesson/MultipleChoice";
import { Translate } from "@/components/lesson/Translate";
import { WordBank } from "@/components/lesson/WordBank";
import { MatchPairs } from "@/components/lesson/MatchPairs";
import { FillInBlank } from "@/components/lesson/FillInBlank";
import { TypeAnswer } from "@/components/lesson/TypeAnswer";
import { FeedbackBar } from "@/components/lesson/FeedbackBar";
import { OutOfHeartsModal } from "@/components/lesson/OutOfHeartsModal";
import { LessonCompleteModal } from "@/components/lesson/LessonCompleteModal";
import { sounds } from "@/lib/sound";

export default function LessonPage() {
  const params = useParams();
  const router = useRouter();
  const lessonId = parseInt(params.lessonId as string);

  const [lesson, setLesson] = useState<LessonDetail | null>(null);
  const [attemptId, setAttemptId] = useState<number | null>(null);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [hearts, setHearts] = useState(5);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  // Exercise interaction state
  const [selectedAnswer, setSelectedAnswer] = useState<any>("");
  const [evaluationStatus, setEvaluationStatus] = useState<"idle" | "correct" | "incorrect">("idle");
  const [answerResult, setAnswerResult] = useState<AnswerResponse | null>(null);
  const [isChecking, setIsChecking] = useState(false);

  // Out of hearts & Completion modals
  const [showOutOfHearts, setShowOutOfHearts] = useState(false);
  const [completeSummary, setCompleteSummary] = useState<LessonCompleteResponse | null>(null);

  // Initialize Lesson and Attempt
  useEffect(() => {
    async function loadLesson() {
      try {
        setLoading(true);
        setError(null);

        // Fetch lesson detail and current user
        const [lessonData, user] = await Promise.all([
          fetchLesson(lessonId),
          fetchCurrentUser()
        ]);

        setLesson(lessonData);
        setHearts(user.hearts);

        // Check hearts
        if (user.hearts <= 0) {
          setShowOutOfHearts(true);
          setLoading(false);
          return;
        }

        // Start attempt on backend
        const startData = await startLesson(lessonId);
        setAttemptId(startData.attempt_id);
        setHearts(startData.hearts_remaining);
      } catch (err: any) {
        setError(err.message || "Failed to load lesson.");
      } finally {
        setLoading(false);
      }
    }

    if (lessonId) {
      loadLesson();
    }
  }, [lessonId]);

  const currentExercise: Exercise | undefined = lesson?.exercises[currentIndex];

  const hasSelection = Boolean(
    (typeof selectedAnswer === "string" && selectedAnswer.trim().length > 0) ||
    (typeof selectedAnswer === "object" && selectedAnswer !== null && Object.keys(selectedAnswer).length > 0)
  );

  // Submit Answer to Backend
  const handleCheck = async () => {
    if (!currentExercise || !hasSelection || isChecking || evaluationStatus !== "idle") return;

    try {
      setIsChecking(true);
      const res = await submitAnswer(lessonId, {
        exercise_id: currentExercise.id,
        answer: selectedAnswer,
        attempt_id: attemptId || undefined
      });

      setAnswerResult(res);
      setHearts(res.hearts_remaining);

      if (res.correct) {
        setEvaluationStatus("correct");
        sounds.playCorrect();
      } else {
        setEvaluationStatus("incorrect");
        sounds.playIncorrect();

        if (res.hearts_remaining <= 0) {
          setTimeout(() => {
            setShowOutOfHearts(true);
          }, 800);
        }
      }
    } catch (err: any) {
      alert(err.message || "Error submitting answer");
    } finally {
      setIsChecking(false);
    }
  };

  // Continue to Next Exercise or Complete
  const handleContinue = async () => {
    if (!lesson) return;

    if (currentIndex < lesson.exercises.length - 1) {
      // Advance to next exercise
      setCurrentIndex((prev) => prev + 1);
      setSelectedAnswer("");
      setEvaluationStatus("idle");
      setAnswerResult(null);
    } else {
      // Lesson Complete!
      try {
        const completionRes = await completeLesson(lessonId, attemptId || undefined);
        setCompleteSummary(completionRes);
      } catch (err: any) {
        alert(err.message || "Error completing lesson");
      }
    }
  };

  if (loading) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4">
        <div className="w-16 h-16 border-4 border-[#58cc02] border-t-transparent rounded-full animate-spin mb-4" />
        <h2 className="text-xl font-black text-neutral-700">Loading your lesson...</h2>
      </div>
    );
  }

  if (error) {
    return (
      <div className="min-h-screen bg-white flex flex-col items-center justify-center p-4 text-center">
        <div className="w-16 h-16 rounded-full bg-red-100 text-[#ff4b4b] flex items-center justify-center text-2xl font-black mb-4">
          !
        </div>
        <h2 className="text-2xl font-black text-neutral-800 mb-2">Could Not Load Lesson</h2>
        <p className="text-neutral-500 max-w-sm mb-6">{error}</p>
        <button onClick={() => router.push("/learn")} className="btn-3d btn-duo-green px-8 py-3 text-sm">
          BACK TO LEARNING PATH
        </button>
      </div>
    );
  }

  if (!currentExercise) {
    return null;
  }

  return (
    <div className="min-h-screen bg-white flex flex-col justify-between pb-32">
      {/* Top Header */}
      <LessonHeader
        currentIndex={currentIndex}
        totalExercises={lesson?.exercises.length || 1}
        hearts={hearts}
      />

      {/* Main Exercise Content */}
      <main className="flex-1 flex flex-col justify-center px-4 py-6 max-w-2xl mx-auto w-full">
        {currentExercise.type === "multiple_choice" && (
          <MultipleChoice
            exercise={currentExercise}
            selectedAnswer={selectedAnswer}
            onSelectAnswer={setSelectedAnswer}
            disabled={evaluationStatus !== "idle"}
          />
        )}

        {currentExercise.type === "translate" && (
          <Translate
            exercise={currentExercise}
            selectedAnswer={selectedAnswer}
            onSelectAnswer={setSelectedAnswer}
            disabled={evaluationStatus !== "idle"}
          />
        )}

        {currentExercise.type === "word_bank" && (
          <WordBank
            exercise={currentExercise}
            selectedAnswer={selectedAnswer}
            onSelectAnswer={setSelectedAnswer}
            disabled={evaluationStatus !== "idle"}
          />
        )}

        {currentExercise.type === "match_pairs" && (
          <MatchPairs
            exercise={currentExercise}
            selectedAnswer={selectedAnswer}
            onSelectAnswer={setSelectedAnswer}
            disabled={evaluationStatus !== "idle"}
          />
        )}

        {currentExercise.type === "fill_blank" && (
          <FillInBlank
            exercise={currentExercise}
            selectedAnswer={selectedAnswer}
            onSelectAnswer={setSelectedAnswer}
            disabled={evaluationStatus !== "idle"}
          />
        )}

        {currentExercise.type === "type_answer" && (
          <TypeAnswer
            exercise={currentExercise}
            selectedAnswer={selectedAnswer}
            onSelectAnswer={setSelectedAnswer}
            disabled={evaluationStatus !== "idle"}
            onSubmit={handleCheck}
          />
        )}
      </main>

      {/* Bottom Floating Feedback Bar */}
      <FeedbackBar
        status={evaluationStatus}
        hasSelection={hasSelection}
        result={answerResult}
        onCheck={handleCheck}
        onContinue={handleContinue}
        isChecking={isChecking}
      />

      {/* Out of Hearts Modal */}
      {showOutOfHearts && (
        <OutOfHeartsModal
          onRefilled={(newHearts) => {
            setHearts(newHearts);
            setShowOutOfHearts(false);
          }}
        />
      )}

      {/* Lesson Complete Screen */}
      {completeSummary && <LessonCompleteModal summary={completeSummary} />}
    </div>
  );
}
