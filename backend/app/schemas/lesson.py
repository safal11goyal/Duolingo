from datetime import datetime
from typing import Optional, List, Any
from pydantic import BaseModel, ConfigDict

class LessonStartResponse(BaseModel):
    attempt_id: int
    lesson_id: int
    started_at: datetime
    hearts_remaining: int
    total_exercises: int

class AnswerSubmission(BaseModel):
    exercise_id: int
    answer: Any  # can be str or list (e.g. for match pairs)
    attempt_id: Optional[int] = None

class AnswerResponse(BaseModel):
    correct: bool
    correct_answer: str
    explanation: Optional[str] = None
    xp_earned: int
    hearts_remaining: int
    is_lesson_complete: bool

class LessonCompleteRequest(BaseModel):
    attempt_id: Optional[int] = None

class SkillProgressSummary(BaseModel):
    skill_id: int
    status: str
    crown_level: int
    completed_lessons: int
    total_lessons: int

class LessonCompleteResponse(BaseModel):
    success: bool
    lesson_id: int
    xp_earned: int
    total_xp: int
    hearts_remaining: int
    streak: int
    skill_progress: SkillProgressSummary
    next_skill_unlocked: bool
    achievements_unlocked: List[str] = []
