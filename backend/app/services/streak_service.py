from datetime import date, timedelta, datetime, timezone
from sqlalchemy.orm import Session
from ..models import User, DailyActivity

def record_activity_and_update_streak(user: User, xp_gained: int, lesson_completed: bool, db: Session, target_date: date = None) -> int:
    """
    Records daily activity for user and calculates current streak.
    
    Rules:
    - If activity already exists for today: add xp_earned and lessons_completed, streak remains current.
    - If no activity yet for today:
        - Check the most recent activity date before today.
        - If that date was yesterday (today - 1 day): streak = user.streak + 1.
        - If that date was older than yesterday (or no prior activity): streak = 1.
    """
    if target_date is None:
        target_date = date.today()

    # Look for existing activity on target_date
    today_activity = db.query(DailyActivity).filter(
        DailyActivity.user_id == user.id,
        DailyActivity.activity_date == target_date
    ).first()

    if today_activity:
        today_activity.xp_earned += xp_gained
        if lesson_completed:
            today_activity.lessons_completed += 1
    else:
        # Check previous activity
        prev_activity = db.query(DailyActivity).filter(
            DailyActivity.user_id == user.id,
            DailyActivity.activity_date < target_date
        ).order_by(DailyActivity.activity_date.desc()).first()

        yesterday = target_date - timedelta(days=1)
        if prev_activity and prev_activity.activity_date == yesterday:
            user.streak = max(1, user.streak + 1)
        else:
            user.streak = 1

        # Create new daily activity record
        today_activity = DailyActivity(
            user_id=user.id,
            activity_date=target_date,
            xp_earned=xp_gained,
            lessons_completed=1 if lesson_completed else 0
        )
        db.add(today_activity)

    now = datetime.now(timezone.utc)
    user.last_active_at = now
    user.updated_at = now
    db.commit()
    db.refresh(user)
    return user.streak
