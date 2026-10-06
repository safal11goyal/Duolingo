from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from ..database import get_db
from ..models import User, Skill, Unit, UserSkillProgress
from ..schemas.course import LearningPathResponse, SkillSummary, UnitSummary
from .deps import get_current_user
from ..services.progress_service import get_learning_path_data

router = APIRouter(prefix="/api", tags=["Learning Path"])

@router.get("/path", response_model=LearningPathResponse)
def get_path(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = get_learning_path_data(user, db)
    if not data:
        raise HTTPException(status_code=404, detail="No course data found. Please run seed script.")
    return data

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
    progresses = db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).all()
    return [
        {
            "skill_id": p.skill_id,
            "status": p.status,
            "xp": p.xp,
            "crown_level": p.crown_level,
            "completed_lessons": p.completed_lessons,
            "updated_at": p.updated_at
        }
        for p in progresses
    ]
