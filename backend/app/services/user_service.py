from datetime import datetime, date
from sqlalchemy.orm import Session
from ..models import User, UserSkillProgress, LessonAttempt, DailyActivity, Course

def get_default_user(db: Session) -> User:
    """Returns the default learner (Alex), creating one if not found."""
    user = db.query(User).filter(User.username == "alex").first()
    if not user:
        user = User(
            username="alex",
            display_name="Alex Rivera",
            avatar="/avatars/alex.png",
            xp=150,
            gems=500,
            hearts=5,
            streak=3,
            daily_goal=20,
            last_active_at=datetime.utcnow(),
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        db.add(user)
        db.commit()
        db.refresh(user)
    
    # Regenerate hearts based on elapsed time
    regenerate_hearts(user, db)
    return user

def regenerate_hearts(user: User, db: Session) -> None:
    """Regenerates 1 heart every 30 minutes if hearts < 5."""
    if user.hearts >= 5:
        return
    
    now = datetime.utcnow()
    last_active = user.updated_at or user.last_active_at or now
    elapsed_minutes = (now - last_active).total_seconds() / 60.0
    
    # 1 heart per 30 minutes
    hearts_to_add = int(elapsed_minutes // 30)
    if hearts_to_add > 0:
        new_hearts = min(5, user.hearts + hearts_to_add)
        if new_hearts != user.hearts:
            user.hearts = new_hearts
            user.updated_at = now
            db.commit()
            db.refresh(user)

def refill_hearts(user: User, db: Session) -> User:
    """Refills hearts to full (5)."""
    user.hearts = 5
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

def practice_heart(user: User, db: Session) -> User:
    """Practice restores +1 heart up to 5."""
    user.hearts = min(5, user.hearts + 1)
    user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(user)
    return user

def get_user_stats(user: User, db: Session) -> dict:
    """Calculates all profile statistics for the user."""
    # Today's daily activity
    today = date.today()
    activity = db.query(DailyActivity).filter(
        DailyActivity.user_id == user.id,
        DailyActivity.activity_date == today
    ).first()
    
    daily_xp = activity.xp_earned if activity else 0
    daily_completed = daily_xp >= user.daily_goal
    
    # Completed skills and crowns
    progresses = db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).all()
    completed_skills = sum(1 for p in progresses if p.status == "completed")
    crowns_count = sum(p.crown_level for p in progresses)
    
    # Completed lessons
    completed_lessons = db.query(LessonAttempt).filter(
        LessonAttempt.user_id == user.id,
        LessonAttempt.completed == True
    ).count()
    
    # League ranking
    # All users sorted by XP desc
    all_users = db.query(User).order_by(User.xp.desc()).all()
    rank = 1
    for idx, u in enumerate(all_users):
        if u.id == user.id:
            rank = idx + 1
            break
            
    league = "Diamond" if user.xp >= 1500 else "Obsidian" if user.xp >= 800 else "Gold" if user.xp >= 300 else "Silver" if user.xp >= 100 else "Bronze"
    
    return {
        "daily_goal_progress": daily_xp,
        "daily_goal_completed": daily_completed,
        "completed_skills_count": completed_skills,
        "completed_lessons_count": completed_lessons,
        "crowns_count": crowns_count,
        "league": league,
        "rank": rank
    }
