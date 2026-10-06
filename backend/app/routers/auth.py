from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..schemas.user import UserRegister, UserLogin, UserResponse, TokenResponse, UserProfileResponse
from ..auth.service import register_user, authenticate_user
from ..auth.security import create_access_token
from ..auth.dependencies import get_current_user
from ..services.user_service import get_user_stats

router = APIRouter(prefix="/api", tags=["Authentication & User"])

@router.post("/auth/register", response_model=TokenResponse)
def register(body: UserRegister, response: Response, db: Session = Depends(get_db)):
    user = register_user(db, body)
    token = create_access_token({"sub": str(user.id)})
    
    # Set HTTP-only secure cookie for persistent web session
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,  # 7 days
        samesite="lax",
        secure=False  # Set to True in HTTPS production
    )
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )

@router.post("/auth/login", response_model=TokenResponse)
def login(body: UserLogin, response: Response, db: Session = Depends(get_db)):
    user = authenticate_user(db, body)
    token = create_access_token({"sub": str(user.id)})
    
    response.set_cookie(
        key="access_token",
        value=token,
        httponly=True,
        max_age=60 * 60 * 24 * 7,
        samesite="lax",
        secure=False
    )
    
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=user
    )

@router.get("/auth/me", response_model=UserResponse)
def auth_me(user: User = Depends(get_current_user)):
    return user

@router.post("/auth/logout")
def logout(response: Response):
    response.delete_cookie(key="access_token")
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
def get_me(user: User = Depends(get_current_user)):
    return user

@router.get("/profile", response_model=UserProfileResponse)
def get_profile(user: User = Depends(get_current_user), db: Session = Depends(get_db)):
    stats = get_user_stats(user, db)
    return UserProfileResponse(
        id=user.id,
        username=user.username,
        email=user.email,
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
