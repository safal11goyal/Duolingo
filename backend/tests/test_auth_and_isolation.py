import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database import Base, get_db
from app.main import app
from app.models import Course, Unit, Skill, Lesson, Exercise, ExerciseOption

from sqlalchemy.pool import StaticPool

# Set up test database with StaticPool so in-memory DB persists across connections
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

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module", autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()

    # Seed Course, Unit, Skills, Lessons
    course = Course(name="Spanish", source_language="English", target_language="Spanish")
    db.add(course)
    db.commit()
    db.refresh(course)

    unit = Unit(course_id=course.id, title="Unit 1", description="Basics", order_index=1)
    db.add(unit)
    db.commit()
    db.refresh(unit)

    skill1 = Skill(unit_id=unit.id, title="Greetings", description="Say hello", order_index=1, xp_reward=10)
    skill2 = Skill(unit_id=unit.id, title="Food", description="Order food", order_index=2, xp_reward=10)
    db.add_all([skill1, skill2])
    db.commit()
    db.refresh(skill1)
    db.refresh(skill2)

    lesson1 = Lesson(skill_id=skill1.id, title="Lesson 1", order_index=1, xp_reward=10)
    lesson2 = Lesson(skill_id=skill2.id, title="Lesson 2", order_index=1, xp_reward=10)
    db.add_all([lesson1, lesson2])
    db.commit()
    db.refresh(lesson1)
    db.refresh(lesson2)

    ex1 = Exercise(
        lesson_id=lesson1.id,
        type="translate",
        question="Translate 'Hello'",
        correct_answer="Hola",
        order_index=1,
        xp=2
    )
    db.add(ex1)
    db.commit()
    db.close()
    yield
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client():
    return TestClient(app)


def test_unauthenticated_requests_are_rejected(client):
    """Protected endpoints must return 401 without valid JWT."""
    assert client.get("/api/auth/me").status_code == 401
    assert client.get("/api/me").status_code == 401
    assert client.get("/api/profile").status_code == 401
    assert client.get("/api/path").status_code == 401
    assert client.get("/api/lessons/1").status_code == 401
    assert client.post("/api/lessons/1/start").status_code == 401


def test_user_registration_and_login(client):
    """User can register and log in, receiving JWT token and HTTP-only cookie."""
    reg_res = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "alice@example.com",
        "password": "Password123!",
        "display_name": "Alice Wonderland"
    })
    assert reg_res.status_code == 200, reg_res.text
    reg_data = reg_res.json()
    assert "access_token" in reg_data
    assert reg_data["user"]["username"] == "alice"
    assert reg_data["user"]["email"] == "alice@example.com"
    # Never expose password_hash or password in response
    assert "password" not in reg_data["user"]
    assert "password_hash" not in reg_data["user"]

    # Duplicate registration fails
    dup_res = client.post("/api/auth/register", json={
        "username": "alice",
        "email": "another@example.com",
        "password": "Password123!",
        "display_name": "Alice 2"
    })
    assert dup_res.status_code == 400

    # Login with wrong password fails
    wrong_pw_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "WrongPassword"
    })
    assert wrong_pw_res.status_code == 401

    # Login with correct password succeeds
    login_res = client.post("/api/auth/login", json={
        "email": "alice@example.com",
        "password": "Password123!"
    })
    assert login_res.status_code == 200
    login_data = login_res.json()
    assert "access_token" in login_data
    assert "access_token" in login_res.cookies


def test_user_data_isolation(client):
    """
    Proves strict isolation between User A and User B:
    - User A's XP, hearts, streak, and completed skills do not affect User B.
    - User B cannot view User A's progress or tamper with User A's lesson attempts.
    """
    # 1. Register User A (User "A")
    res_a = client.post("/api/auth/register", json={
        "username": "usera",
        "email": "usera@example.com",
        "password": "Password123!",
        "display_name": "User A"
    })
    assert res_a.status_code == 200
    token_a = res_a.json()["access_token"]
    headers_a = {"Authorization": f"Bearer {token_a}"}

    # 2. Register User B (User "B")
    res_b = client.post("/api/auth/register", json={
        "username": "userb",
        "email": "userb@example.com",
        "password": "Password123!",
        "display_name": "User B"
    })
    assert res_b.status_code == 200
    token_b = res_b.json()["access_token"]
    headers_b = {"Authorization": f"Bearer {token_b}"}

    # Verify initial stats for both users
    profile_a = client.get("/api/profile", headers=headers_a).json()
    profile_b = client.get("/api/profile", headers=headers_b).json()

    assert profile_a["xp"] == 0
    assert profile_a["hearts"] == 5
    assert profile_a["streak"] == 0

    assert profile_b["xp"] == 0
    assert profile_b["hearts"] == 5
    assert profile_b["streak"] == 0

    # User A starts and completes lesson 1
    start_res_a = client.post("/api/lessons/1/start", headers=headers_a)
    assert start_res_a.status_code == 200
    attempt_a_id = start_res_a.json()["attempt_id"]

    # User A answers exercise
    ans_res_a = client.post("/api/lessons/1/answer", headers=headers_a, json={
        "exercise_id": 1,
        "answer": "Hola",
        "attempt_id": attempt_a_id
    })
    assert ans_res_a.status_code == 200
    assert ans_res_a.json()["correct"] is True

    # User A completes lesson 1
    comp_res_a = client.post("/api/lessons/1/complete", headers=headers_a, json={
        "attempt_id": attempt_a_id
    })
    assert comp_res_a.status_code == 200

    # Verify User A's progress updated
    new_profile_a = client.get("/api/profile", headers=headers_a).json()
    assert new_profile_a["xp"] > 0
    assert new_profile_a["streak"] == 1
    assert new_profile_a["completed_lessons_count"] == 1

    path_a = client.get("/api/path", headers=headers_a).json()
    skill1_a = path_a["units"][0]["skills"][0]
    skill2_a = path_a["units"][0]["skills"][1]
    assert skill1_a["status"] == "completed"
    assert skill2_a["status"] == "available"  # unlocked for User A

    # CRITICAL CHECK: User B's progress MUST be completely untouched
    new_profile_b = client.get("/api/profile", headers=headers_b).json()
    assert new_profile_b["xp"] == 0, "User B XP must remain 0"
    assert new_profile_b["streak"] == 0, "User B streak must remain 0"
    assert new_profile_b["completed_lessons_count"] == 0, "User B must have 0 completed lessons"

    path_b = client.get("/api/path", headers=headers_b).json()
    skill1_b = path_b["units"][0]["skills"][0]
    skill2_b = path_b["units"][0]["skills"][1]
    assert skill1_b["status"] == "available"  # still available for User B
    assert skill2_b["status"] == "locked", "User B skill 2 must remain locked"

    # User B cannot access locked Skill 2 / Lesson 2
    lesson2_b = client.get("/api/lessons/2", headers=headers_b)
    assert lesson2_b.status_code == 403, "User B must not be able to access locked lesson"

    # TAMPERING CHECK: User B attempts to answer using User A's attempt ID
    tamper_ans = client.post("/api/lessons/1/answer", headers=headers_b, json={
        "exercise_id": 1,
        "answer": "Hola",
        "attempt_id": attempt_a_id
    })
    assert tamper_ans.status_code == 403, "User B cannot answer on User A attempt"

    # TAMPERING CHECK: User B attempts to complete User A's lesson attempt
    tamper_comp = client.post("/api/lessons/1/complete", headers=headers_b, json={
        "attempt_id": attempt_a_id
    })
    assert tamper_comp.status_code == 403, "User B cannot complete User A attempt"

    # Logout verification
    logout_res = client.post("/api/auth/logout", headers=headers_a)
    assert logout_res.status_code == 200
