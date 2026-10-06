from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Skill, Unit, UserSkillProgress, Course, Lesson, Exercise, UserAnswer, LessonAttempt
from ..schemas.course import LearningPathResponse, SkillSummary, UnitSummary
from .deps import get_current_user
from ..services.progress_service import get_learning_path_data

router = APIRouter(tags=["Learning Path"])

@router.get("/path", response_model=LearningPathResponse)
def get_path(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = get_learning_path_data(user, db)
    if not data:
        raise HTTPException(status_code=404, detail="No course data found. Please run seed script.")
    return data

@router.get("/courses")
def get_courses(db: Session = Depends(get_db)):
    courses = db.query(Course).all()
    return [
        {
            "id": c.id,
            "name": c.name,
            "source_language": c.source_language,
            "target_language": c.target_language,
            "description": c.description,
            "difficulty": c.difficulty,
            "created_at": c.created_at,
        }
        for c in courses
    ]

@router.get("/units")
def get_units(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = get_learning_path_data(user, db)
    if not data:
        raise HTTPException(status_code=404, detail="No course data found.")
    return data["units"]

@router.get("/skills/{skill_id}")
def get_skill(skill_id: int, user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    skill = db.query(Skill).filter(Skill.id == skill_id).first()
    if not skill:
        raise HTTPException(status_code=404, detail="Skill not found.")

    progress = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user.id,
        UserSkillProgress.skill_id == skill.id
    ).first()

    return {
        "id": skill.id,
        "unit_id": skill.unit_id,
        "title": skill.title,
        "description": skill.description,
        "order_index": skill.order_index,
        "xp_reward": skill.xp_reward,
        "status": progress.status if progress else "locked",
        "crown_level": progress.crown_level if progress else 0,
        "completed_lessons": progress.completed_lessons if progress else 0,
        "total_lessons": len(skill.lessons),
        "lessons": [
            {
                "id": l.id,
                "title": l.title,
                "order_index": l.order_index,
                "xp_reward": l.xp_reward,
                "exercise_count": len(l.exercises)
            }
            for l in skill.lessons
        ]
    }

@router.get("/progress")
def get_progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    attempts = db.query(LessonAttempt).filter(LessonAttempt.user_id == user.id).all()
    skill_progresses = db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).all()
    return {
        "user_id": user.id,
        "xp": user.xp,
        "streak": user.streak,
        "lessons": [
            {
                "id": a.id,
                "user_id": a.user_id,
                "lesson_id": a.lesson_id,
                "completed": a.completed,
                "score": a.score,
                "xp_earned": a.xp_earned,
                "attempts": a.attempts,
                "completed_at": a.completed_at,
                "last_attempted_at": a.last_attempted_at or a.started_at
            }
            for a in attempts
        ],
        "skills": [
            {
                "skill_id": p.skill_id,
                "status": p.status,
                "xp": p.xp,
                "crown_level": p.crown_level,
                "completed_lessons": p.completed_lessons,
                "updated_at": p.updated_at
            }
            for p in skill_progresses
        ]
    }

@router.get("/lessons")
def list_all_lessons(db: Session = Depends(get_db)):
    lessons = db.query(Lesson).order_by(Lesson.order_index).all()
    return [
        {
            "id": l.id,
            "skill_id": l.skill_id,
            "course_id": l.course_id,
            "title": l.title,
            "description": l.description,
            "order_index": l.order_index,
            "xp_reward": l.xp_reward,
            "exercise_count": len(l.exercises)
        }
        for l in lessons
    ]

@router.get("/questions")
def list_all_questions(lesson_id: int = None, db: Session = Depends(get_db)):
    q = db.query(Exercise)
    if lesson_id is not None:
        q = q.filter(Exercise.lesson_id == lesson_id)
    exercises = q.order_by(Exercise.order_index).all()
    return [
        {
            "id": ex.id,
            "lesson_id": ex.lesson_id,
            "type": ex.type,
            "question": ex.question,
            "correct_answer": ex.correct_answer,
            "explanation": ex.explanation,
            "order_index": ex.order_index,
            "xp": ex.xp,
            "options": [{"id": opt.id, "text": opt.text} for opt in ex.options]
        }
        for ex in exercises
    ]

@router.get("/answers")
def list_user_answers(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    answers = db.query(UserAnswer).filter(UserAnswer.user_id == user.id).order_by(UserAnswer.timestamp.desc()).limit(100).all()
    return [
        {
            "id": a.id,
            "user_id": a.user_id,
            "question_id": a.question_id,
            "lesson_id": a.lesson_id,
            "attempt_id": a.attempt_id,
            "submitted_answer": a.submitted_answer,
            "is_correct": a.is_correct,
            "timestamp": a.timestamp
        }
        for a in answers
    ]

