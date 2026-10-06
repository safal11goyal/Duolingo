from datetime import datetime
from typing import List
from sqlalchemy.orm import Session
from ..models import User, Achievement, UserAchievement, LessonAttempt, UserSkillProgress

def check_and_unlock_achievements(user: User, db: Session, is_perfect_lesson: bool = False) -> List[str]:
    """
    Checks all achievements and unlocks any eligible ones that haven't been unlocked yet.
    Returns a list of newly unlocked achievement names.
    """
    all_achievements = db.query(Achievement).all()
    user_unlocked = {
        ua.achievement_id for ua in db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    }

    # Aggregate user stats
    completed_lessons_count = db.query(LessonAttempt).filter(
        LessonAttempt.user_id == user.id,
        LessonAttempt.completed == True
    ).count()

    total_crowns = db.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user.id
    ).all()
    crowns_count = sum(p.crown_level for p in total_crowns)

    newly_unlocked_names = []

    for ach in all_achievements:
        if ach.id in user_unlocked:
            continue

        eligible = False
        if ach.requirement_type == "first_lesson" and completed_lessons_count >= ach.requirement_value:
            eligible = True
        elif ach.requirement_type == "streak" and user.streak >= ach.requirement_value:
            eligible = True
        elif ach.requirement_type == "xp" and user.xp >= ach.requirement_value:
            eligible = True
        elif ach.requirement_type == "perfect_lesson" and is_perfect_lesson:
            eligible = True
        elif ach.requirement_type == "crowns" and crowns_count >= ach.requirement_value:
            eligible = True

        if eligible:
            new_ua = UserAchievement(
                user_id=user.id,
                achievement_id=ach.id,
                unlocked_at=datetime.utcnow()
            )
            db.add(new_ua)
            newly_unlocked_names.append(ach.name)

    if newly_unlocked_names:
        db.commit()

    return newly_unlocked_names

def get_user_achievements_status(user: User, db: Session):
    """Returns all achievements with progress and unlock status for the user."""
    all_achievements = db.query(Achievement).all()
    user_unlocked_map = {
        ua.achievement_id: ua.unlocked_at
        for ua in db.query(UserAchievement).filter(UserAchievement.user_id == user.id).all()
    }

    completed_lessons_count = db.query(LessonAttempt).filter(
        LessonAttempt.user_id == user.id,
        LessonAttempt.completed == True
    ).count()

    crowns_count = sum(
        p.crown_level
        for p in db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).all()
    )

    results = []
    for ach in all_achievements:
        unlocked = ach.id in user_unlocked_map
        progress = 0
        if ach.requirement_type == "first_lesson":
            progress = min(ach.requirement_value, completed_lessons_count)
        elif ach.requirement_type == "streak":
            progress = min(ach.requirement_value, user.streak)
        elif ach.requirement_type == "xp":
            progress = min(ach.requirement_value, user.xp)
        elif ach.requirement_type == "perfect_lesson":
            progress = 1 if unlocked else 0
        elif ach.requirement_type == "crowns":
            progress = min(ach.requirement_value, crowns_count)

        results.append({
            "id": ach.id,
            "name": ach.name,
            "description": ach.description,
            "icon": ach.icon,
            "requirement_type": ach.requirement_type,
            "requirement_value": ach.requirement_value,
            "unlocked": unlocked,
            "unlocked_at": user_unlocked_map.get(ach.id),
            "progress": progress
        })

    return results
