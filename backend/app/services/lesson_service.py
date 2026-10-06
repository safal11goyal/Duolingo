import re
import unicodedata
import json
from datetime import datetime, timezone
from typing import Any
from fastapi import HTTPException
from sqlalchemy.orm import Session

from ..models import User, Lesson, Exercise, ExerciseOption, LessonAttempt, UserSkillProgress, Skill
from .streak_service import record_activity_and_update_streak
from .achievement_service import check_and_unlock_achievements
from .progress_service import unlock_next_skill

def normalize_text(text: str) -> str:
    """Normalizes text by trimming whitespace, lowercasing, and stripping punctuation."""
    if not text:
        return ""
    # Strip leading/trailing punctuation like ¿¡!?,.
    cleaned = re.sub(r"[^\w\s]", "", text.strip().lower())
    # Collapse multiple whitespaces
    return " ".join(cleaned.split())

def strip_accents(text: str) -> str:
    """Removes diacritics for flexible accent tolerance."""
    nfkd = unicodedata.normalize("NFKD", text)
    return "".join(c for c in nfkd if not unicodedata.combining(c))

def start_lesson_attempt(user: User, lesson_id: int, db: Session) -> dict:
    """Checks requirements and initiates a lesson attempt."""
    if user.hearts <= 0:
        raise HTTPException(status_code=400, detail="Out of hearts. Practice or refill to continue.")

    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    # Check skill lock state
    progress = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user.id,
        UserSkillProgress.skill_id == lesson.skill_id
    ).first()

    if progress and progress.status == "locked":
        raise HTTPException(status_code=403, detail="Skill is locked. Complete previous skills first.")

    attempt = LessonAttempt(
        user_id=user.id,
        lesson_id=lesson_id,
        started_at=datetime.now(timezone.utc),
        score=0,
        correct_answers=0,
        wrong_answers=0,
        xp_earned=0,
        hearts_lost=0,
        completed=False
    )
    db.add(attempt)
    db.commit()
    db.refresh(attempt)

    return {
        "attempt_id": attempt.id,
        "lesson_id": lesson_id,
        "started_at": attempt.started_at,
        "hearts_remaining": user.hearts,
        "total_exercises": len(lesson.exercises)
    }

def validate_user_answer(exercise: Exercise, user_answer: Any) -> bool:
    """Validates submitted answer against backend truth according to exercise type."""
    if exercise.type == "multiple_choice":
        # Can match option text or option ID
        correct_opt = next((opt for opt in exercise.options if opt.is_correct), None)
        if not correct_opt:
            return normalize_text(str(user_answer)) == normalize_text(exercise.correct_answer)
        
        user_str = str(user_answer).strip()
        # Direct match with correct option text or correct option ID
        if user_str == str(correct_opt.id) or normalize_text(user_str) == normalize_text(correct_opt.text):
            return True
        return normalize_text(user_str) == normalize_text(exercise.correct_answer)

    elif exercise.type == "match_pairs":
        # user_answer is expected as list of pair objects or dict
        try:
            expected_pairs = json.loads(exercise.correct_answer)
        except Exception:
            # Format fallback "Hello:Hola,Bye:Adios"
            pairs = exercise.correct_answer.split(",")
            expected_pairs = {}
            for p in pairs:
                if ":" in p:
                    k, v = p.split(":", 1)
                    expected_pairs[k.strip().lower()] = v.strip().lower()

        if isinstance(user_answer, str):
            try:
                user_answer = json.loads(user_answer)
            except Exception:
                pass

        if isinstance(user_answer, list):
            # Expecting [{"left": "...", "right": "..."}] or [{"source": "...", "target": "..."}]
            user_dict = {}
            for item in user_answer:
                k = item.get("left") or item.get("source") or item.get("key")
                v = item.get("right") or item.get("target") or item.get("value")
                if k and v:
                    user_dict[normalize_text(k)] = normalize_text(v)
            user_answer = user_dict

        if isinstance(user_answer, dict) and isinstance(expected_pairs, dict):
            if len(user_answer) != len(expected_pairs):
                return False
            for k, v in expected_pairs.items():
                norm_k = normalize_text(k)
                norm_v = normalize_text(v)
                user_v = user_answer.get(norm_k)
                if not user_v or (user_v != norm_v and strip_accents(user_v) != strip_accents(norm_v)):
                    return False
            return True
        return False

    elif exercise.type in ("translate", "word_bank", "fill_blank", "type_answer"):
        if isinstance(user_answer, list):
            user_str = " ".join(str(w) for w in user_answer)
        else:
            user_str = str(user_answer)

        norm_user = normalize_text(user_str)
        
        # Check against multiple acceptable alternatives separated by '/' or ';'
        alternatives = [a.strip() for a in re.split(r"[/;]", exercise.correct_answer)]
        for alt in alternatives:
            norm_alt = normalize_text(alt)
            if norm_user == norm_alt:
                return True
            # Also accept accent-tolerant match
            if strip_accents(norm_user) == strip_accents(norm_alt):
                return True

        return False

    return False

def submit_exercise_answer(user: User, lesson_id: int, exercise_id: int, answer: Any, attempt_id: int = None, db: Session = None) -> dict:
    """Validates answer, deducts heart on fail, awards XP on success, records progress."""
    if user.hearts <= 0:
        raise HTTPException(status_code=400, detail="Out of hearts. Practice or refill to continue.")

    exercise = db.query(Exercise).filter(Exercise.id == exercise_id).first()
    if not exercise:
        raise HTTPException(status_code=404, detail="Exercise not found.")

    if exercise.lesson_id != lesson_id:
        raise HTTPException(status_code=400, detail="Exercise does not belong to this lesson.")

    is_correct = validate_user_answer(exercise, answer)
    xp_earned = exercise.xp if is_correct else 0

    if is_correct:
        user.xp += xp_earned
    else:
        user.hearts = max(0, user.hearts - 1)

    # Track in attempt if attempt_id is provided
    if attempt_id:
        attempt = db.query(LessonAttempt).filter(LessonAttempt.id == attempt_id).first()
        if attempt:
            if attempt.user_id != user.id:
                raise HTTPException(status_code=403, detail="Forbidden: You cannot modify another user's lesson attempt.")
            if is_correct:
                attempt.correct_answers += 1
                attempt.xp_earned += xp_earned
            else:
                attempt.wrong_answers += 1
                attempt.hearts_lost += 1

    user.last_active_at = datetime.now(timezone.utc)
    user.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(user)

    return {
        "correct": is_correct,
        "correct_answer": exercise.correct_answer,
        "explanation": exercise.explanation,
        "xp_earned": xp_earned,
        "hearts_remaining": user.hearts,
        "is_lesson_complete": False
    }

def finish_lesson(user: User, lesson_id: int, attempt_id: int = None, db: Session = None) -> dict:
    """Marks lesson completed, gives completion bonus XP, updates skill progress & streak."""
    lesson = db.query(Lesson).filter(Lesson.id == lesson_id).first()
    if not lesson:
        raise HTTPException(status_code=404, detail="Lesson not found.")

    skill = lesson.skill
    bonus_xp = lesson.xp_reward
    user.xp += bonus_xp

    attempt = None
    is_perfect = False
    if attempt_id:
        attempt = db.query(LessonAttempt).filter(LessonAttempt.id == attempt_id).first()
        if attempt:
            if attempt.user_id != user.id:
                raise HTTPException(status_code=403, detail="Forbidden: You cannot complete another user's lesson attempt.")
            attempt.completed = True
            attempt.completed_at = datetime.now(timezone.utc)
            attempt.xp_earned += bonus_xp
            attempt.score = int((attempt.correct_answers / max(1, attempt.correct_answers + attempt.wrong_answers)) * 100)
            if attempt.wrong_answers == 0 and attempt.correct_answers > 0:
                is_perfect = True

    # Update UserSkillProgress
    progress = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user.id,
        UserSkillProgress.skill_id == skill.id
    ).first()

    if not progress:
        progress = UserSkillProgress(
            user_id=user.id,
            skill_id=skill.id,
            status="in_progress",
            xp=0,
            crown_level=0,
            completed_lessons=0
        )
        db.add(progress)

    progress.completed_lessons += 1
    progress.xp += bonus_xp

    next_skill_unlocked = False
    total_lessons = len(skill.lessons)
    if progress.completed_lessons >= total_lessons:
        progress.status = "completed"
        progress.crown_level += 1
        # Unlock next skill
        next_skill_unlocked = unlock_next_skill(user, skill.id, db)
    else:
        progress.status = "in_progress"

    # Record daily activity & streak
    current_streak = record_activity_and_update_streak(user, bonus_xp, lesson_completed=True, db=db)

    # Check achievements
    unlocked_achievements = check_and_unlock_achievements(user, db, is_perfect_lesson=is_perfect)

    db.commit()
    db.refresh(user)
    db.refresh(progress)

    return {
        "success": True,
        "lesson_id": lesson_id,
        "xp_earned": bonus_xp,
        "total_xp": user.xp,
        "hearts_remaining": user.hearts,
        "streak": current_streak,
        "skill_progress": {
            "skill_id": skill.id,
            "status": progress.status,
            "crown_level": progress.crown_level,
            "completed_lessons": progress.completed_lessons,
            "total_lessons": total_lessons
        },
        "next_skill_unlocked": next_skill_unlocked,
        "achievements_unlocked": unlocked_achievements
    }
