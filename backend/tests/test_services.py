import pytest
from datetime import date, timedelta, datetime
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base
from app.models import (
    User, Course, Unit, Skill, Lesson, Exercise, ExerciseOption,
    UserSkillProgress, LessonAttempt, DailyActivity, Achievement, UserAchievement
)
from app.services.lesson_service import (
    normalize_text, strip_accents, validate_user_answer,
    start_lesson_attempt, submit_exercise_answer, finish_lesson
)
from app.services.streak_service import record_activity_and_update_streak
from app.services.progress_service import unlock_next_skill, get_learning_path_data
from app.services.user_service import refill_hearts, practice_heart

@pytest.fixture
def db_session():
    # In-memory SQLite for testing
    engine = create_engine("sqlite:///:memory:", connect_args={"check_same_thread": False})
    Base.metadata.create_all(bind=engine)
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    session = TestingSessionLocal()

    # Seed minimal course structure
    user = User(
        username="test_user",
        display_name="Test User",
        avatar="/avatars/alex.png",
        xp=50,
        gems=100,
        hearts=5,
        streak=1,
        daily_goal=20
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    course = Course(name="Spanish", source_language="English", target_language="Spanish")
    session.add(course)
    session.commit()
    session.refresh(course)

    unit = Unit(course_id=course.id, title="Unit 1", description="Basics", order_index=1)
    session.add(unit)
    session.commit()
    session.refresh(unit)

    skill1 = Skill(unit_id=unit.id, title="Greetings", description="Greetings", order_index=1, xp_reward=10)
    skill2 = Skill(unit_id=unit.id, title="Food", description="Food", order_index=2, xp_reward=10)
    session.add_all([skill1, skill2])
    session.commit()
    session.refresh(skill1)
    session.refresh(skill2)

    lesson1 = Lesson(skill_id=skill1.id, title="Lesson 1", order_index=1, xp_reward=10)
    session.add(lesson1)
    session.commit()
    session.refresh(lesson1)

    ex1 = Exercise(
        lesson_id=lesson1.id,
        type="translate",
        question="Translate 'Hello'",
        correct_answer="Hola",
        order_index=1,
        xp=2
    )
    ex2 = Exercise(
        lesson_id=lesson1.id,
        type="multiple_choice",
        question="Which is coffee?",
        correct_answer="Café",
        order_index=2,
        xp=2
    )
    session.add_all([ex1, ex2])
    session.commit()
    session.refresh(ex1)
    session.refresh(ex2)

    opt1 = ExerciseOption(exercise_id=ex2.id, text="Café", is_correct=True)
    opt2 = ExerciseOption(exercise_id=ex2.id, text="Té", is_correct=False)
    session.add_all([opt1, opt2])

    prog1 = UserSkillProgress(
        user_id=user.id,
        skill_id=skill1.id,
        status="available",
        xp=0,
        crown_level=0,
        completed_lessons=0
    )
    prog2 = UserSkillProgress(
        user_id=user.id,
        skill_id=skill2.id,
        status="locked",
        xp=0,
        crown_level=0,
        completed_lessons=0
    )
    session.add_all([prog1, prog2])
    session.commit()

    yield session
    session.close()


def test_answer_normalization():
    assert normalize_text("  ¡Hola, mundo!  ") == "hola mundo"
    assert normalize_text("Buenos días...") == "buenos días"
    assert strip_accents("Adiós") == "Adios"


def test_answer_validation_varieties(db_session):
    ex = db_session.query(Exercise).filter(Exercise.type == "translate").first()
    assert validate_user_answer(ex, "Hola") is True
    assert validate_user_answer(ex, "  hola! ") is True
    assert validate_user_answer(ex, "Adiós") is False

    # Accent tolerance
    assert validate_user_answer(ex, "hola") is True


def test_hearts_deduction_and_blocking(db_session):
    user = db_session.query(User).first()
    lesson = db_session.query(Lesson).first()
    ex = db_session.query(Exercise).first()

    assert user.hearts == 5

    # Wrong answer removes 1 heart
    res = submit_exercise_answer(user, lesson.id, ex.id, "Wrong Answer", db=db_session)
    assert res["correct"] is False
    assert res["hearts_remaining"] == 4
    assert user.hearts == 4

    # Drop hearts to 0
    user.hearts = 0
    db_session.commit()

    # Further attempt must be blocked
    with pytest.raises(Exception) as exc_info:
        submit_exercise_answer(user, lesson.id, ex.id, "Hola", db=db_session)
    assert "Out of hearts" in str(exc_info.value.detail)

    # Practice restores 1 heart
    practice_heart(user, db_session)
    assert user.hearts == 1

    # Refill restores full 5 hearts
    refill_hearts(user, db_session)
    assert user.hearts == 5


def test_xp_award_and_lesson_completion(db_session):
    user = db_session.query(User).first()
    lesson = db_session.query(Lesson).first()
    ex = db_session.query(Exercise).filter(Exercise.type == "translate").first()

    initial_xp = user.xp
    start_info = start_lesson_attempt(user, lesson.id, db_session)
    attempt_id = start_info["attempt_id"]

    # Correct answer awards exercise xp
    res = submit_exercise_answer(user, lesson.id, ex.id, "Hola", attempt_id=attempt_id, db=db_session)
    assert res["correct"] is True
    assert res["xp_earned"] == 2
    assert user.xp == initial_xp + 2

    # Finish lesson awards bonus xp and updates skill progress
    complete_res = finish_lesson(user, lesson.id, attempt_id=attempt_id, db=db_session)
    assert complete_res["success"] is True
    assert complete_res["xp_earned"] == 10
    assert user.xp == initial_xp + 12
    assert complete_res["skill_progress"]["status"] == "completed"
    assert complete_res["next_skill_unlocked"] is True


def test_streak_calculation_logic(db_session):
    user = db_session.query(User).first()
    user.streak = 0
    db_session.commit()

    today = date.today()
    day1 = today - timedelta(days=2)
    day2 = today - timedelta(days=1)
    day3 = today

    # Day 1 activity: streak starts at 1
    s1 = record_activity_and_update_streak(user, 10, True, db_session, target_date=day1)
    assert s1 == 1

    # Same day extra activity does not increment streak
    s1_again = record_activity_and_update_streak(user, 10, True, db_session, target_date=day1)
    assert s1_again == 1

    # Consecutive Day 2 activity increments streak to 2
    s2 = record_activity_and_update_streak(user, 10, True, db_session, target_date=day2)
    assert s2 == 2

    # Consecutive Day 3 activity increments streak to 3
    s3 = record_activity_and_update_streak(user, 10, True, db_session, target_date=day3)
    assert s3 == 3

    # Skipping day 4 and doing day 5 resets streak to 1
    day5 = today + timedelta(days=2)
    s5 = record_activity_and_update_streak(user, 10, True, db_session, target_date=day5)
    assert s5 == 1


def test_skill_unlocking_logic(db_session):
    user = db_session.query(User).first()
    skills = db_session.query(Skill).order_by(Skill.order_index).all()
    skill1, skill2 = skills[0], skills[1]

    # Skill 2 starts locked
    prog2 = db_session.query(UserSkillProgress).filter(
        UserSkillProgress.user_id == user.id,
        UserSkillProgress.skill_id == skill2.id
    ).first()
    assert prog2.status == "locked"

    # Unlock next skill
    unlocked = unlock_next_skill(user, skill1.id, db_session)
    assert unlocked is True
    db_session.refresh(prog2)
    assert prog2.status == "available"
