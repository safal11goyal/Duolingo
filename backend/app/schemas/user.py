from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict, EmailStr, Field

class UserBase(BaseModel):
    username: str
    email: EmailStr
    display_name: str
    avatar: str = "/avatars/alex.png"
    daily_goal: int = 20

class UserRegister(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr
    password: str = Field(..., min_length=6, max_length=100)
    display_name: str = Field(..., min_length=1, max_length=100)

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
    avatar: str
    xp: int
    gems: int
    hearts: int
    streak: int
    daily_goal: int
    last_active_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class TokenResponse(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserResponse

class UserProfileResponse(BaseModel):
    id: int
    username: str
    email: str
    display_name: str
    avatar: str
    xp: int
    gems: int
    hearts: int
    streak: int
    daily_goal: int
    daily_goal_progress: int
    daily_goal_completed: bool
    completed_skills_count: int
    completed_lessons_count: int
    crowns_count: int
    league: str
    rank: int
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)
