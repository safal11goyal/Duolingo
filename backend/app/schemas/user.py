from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserBase(BaseModel):
    username: str
    display_name: str
    avatar: str
    daily_goal: int

class UserResponse(UserBase):
    id: int
    xp: int
    gems: int
    hearts: int
    streak: int
    last_active_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class UserProfileResponse(BaseModel):
    id: int
    username: str
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
