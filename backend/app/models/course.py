from sqlalchemy import Column, Integer, String, Text, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from ..database import Base

class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    source_language = Column(String(50), nullable=False, default="English")
    target_language = Column(String(50), nullable=False, default="Spanish")

    units = relationship("Unit", back_populates="course", cascade="all, delete-orphan", order_by="Unit.order_index")


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    course_id = Column(Integer, ForeignKey("courses.id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False, default=1)

    course = relationship("Course", back_populates="units")
    skills = relationship("Skill", back_populates="unit", cascade="all, delete-orphan", order_by="Skill.order_index")


class Skill(Base):
    __tablename__ = "skills"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    unit_id = Column(Integer, ForeignKey("units.id"), nullable=False)
    title = Column(String(150), nullable=False)
    description = Column(Text, nullable=False)
    order_index = Column(Integer, nullable=False, default=1)
    xp_reward = Column(Integer, nullable=False, default=10)

    unit = relationship("Unit", back_populates="skills")
    lessons = relationship("Lesson", back_populates="skill", cascade="all, delete-orphan", order_by="Lesson.order_index")
    user_progresses = relationship("UserSkillProgress", back_populates="skill", cascade="all, delete-orphan")


class Lesson(Base):
    __tablename__ = "lessons"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    skill_id = Column(Integer, ForeignKey("skills.id"), nullable=False)
    title = Column(String(150), nullable=False)
    order_index = Column(Integer, nullable=False, default=1)
    xp_reward = Column(Integer, nullable=False, default=10)

    skill = relationship("Skill", back_populates="lessons")
    exercises = relationship("Exercise", back_populates="lesson", cascade="all, delete-orphan", order_by="Exercise.order_index")
    attempts = relationship("LessonAttempt", back_populates="lesson", cascade="all, delete-orphan")


class Exercise(Base):
    __tablename__ = "exercises"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    lesson_id = Column(Integer, ForeignKey("lessons.id"), nullable=False)
    type = Column(String(50), nullable=False)  # multiple_choice, translate, word_bank, match_pairs, fill_blank, type_answer
    question = Column(Text, nullable=False)
    correct_answer = Column(Text, nullable=False)
    explanation = Column(Text, nullable=True)
    order_index = Column(Integer, nullable=False, default=1)
    xp = Column(Integer, nullable=False, default=2)

    lesson = relationship("Lesson", back_populates="exercises")
    options = relationship("ExerciseOption", back_populates="exercise", cascade="all, delete-orphan")


class ExerciseOption(Base):
    __tablename__ = "exercise_options"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    exercise_id = Column(Integer, ForeignKey("exercises.id"), nullable=False)
    text = Column(String(255), nullable=False)
    is_correct = Column(Boolean, nullable=False, default=False)

    exercise = relationship("Exercise", back_populates="options")
