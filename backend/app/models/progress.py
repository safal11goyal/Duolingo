from datetime import datetime, timezone
from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, UniqueConstraint
from sqlalchemy.orm import relationship
from ..database import Base

def utcnow():
    return datetime.now(timezone.utc)

class UserSkillProgress(Base):
    __tablename__ = "user_skill_progresses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False, index=True)
    status = Column(String(50), nullable=False, default="locked")  # locked, available, in_progress, completed
    xp = Column(Integer, nullable=False, default=0)
    crown_level = Column(Integer, nullable=False, default=0)
    completed_lessons = Column(Integer, nullable=False, default=0)
    updated_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    __table_args__ = (
        UniqueConstraint("user_id", "skill_id", name="uq_user_skill"),
    )

    user = relationship("User", back_populates="skill_progresses")
    skill = relationship("Skill", back_populates="user_progresses")


class LessonAttempt(Base):
    __tablename__ = "lesson_attempts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False, index=True)
    started_at = Column(DateTime, default=utcnow, nullable=False)
    completed_at = Column(DateTime, nullable=True)
    score = Column(Integer, nullable=False, default=0)
    correct_answers = Column(Integer, nullable=False, default=0)
    wrong_answers = Column(Integer, nullable=False, default=0)
    xp_earned = Column(Integer, nullable=False, default=0)
    hearts_lost = Column(Integer, nullable=False, default=0)
    completed = Column(Boolean, nullable=False, default=False)
    attempts = Column(Integer, nullable=False, default=1)
    last_attempted_at = Column(DateTime, default=utcnow, onupdate=utcnow, nullable=False)

    user = relationship("User", back_populates="lesson_attempts")
    lesson = relationship("Lesson", back_populates="attempts")
    answers = relationship("UserAnswer", back_populates="attempt", cascade="all, delete-orphan")


class UserAnswer(Base):
    __tablename__ = "user_answers"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, index=True)
    question_id = Column(Integer, ForeignKey("exercises.id"), nullable=False, index=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=True, index=True)
    attempt_id = Column(Integer, ForeignKey("lesson_attempts.id"), nullable=True, index=True)
    submitted_answer = Column(String(500), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime, default=utcnow, nullable=False)

    user = relationship("User", back_populates="answers")
    question = relationship("Exercise")
    lesson = relationship("Lesson")
    attempt = relationship("LessonAttempt", back_populates="answers")

