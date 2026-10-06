import json
import random
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Lesson, Exercise, UserSkillProgress
from ..schemas.course import LessonDetail, ExercisePublic, ExerciseOptionPublic
from ..schemas.lesson import LessonStartResponse, AnswerSubmission, AnswerResponse, LessonCompleteRequest, LessonCompleteResponse
from .deps import get_current_user
from ..services.lesson_service import start_lesson_attempt, submit_exercise_answer, finish_lesson

router = APIRouter(prefix="/api/lessons", tags=["Lessons"])

@router.get("/{lesson_id}", response_model=LessonDetail)
def get_lesson(lesson_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    if not lesson.skill:
        raise HTTPException(status_code=404, detail="Lesson does not belong to a valid skill.")

    if not lesson.skill.unit or not lesson.skill.unit.course:
        raise HTTPException(status_code=404, detail="Skill does not belong to a valid course.")

    if user.hearts <= 0:
        raise HTTPException(status_code=400, detail="Out of hearts. Practice or refill to continue learning.")

    # Check if skill is locked
    progress = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user.id,
        UserSkillProgress.skill_id == lesson.skill_id
    ).first()

    if not progress or progress.status == "locked":
        raise HTTPException(status_code=403, detail="Skill is locked. Complete previous skills first.")

    # Sanitize exercises (hide correct answers & solutions)
    public_exercises = []
    for ex in lesson.exercises:
        options_public = [
            ExerciseOptionPublic(id=opt.id, text=opt.text)
            for opt in ex.options
        ]
        
        metadata = {}
        if ex.type == "match_pairs":
            try:
                pairs_dict = json.loads(ex.correct_answer)
            except Exception:
                pairs = ex.correct_answer.split(",")
                pairs_dict = {}
                for p in pairs:
                    if ":" in p:
                        k, v = p.split(":", 1)
                        pairs_dict[k.strip()] = v.strip()
            
            left_items = list(pairs_dict.keys())
            right_items = list(pairs_dict.values())
            random.seed(ex.id)  # Deterministic shuffle for consistency
            shuffled_right = list(right_items)
            random.shuffle(shuffled_right)
            metadata["left_items"] = left_items
            metadata["right_items"] = shuffled_right
            metadata["pairs_count"] = len(left_items)
            
        elif ex.type == "word_bank":
            # Provide tokens including correct words plus distractors
            options_words = [opt.text for opt in ex.options]
            if not options_words:
                words = [w.strip() for w in ex.correct_answer.split() if w.strip()]
                # Add some common Spanish distractors if none provided
                distractors = ["la", "un", "bien", "gracias", "yo", "es", "el", "muy"]
                distractors = [d for d in distractors if d not in words][:3]
                all_tokens = words + distractors
                random.seed(ex.id)
                random.shuffle(all_tokens)
                metadata["tokens"] = all_tokens
            else:
                metadata["tokens"] = options_words

        public_exercises.append(
            ExercisePublic(
                id=ex.id,
                lesson_id=ex.lesson_id,
                type=ex.type,
                question=ex.question,
                order_index=ex.order_index,
                xp=ex.xp,
                options=options_public,
                metadata=metadata
            )
        )

    return LessonDetail(
        id=lesson.id,
        skill_id=lesson.skill_id,
        title=lesson.title,
        order_index=lesson.order_index,
        xp_reward=lesson.xp_reward,
        exercises=public_exercises
    )

@router.post("/{lesson_id}/start", response_model=LessonStartResponse)
def start_lesson(lesson_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    result = start_lesson_attempt(user, lesson_id, db)
    return LessonStartResponse(**result)

@router.post("/{lesson_id}/answer", response_model=AnswerResponse)
def answer_exercise(
    lesson_id: int,
    body: AnswerSubmission,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = submit_exercise_answer(
        user=user,
        lesson_id=lesson_id,
        exercise_id=body.exercise_id,
        answer=body.answer,
        attempt_id=body.attempt_id,
        db=db
    )
    return AnswerResponse(**result)

@router.post("/{lesson_id}/complete", response_model=LessonCompleteResponse)
def complete_lesson_endpoint(
    lesson_id: int,
    body: LessonCompleteRequest = LessonCompleteRequest(),
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    result = finish_lesson(user=user, lesson_id=lesson_id, attempt_id=body.attempt_id, db=db)
    return LessonCompleteResponse(**result)
