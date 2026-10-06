from datetime import datetime, date
from typing import Optional, List
from pydantic import BaseModel, ConfigDict

class LeaderboardEntry(BaseModel):
    rank: int
    user_id: int
    username: str
    display_name: str
    avatar: str
    xp: int
    is_current_user: bool

class AchievementResponse(BaseModel):
    id: int
    name: str
    description: str
    icon: str
    requirement_type: str
    requirement_value: int
    unlocked: bool
    unlocked_at: Optional[datetime] = None
    progress: int

    model_config = ConfigDict(from_attributes=True)

class DailyActivityResponse(BaseModel):
    activity_date: date
    xp_earned: int
    lessons_completed: int

class HeartStatusResponse(BaseModel):
    hearts: int
    max_hearts: int = 5
    next_heart_in_seconds: Optional[int] = None
    message: str
