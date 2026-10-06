from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.user import UserResponse, UserProfileResponse
from .deps import get_current_user
from ..services.user_service import get_user_stats

router = APIRouter(prefix="/api", tags=["User & Profile"])

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.get("/profile", response_model=UserProfileResponse)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stats = get_user_stats(user, db)
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        display_name=user.display_name,
        avatar=user.avatar,
        xp=user.xp,
        gems=user.gems,
        hearts=user.hearts,
        streak=user.streak,
        daily_goal=user.daily_goal,
        daily_goal_progress=stats["daily_goal_progress"],
        daily_goal_completed=stats["daily_goal_completed"],
        completed_skills_count=stats["completed_skills_count"],
        completed_lessons_count=stats["completed_lessons_count"],
        crowns_count=stats["crowns_count"],
        league=stats["league"],
        rank=stats["rank"],
        created_at=user.created_at
    )
