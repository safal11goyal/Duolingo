from sqlalchemy.orm import Session
from sqlalchemy import func
from fastapi import HTTPException, status
from ..models import User, Skill, Unit, Course, UserSkillProgress
from ..schemas.user import UserRegister, UserLogin
from .security import hash_password, verify_password

def register_user(db: Session, data: UserRegister) -> User:
    """Registers a new user, hashes password, and initializes their isolated skill progress."""
    normalized_email = data.email.lower().strip()
    normalized_username = data.username.lower().strip()

    # Check existing email
    existing_email = db.query(User).filter(func.lower(User.email) == normalized_email).first()
    if existing_email:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="An account with this email already exists."
        )

    # Check existing username
    existing_username = db.query(User).filter(func.lower(User.username) == normalized_username).first()
    if existing_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="This username is already taken. Please choose another."
        )

    # Create new user record
    new_user = User(
        username=data.username.strip(),
        email=normalized_email,
        password_hash=hash_password(data.password),
        display_name=data.display_name.strip(),
        avatar="/avatars/alex.png",
        xp=0,
        gems=500,
        hearts=5,
        streak=0,
        daily_goal=20
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Initialize fresh skill progress for this specific user
    init_user_skill_progress(new_user, db)

    return new_user

def init_user_skill_progress(user: User, db: Session):
    """Sets up the initial progression for a brand new user: first skill available, others locked."""
    skills = db.query(Skill).join(Unit).join(Course).order_by(Unit.order_index, Skill.order_index).all()
    if not skills:
        return

    for idx, skill in enumerate(skills):
        status_val = "available" if idx == 0 else "locked"
        progress = UserSkillProgress(
            user_id=user.id,
            skill_id=skill.id,
            status=status_val,
            xp=0,
            crown_level=0,
            completed_lessons=0
        )
        db.add(progress)
    db.commit()

def authenticate_user(db: Session, data: UserLogin) -> User:
    """Verifies email and password hash, returning user on success."""
    normalized_email = data.email.lower().strip()
    user = db.query(User).filter(func.lower(User.email) == normalized_email).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Passive heart regeneration
    from ..services.user_service import regenerate_hearts
    regenerate_hearts(user, db)
    return user
