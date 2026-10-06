from fastapi import Depends
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import User
from ..services.user_service import get_default_user

def get_current_user(db: Session = Depends(get_db)) -> User:
    """Dependency that returns the current authenticated user (Alex)."""
    return get_default_user(db)
