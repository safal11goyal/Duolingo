import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app
from app.models import Course, Unit, Skill, Lesson, Exercise, UserAnswer, LessonAttempt
from alembic.config import Config
from alembic import command

# Setup persistent test in-memory SQLite database
engine = create_engine(
    "sqlite:///:memory:",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

@pytest.fixture(scope="module")
def client():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    course = Course(
        name="Spanish",
        source_language="English",
        target_language="Spanish",
        description="Learn Spanish from English",
        difficulty="beginner"
    )
    db.add(course)
    db.commit()
    db.refresh(course)

    unit = Unit(course_id=course.id, title="Unit 1", description="Basics", order_index=1)
    db.add(unit)
    db.commit()
    db.refresh(unit)

    skill = Skill(unit_id=unit.id, title="Greetings", description="Basics", order_index=1, xp_reward=10)
    db.add(skill)
    db.commit()
    db.refresh(skill)

    lesson = Lesson(
        skill_id=skill.id,
        course_id=course.id,
        title="Lesson 1",
        description="Introduction to Greetings",
        order_index=1,
        xp_reward=10
    )
    db.add(lesson)
    db.commit()
    db.refresh(lesson)

    ex = Exercise(
        lesson_id=lesson.id,
        type="multiple_choice",
        question="Select 'Hello'",
        correct_answer="Hola",
        order_index=1,
        xp=5
    )
    db.add(ex)
    db.commit()
    db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.pop(get_db, None)


def test_migration_and_crud_endpoints(client):
    # 1. Register via /register or /api/auth/register
    res = client.post("/register", json={
        "username": "migrated_user",
        "email": "migrated@example.com",
        "password": "Password123!",
        "display_name": "Migrated User"
    })
    assert res.status_code == 200
    token = res.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    # 2. Test /me
    me_res = client.get("/me", headers=headers)
    assert me_res.status_code == 200
    assert me_res.json()["email"] == "migrated@example.com"
    assert "password_hash" not in me_res.json()

    # 3. Test /courses
    courses_res = client.get("/courses")
    assert courses_res.status_code == 200
    courses = courses_res.json()
    assert len(courses) >= 1
    assert courses[0]["name"] == "Spanish"

    # 4. Test /lessons
    lessons_res = client.get("/lessons")
    assert lessons_res.status_code == 200
    lessons = lessons_res.json()
    assert len(lessons) >= 1

    # 5. Test /questions
    questions_res = client.get(f"/questions?lesson_id={lessons[0]['id']}")
    assert questions_res.status_code == 200
    questions = questions_res.json()
    assert len(questions) >= 1
    assert questions[0]["correct_answer"] == "Hola"

    # 6. Start lesson and answer question
    start_res = client.post(f"/api/lessons/{lessons[0]['id']}/start", headers=headers)
    assert start_res.status_code == 200
    attempt_id = start_res.json()["attempt_id"]

    ans_res = client.post(f"/api/lessons/{lessons[0]['id']}/answer", headers=headers, json={
        "exercise_id": questions[0]["id"],
        "answer": "Hola",
        "attempt_id": attempt_id
    })
    assert ans_res.status_code == 200
    assert ans_res.json()["correct"] is True

    # Complete lesson
    comp_res = client.post(f"/api/lessons/{lessons[0]['id']}/complete", headers=headers, json={
        "attempt_id": attempt_id
    })
    assert comp_res.status_code == 200

    # 7. Test /progress
    prog_res = client.get("/progress", headers=headers)
    assert prog_res.status_code == 200
    progress = prog_res.json()
    assert progress["xp"] > 0
    assert len(progress["lessons"]) >= 1
    assert progress["lessons"][0]["completed"] is True
    assert progress["lessons"][0]["attempts"] >= 1

    # 8. Test /answers
    ans_list_res = client.get("/answers", headers=headers)
    assert ans_list_res.status_code == 200
    user_answers = ans_list_res.json()
    assert len(user_answers) >= 1
    assert user_answers[0]["submitted_answer"] == "Hola"
    assert user_answers[0]["is_correct"] is True
