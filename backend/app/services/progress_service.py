from sqlalchemy.orm import Session
from ..models import User, Course, Unit, Skill, Lesson, UserSkillProgress

def ensure_user_progress_initialized(user: User, db: Session):
    """Ensures user has progress entries for all skills in course, with proper locked/available status."""
    skills = db.query(Skill).join(Unit).join(Course).order_by(Unit.order_index, Skill.order_index).all()
    if not skills:
        return

    progress_map = {
        p.skill_id: p for p in db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).all()
    }

    prev_skill_completed = True  # First skill starts available
    for idx, skill in enumerate(skills):
        progress = progress_map.get(skill.id)
        if not progress:
            status = "available" if (idx == 0 or prev_skill_completed) else "locked"
            progress = UserSkillProgress(
                user_id=user.id,
                skill_id=skill.id,
                status=status,
                xp=0,
                crown_level=0,
                completed_lessons=0
            )
            db.add(progress)
            db.commit()
            db.refresh(progress)
            progress_map[skill.id] = progress

        prev_skill_completed = (progress.status == "completed")

def get_learning_path_data(user: User, db: Session):
    """Fetches full structured learning path with units, skills, lesson counts and user progress."""
    ensure_user_progress_initialized(user, db)

    course = db.query(Course).first()
    if not course:
        return None

    progress_map = {
        p.skill_id: p for p in db.query(UserSkillProgress).filter(UserSkillProgress.user_id == user.id).all()
    }

    units_data = []
    for unit in course.units:
        skills_data = []
        for skill in unit.skills:
            prog = progress_map.get(skill.id)
            status = prog.status if prog else "locked"
            crown_level = prog.crown_level if prog else 0
            completed_lessons = prog.completed_lessons if prog else 0

            lessons_data = []
            for lesson in skill.lessons:
                lessons_data.append({
                    "id": lesson.id,
                    "skill_id": lesson.skill_id,
                    "title": lesson.title,
                    "order_index": lesson.order_index,
                    "xp_reward": lesson.xp_reward,
                    "exercise_count": len(lesson.exercises)
                })

            skills_data.append({
                "id": skill.id,
                "unit_id": skill.unit_id,
                "title": skill.title,
                "description": skill.description,
                "order_index": skill.order_index,
                "xp_reward": skill.xp_reward,
                "status": status,
                "crown_level": crown_level,
                "completed_lessons": completed_lessons,
                "total_lessons": len(skill.lessons),
                "lessons": lessons_data
            })

        units_data.append({
            "id": unit.id,
            "course_id": unit.course_id,
            "title": unit.title,
            "description": unit.description,
            "order_index": unit.order_index,
            "skills": skills_data
        })

    return {
        "course_name": course.name,
        "source_language": course.source_language,
        "target_language": course.target_language,
        "units": units_data
    }

def unlock_next_skill(user: User, completed_skill_id: int, db: Session) -> bool:
    """Finds next skill in order and unlocks it if locked."""
    all_skills = db.query(Skill).join(Unit).order_by(Unit.order_index, Skill.order_index).all()
    
    current_idx = -1
    for idx, s in enumerate(all_skills):
        if s.id == completed_skill_id:
            current_idx = idx
            break

    if current_idx != -1 and current_idx + 1 < len(all_skills):
        next_skill = all_skills[current_idx + 1]
        next_progress = db.query(UserSkillProgress).filter(
            UserSkillProgress.user_id == user.id,
            UserSkillProgress.skill_id == next_skill.id
        ).first()

        if not next_progress:
            next_progress = UserSkillProgress(
                user_id=user.id,
                skill_id=next_skill.id,
                status="available",
                xp=0,
                crown_level=0,
                completed_lessons=0
            )
            db.add(next_progress)
            db.commit()
            return True
        elif next_progress.status == "locked":
            next_progress.status = "available"
            db.commit()
            return True

    return False
