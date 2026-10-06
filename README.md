# 🦉 Duolingo Clone — Full-Stack Language Learning Web App

A production-quality full-stack Duolingo clone reproducing the overall visual design, interaction patterns, lesson flow, curved learning path, and gamification mechanics of the modern Duolingo web application.

---

## 📑 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [System Architecture](#system-architecture)
- [Folder Structure](#folder-structure)
- [Database Schema & ER Diagram](#database-schema--er-diagram)
- [API Reference](#api-reference)
- [Setup & Installation](#setup--installation)
- [Automated Testing](#automated-testing)
- [Design Decisions & Interview Guide](#design-decisions--interview-guide)

---

## 🌟 Project Overview

This application delivers the authentic Duolingo language learning experience:
- **Playful Design Language**: Vibrant color scheme (Duolingo Green `#58cc02`, Blue `#1cb0f6`, Yellow `#ffc800`, Red `#ff4b4b`), tactile 3D physical keys (`border-b-4` buttons), micro-animations, and animated SVG mascot expressions (happy, thinking, cheering, celebrate, sad).
- **Curved Vertical Learning Path**: Snake progression path with Units, interactive Skill Nodes (completed with crowns, active with pulse animations, locked with padlocks), and start popups.
- **Dynamic Lesson Player**: 6 distinct interactive exercise types with backend validation, progress bar, hearts depletion, audio feedback, and celebratory confetti completion screen.
- **Deep Gamification**: Persistent XP, Hearts system with regeneration & practice refill, daily streaks with date simulation tools, daily XP goals, leagues, and unlockable achievements.

---

## ✨ Key Features

### 1. Interactive Lesson Player (`/lesson/[lessonId]`)
- **6 Exercise Types**:
  1. **Multiple Choice**: Tactile selectable cards with keyboard shortcuts (`1`, `2`, `3`, `4`).
  2. **Translate**: Speech synthesis audio button, clean input, and quick Spanish accent toolbar (`á`, `é`, `í`, `ó`, `ú`, `ñ`, `¿`, `¡`).
  3. **Word Bank**: Sentence builder with animated word chips that bounce into answer slots and return upon click.
  4. **Match Pairs**: Interactive two-column tile matching with pair status highlights.
  5. **Fill in the Blank**: Inline sentence slot with selectable word chips.
  6. **Type the Answer**: Keyboard input with accent bar and Enter-key submission.
- **Signature Feedback Bar**:
  - Green banner for correct answers with chime sound and encouragement.
  - Red banner for mistakes with shake animation, correct solution, and explanation.
- **Zero Hearts Flow**: Out-of-hearts modal offering free practice or instant full refill.
- **Celebration Screen**: Confetti burst, XP summary (+bonus completion XP), streak counter, and crown level-ups.

### 2. Vertical Learning Path (`/learn`)
- Unit banners with titles, descriptions, and guidebook triggers.
- Sine-wave curved node path with crown levels, checkmarks, active rings, and locks.
- Real-time right sidebar widgets: Daily Goal tracker, Hearts status, and League standings.

### 3. Gamification Engine
- **Hearts System**: 5 hearts max; wrong answers deduct 1 heart; passive regeneration (1 heart / 30 mins) or practice refill.
- **Streak Tracking**: Deterministic consecutive day calculation backed by `DailyActivity`; resets if a day is skipped; includes a test date simulation panel.
- **Daily XP Goal**: Configurable goals (Casual 10 XP, Regular 20 XP, Serious 30 XP, Intense 50 XP) with progress bar and completion celebration.
- **Leaderboard (`/leaderboard`)**: Dynamic ranking of seeded users and leagues (Bronze, Silver, Gold, Obsidian, Diamond) with user rank highlighted.
- **Achievements (`/profile`)**: Auto-unlocked badges (First Step, Wildfire, Sage, Scholar, Legend, Sharpshooter, Crown Collector).
- **Audio Synthesizer**: Web Audio API audio cues (clean chimes, buzzers, and arpeggios) plus Spanish speech synthesis.

---

## 🛠️ Tech Stack

- **Frontend**:
  - **Framework**: Next.js 16 (App Router)
  - **Language**: TypeScript
  - **Styling**: Tailwind CSS with custom 3D button utilities
  - **Icons & Effects**: `lucide-react`, `canvas-confetti`
  - **Audio**: Web Audio API synthesizer + Web Speech API (zero external sound file dependencies)
- **Backend**:
  - **Framework**: FastAPI (Python 3.14 / 3.10+)
  - **ORM**: SQLAlchemy 2.0
  - **Validation**: Pydantic v2
  - **Database**: SQLite (Zero configuration local database)
  - **Testing**: `pytest`, `httpx`

---

## 🏛️ System Architecture

```text
       ┌───────────────────────────────┐
       │     Next.js Frontend (React)   │
       │   - App Router Pages          │
       │   - Custom 3D Components      │
       │   - Web Audio & Speech        │
       └──────────────┬────────────────┘
                      │ REST API (JSON)
                      ▼
       ┌───────────────────────────────┐
       │       FastAPI API Router      │
       │   - /api/me, /api/path        │
       │   - /api/lessons/{id}/...     │
       │   - /api/leaderboard, etc.    │
       └──────────────┬────────────────┘
                      │
                      ▼
       ┌───────────────────────────────┐
       │         Service Layer         │
       │   - lesson_service.py         │
       │   - progress_service.py       │
       │   - streak_service.py         │
       │   - achievement_service.py    │
       │   - user_service.py           │
       └──────────────┬────────────────┘
                      │ SQLAlchemy ORM
                      ▼
       ┌───────────────────────────────┐
       │       SQLite Database         │
       │   - duolingo.db (Persistent)  │
       └───────────────────────────────┘
```

---

## 📁 Folder Structure

```text
Duolingo/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── database.py             # SQLite engine & session management
│   │   ├── main.py                 # FastAPI application & CORS
│   │   ├── seed.py                 # Comprehensive Spanish course seeder
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── user.py
│   │   │   ├── course.py
│   │   │   ├── progress.py
│   │   │   └── gamification.py
│   │   ├── schemas/                # Pydantic v2 request/response schemas
│   │   │   ├── user.py
│   │   │   ├── course.py
│   │   │   ├── lesson.py
│   │   │   └── gamification.py
│   │   ├── services/               # Core business logic services
│   │   │   ├── user_service.py
│   │   │   ├── progress_service.py
│   │   │   ├── lesson_service.py
│   │   │   ├── streak_service.py
│   │   │   └── achievement_service.py
│   │   └── routers/                # REST API routers
│   │       ├── auth.py
│   │       ├── path.py
│   │       ├── lessons.py
│   │       ├── gamification.py
│   │       ├── dev.py
│   │       └── deps.py
│   ├── tests/
│   │   └── test_services.py        # Pytest test suite for backend services
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx
│   │   │   ├── globals.css         # Duolingo 3D button utilities
│   │   │   ├── page.tsx            # Redirects to /learn
│   │   │   ├── learn/page.tsx      # Main learning path & widgets
│   │   │   ├── lesson/[lessonId]/  # Fullscreen lesson player
│   │   │   ├── leaderboard/        # League standings
│   │   │   ├── profile/            # Stats & dev simulator tools
│   │   │   └── settings/           # Daily goal & audio options
│   │   ├── components/
│   │   │   ├── layout/             # Sidebar, TopHeader, MobileNav
│   │   │   ├── path/               # UnitHeader, SkillNode, PathRightSidebar
│   │   │   ├── lesson/             # Exercise components, FeedbackBar, Modals
│   │   │   └── ui/                 # DuoMascot SVG component
│   │   └── lib/
│   │       ├── api.ts              # Typed REST client
│   │       ├── types.ts            # TypeScript interfaces
│   │       └── sound.ts            # Web Audio API synthesizers
│   └── package.json
│
└── README.md
```

---

## 📊 Database Schema & ER Diagram

```text
+-------------------+             +-------------------+             +--------------------+
|       User        |             |      Course       |             |        Unit        |
+-------------------+             +-------------------+             +--------------------+
| id (PK)           |             | id (PK)           | 1         * | id (PK)            |
| username          |             | name              |-------------| course_id (FK)     |
| display_name      |             | source_language   |             | title              |
| avatar            |             | target_language   |             | description        |
| xp                |             +-------------------+             | order_index        |
| gems              |                                               +--------------------+
| hearts            |                                                         | 1
| streak            |                                                         | *
| daily_goal        |                                               +--------------------+
| last_active_at    |                                               |       Skill        |
| created_at        |                                               +--------------------+
+-------------------+                                               | id (PK)            |
   | 1         | 1                                                  | unit_id (FK)       |
   |           |                                                    | title              |
   | *         | *                                                  | description        |
+----------------------+   +-----------------------+                | order_index        |
|  UserSkillProgress   |   |     LessonAttempt     |                | xp_reward          |
+----------------------+   +-----------------------+                +--------------------+
| id (PK)              |   | id (PK)               |                          | 1
| user_id (FK)         |   | user_id (FK)          |                          | *
| skill_id (FK)        |   | lesson_id (FK)        |                +--------------------+
| status               |   | started_at            |                |       Lesson       |
| xp                   |   | completed_at          |                +--------------------+
| crown_level          |   | correct_answers       |                | id (PK)            |
| completed_lessons    |   | wrong_answers         |                | skill_id (FK)      |
+----------------------+   | xp_earned             |                | title              |
                           | completed             |                | order_index        |
                           +-----------------------+                | xp_reward          |
                                                                    +--------------------+
                                                                              | 1
                                                                              | *
+----------------------+   +-----------------------+                +--------------------+
|    DailyActivity     |   |      Achievement      |                |      Exercise      |
+----------------------+   +-----------------------+                +--------------------+
| id (PK)              |   | id (PK)               | 1            * | id (PK)            |
| user_id (FK)         |   | name                  |----------------| lesson_id (FK)     |
| activity_date        |   | requirement_type      |                | type               |
| xp_earned            |   | requirement_value     |                | question           |
| lessons_completed    |   +-----------------------+                | correct_answer     |
+----------------------+               | 1                          | xp                 |
                                       | *                          +--------------------+
                           +-----------------------+                          | 1
                           |    UserAchievement    |                          | *
                           +-----------------------+                +--------------------+
                           | user_id (FK)          |                |   ExerciseOption   |
                           | achievement_id (FK)   |                +--------------------+
                           | unlocked_at           |                | id (PK)            |
                           +-----------------------+                | exercise_id (FK)   |
                                                                    | text               |
                                                                    | is_correct         |
                                                                    +--------------------+
```

---

## 🔌 API Reference

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/me` | Fetch active learner info (Alex) |
| `GET` | `/api/profile` | Detailed stats, crowns, streak, league |
| `GET` | `/api/path` | Complete hierarchical units, skills, and progress |
| `GET` | `/api/lessons/{id}` | Lesson detail with sanitized exercises (answers hidden) |
| `POST` | `/api/lessons/{id}/start` | Initialize lesson attempt, verify hearts and lock status |
| `POST` | `/api/lessons/{id}/answer` | Submit answer for backend validation and hearts/XP calculation |
| `POST` | `/api/lessons/{id}/complete` | Finalize lesson, award completion XP, update streak & progress |
| `GET` | `/api/leaderboard` | Ranked user standings and league brackets |
| `GET` | `/api/achievements` | List achievements with user progress and unlocked timestamps |
| `POST` | `/api/hearts/refill` | Instantly restores hearts to full 5 |
| `POST` | `/api/hearts/practice` | Earns +1 heart via practice session |
| `POST` | `/api/dev/simulate-activity`| Simulate learning on specific date for streak verification |
| `POST` | `/api/dev/reset-progress` | Resets learner progress for fresh testing |

### Example: Submit Answer
**Request:**
```http
POST /api/lessons/1/answer
Content-Type: application/json

{
  "exercise_id": 1,
  "answer": "Hola",
  "attempt_id": 3
}
```
**Response (Correct):**
```json
{
  "correct": true,
  "correct_answer": "Hola",
  "explanation": "'Hola' is the universal Spanish greeting for hello.",
  "xp_earned": 2,
  "hearts_remaining": 5,
  "is_lesson_complete": false
}
```

---

## 🚀 Setup & Installation

### Prerequisites
- Python 3.10+
- Node.js 18+ and npm

### 1. Backend Setup
```bash
cd backend

# Create and activate virtual environment
python -m venv venv

# Windows:
.\venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Seed the database
python -m app.seed

# Run FastAPI server
uvicorn app.main:app --port 8000 --reload
```
API docs will be available at `http://localhost:8000/docs`.

### 2. Frontend Setup
```bash
cd frontend

# Install dependencies
npm install

# Run Next.js development server
npm run dev
```
Open `http://localhost:3000` in your browser.

---

## 🧪 Automated Testing

### Backend Unit & Integration Tests
The backend test suite covers:
- Answer validation & text normalization (casing, whitespace, accent tolerance)
- Heart deduction, non-negative limits, and zero-heart blocking
- XP awarding and duplicate submission protection
- Consecutive daily streak incrementing, maintenance, and reset logic
- Skill unlocking and crown progression

Run tests with `pytest`:
```bash
cd backend
.\venv\Scripts\pytest -v
```

---

## 💡 Design Decisions & Interview Guide

### 1. Why SQLite?
SQLite provides a zero-setup, serverless, self-contained SQL database stored in a single file (`duolingo.db`). It eliminates external dependencies for local development and reviewers while providing ACID compliance and standard SQL capabilities.

### 2. Why SQLAlchemy?
SQLAlchemy 2.0 provides an enterprise ORM with strong relationship mapping, typed queries, and clear separation of database schemas. It allows seamless migration to PostgreSQL or MySQL simply by changing the connection string without rewriting business logic.

### 3. Why FastAPI?
FastAPI offers asynchronous request handling, automatic schema validation via Pydantic v2, and auto-generated Swagger documentation (`/docs`).

### 4. How Lesson State and Answer Validation Work
Exercises fetched by the frontend (`GET /api/lessons/{id}`) are sanitized: correct answers and `is_correct` flags are stripped on the backend. When a learner checks their answer, the raw input is submitted to `POST /api/lessons/{id}/answer`. The backend service applies case, punctuation, whitespace, and diacritic normalization, compares it with stored truth, and determines correctness.

### 5. How XP and Hearts are Protected
The frontend never submits XP or heart values. The backend service decrements hearts on failed submissions, enforces the zero-heart boundary, and adds XP upon validated answers and lesson completions.

### 6. How Daily Streaks Work
The system maintains a `DailyActivity` table with a unique constraint on `(user_id, activity_date)`. When activity occurs:
- If activity for today already exists, the streak is unchanged.
- If the most recent activity before today was yesterday, streak increments by 1.
- If the most recent activity was older than yesterday, streak resets to 1.
A dev endpoint (`/api/dev/simulate-activity`) is provided to test consecutive dates without waiting.

### 7. How the Application Scales
- **Database**: Transition SQLite to PostgreSQL or CockroachDB with connection pooling (`pgbouncer`).
- **Caching**: Add Redis caching for frequently accessed learning paths and leaderboard ranks.
- **Authentication**: Integrate JWT tokens or NextAuth / OAuth2 into the FastAPI `get_current_user` dependency.
- **Microservices**: Split the Lesson Evaluation Engine into an isolated, horizontally auto-scaled worker tier.
