from typing import List, Optional, Any
from pydantic import BaseModel, ConfigDict

class ExerciseOptionPublic(BaseModel):
    id: int
    text: str

    model_config = ConfigDict(from_attributes=True)

class ExercisePublic(BaseModel):
    id: int
    lesson_id: int
    type: str  # multiple_choice, translate, word_bank, match_pairs, fill_blank, type_answer
    question: str
    order_index: int
    xp: int
    options: List[ExerciseOptionPublic] = []
    # Additional metadata helper fields if needed (e.g. word bank tokens or pairs scrambled)
    metadata: Optional[dict] = None

    model_config = ConfigDict(from_attributes=True)

class LessonSummary(BaseModel):
    id: int
    skill_id: int
    title: str
    order_index: int
    xp_reward: int
    exercise_count: int

    model_config = ConfigDict(from_attributes=True)

class LessonDetail(BaseModel):
    id: int
    skill_id: int
    title: str
    order_index: int
    xp_reward: int
    exercises: List[ExercisePublic]

    model_config = ConfigDict(from_attributes=True)

class SkillSummary(BaseModel):
    id: int
    unit_id: int
    title: str
    description: str
    order_index: int
    xp_reward: int
    status: str  # locked, available, in_progress, completed
    crown_level: int
    completed_lessons: int
    total_lessons: int
    lessons: List[LessonSummary] = []

    model_config = ConfigDict(from_attributes=True)

class UnitSummary(BaseModel):
    id: int
    course_id: int
    title: str
    description: str
    order_index: int
    skills: List[SkillSummary] = []

    model_config = ConfigDict(from_attributes=True)

class LearningPathResponse(BaseModel):
    course_name: str
    source_language: str
    target_language: str
    units: List[UnitSummary]
