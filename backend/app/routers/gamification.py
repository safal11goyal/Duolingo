from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ..database import get_db
from ..models import User
from ..schemas.gamification import LeaderboardEntry, AchievementResponse, HeartStatusResponse
from .deps import get_current_user
from ..services.user_service import refill_hearts, practice_heart
from ..services.achievement_service import get_user_achievements_status

router = APIRouter(prefix="/api", tags=["Gamification"])

@router.get("/leaderboard", response_model=List[LeaderboardEntry])
def get_leaderboard(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    users = db.query(User).order_by(User.xp.desc()).limit(20).all()
    results = []
    for rank_idx, u in enumerate(users, start=1):
        results.append(
            LeaderboardEntry(
                rank=rank_idx,
                user_id=u.id,
                username=u.username,
                display_name=u.display_name,
                avatar=u.avatar,
                xp=u.xp,
                is_current_user=(u.id == user.id)
            )
        )
    return results

@router.get("/achievements", response_model=List[AchievementResponse])
def get_achievements(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    data = get_user_achievements_status(user, db)
    return [AchievementResponse(**item) for item in data]

@router.post("/hearts/refill", response_model=HeartStatusResponse)
def refill_hearts_endpoint(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = refill_hearts(user, db)
    return HeartStatusResponse(
        hearts=updated_user.hearts,
        max_hearts=5,
        message="Hearts refilled to full!"
    )

@router.post("/hearts/practice", response_model=HeartStatusResponse)
def practice_heart_endpoint(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    updated_user = practice_heart(user, db)
    return HeartStatusResponse(
        hearts=updated_user.hearts,
        max_hearts=5,
        message="+1 Heart earned from practice session!"
    )

@router.get("/hearts/status", response_model=HeartStatusResponse)
def heart_status(user: User = Depends(get_current_user)):
    return HeartStatusResponse(
        hearts=user.hearts,
        max_hearts=5,
        message="Hearts status"
    )
