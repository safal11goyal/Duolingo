from datetime import date, datetime, timedelta
from typing import Optional
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User, DailyActivity, UserSkillProgress, LessonAttempt, UserAchievement
from .deps import get_current_user
from ..services.streak_service import record_activity_and_update_streak

router = APIRouter(prefix="/api/dev", tags=["Development & Testing Helpers"])

class SimulateDateRequest(BaseModel):
    simulated_date: str  # YYYY-MM-DD
    xp_gained: int = 15

class UpdateGoalRequest(BaseModel):
    daily_goal: int

@router.post("/simulate-activity")
def simulate_activity(
    body: SimulateDateRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Simulates activity on a specific date to test streak logic."""
    target_dt = datetime.strptime(body.simulated_date, "%Y-%m-%d").date()
    streak = record_activity_and_update_streak(
        user=user,
        xp_gained=body.xp_gained,
        lesson_completed=True,
        db=db,
        target_date=target_dt
    )
    return {
        "message": f"Simulated activity for date {body.simulated_date}",
        "current_streak": streak,
        "total_xp": user.xp
    }

@router.post("/update-goal")
def update_goal(
    body: UpdateGoalRequest,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Updates daily XP goal."""
    user.daily_goal = body.daily_goal
    db.commit()
    return {"daily_goal": user.daily_goal}

@router.post("/reset-progress")
def reset_progress(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    """Resets user's progress for testing fresh learning flow."""
    db.query(DailyActivity).filter(DailyActivity.user_id == user.id).delete()
    db.query(LessonAttempt).filter(LessonAttempt.user_id == user.id).delete()
    db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).delete()
    db.query(UserAchievement).filter(UserAchievement.user_id == user.id).delete()
    
    user.xp = 0
    user.hearts = 5
    user.streak = 0
    db.commit()
    
    from ..auth.service import init_user_skill_progress
    init_user_skill_progress(user, db)
    
    return {"message": "User progress has been reset for fresh testing."}
