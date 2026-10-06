# 🦉 Duolingo Clone — Full-Stack Language Learning Web App

A production-quality full-stack Duolingo clone reproducing the overall visual design, interaction patterns, lesson flow, curved learning path, gamification mechanics, and a **secure user authentication & multi-learner data isolation system**.

---

## 📑 Table of Contents

- [Project Overview](#project-overview)
- [Key Features](#key-features)
- [Authentication & Multi-User Architecture](#authentication--multi-user-architecture)
- [Demo Account Credentials](#demo-account-credentials)
- [User Data Isolation & Relationships](#user-data-isolation--relationships)
- [Security Model](#security-model)
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
- **Full Authentication & Isolated Learner Progress**: Complete user registration, login, logout, password hashing, JWT sessions, protected routes, and isolated user data in SQLite.

---

## 🔐 Authentication & Multi-User Architecture

The authentication system is built cleanly into the FastAPI backend and Next.js frontend with enterprise security standards:

```text
Register / Login
       ↓
Password Hashed with bcrypt (Salt Rounds)
       ↓
User Stored in SQLite (password_hash never exposed)
       ↓
Generate JWT Access Token
       ↓
Session Persisted via HTTP-only Cookie + Authorization Header
       ↓
FastAPI get_current_user Dependency Validates Token
       ↓
Derives User ID from Token Claim ("sub")
       ↓
Completely Isolated User-Specific Progress Returned
```

### 1. Authentication Features
- **Registration (`/register`)**: Account creation with validation (unique username, unique email, minimum password length, password confirmation matching). Newly registered users immediately receive fresh, isolated progression: Skill 1 is available, all remaining skills are locked, 0 XP, 5 hearts, 0 streak.
- **Login (`/login`)**: Secure authentication verifying `bcrypt` hashes. Includes a 1-click **"Fill Demo (Alex)"** quick-fill button for fast evaluation and grading.
- **Logout**: `POST /api/auth/logout` clears HTTP-only cookie and frontend auth context, redirecting users to `/login`.
- **Protected Routes**: `/`, `/learn`, `/profile`, `/settings`, `/leaderboard`, and `/lesson/*` are guarded by `<ProtectedRoute />`. Unauthenticated requests redirect to `/login`.
- **Persistent Sessions**: Browser refreshes retain authentication seamlessly via `GET /api/auth/me`. The user is never kicked back to login simply because of a page reload.

---

## 👤 Demo Account Credentials

A fully seeded demo learner account is pre-configured and ready to use:

| Field | Value |
| :--- | :--- |
| **Email** | `demo@example.com` |
| **Password** | `Demo123!` |
| **Username** | `alex` |
| **Display Name** | `Alex Rivera` |

*Note: The demo account behaves exactly like a standard user account and is not special-cased in application logic.*

---

## 🛡️ User Data Isolation & Relationships

Every learner's progress is strictly partitioned in SQLite. A user never sees, modifies, or accesses another user's progress:

```text
User
 │
 ├── UserSkillProgress [UNIQUE(user_id, skill_id)]
 │      └── Skill
 │
 ├── LessonAttempt [user_id == current_user.id enforced]
 │      └── Lesson
 │
 ├── DailyActivity [UNIQUE(user_id, activity_date)]
 │
 └── UserAchievement
        └── Achievement
```

### Multi-User Demonstration
- **User A (Alex / Demo)**: 150 XP, 3 Day Streak, Greetings completed, Food available.
- **User B (Brand New)**: 0 XP, 0 Day Streak, Greetings available, Food locked.
- **User B cannot tamper with User A**: Submitting answers or completions referencing another user's `attempt_id` returns `403 Forbidden`.

---

## 🔒 Security Model

### Zero Client Trust
The backend never trusts or accepts learner metrics from frontend request payloads:
- **No `user_id` in request bodies**: The backend derives the authenticated user strictly from the verified JWT claims (`get_current_user()`).
- **No client-supplied `xp`**: XP is calculated and awarded exclusively by the backend Lesson Service.
- **No client-supplied `hearts`**: Heart deductions and regenerations are enforced exclusively on the backend.
- **No client-supplied `correct: true`**: All exercise validations (multiple choice, word bank, translate, match pairs, fill blank, type answer) execute against backend truth.
- **Locked lesson protection**: Manipulating lesson URLs to access locked skills directly returns `403 Forbidden`.

---

## 🛠️ Tech Stack

- **Frontend**:
  - **Framework**: Next.js 16 (App Router)
  - **Language**: TypeScript
  - **Styling**: Tailwind CSS with custom 3D button utilities
  - **Icons & Effects**: `lucide-react`, `canvas-confetti`
  - **Audio**: Web Audio API synthesizer + Web Speech API (zero external sound file dependencies)
- **Backend**:
  - **Framework**: FastAPI (Python 3.10+)
  - **Security**: `pyjwt`, `bcrypt`, `email-validator`
  - **ORM**: SQLAlchemy 2.0
  - **Validation**: Pydantic v2
  - **Database**: SQLite (`duolingo.db`)
  - **Testing**: `pytest`, `httpx`

---

## 🏛️ System Architecture

```text
       ┌───────────────────────────────┐
       │     Next.js Frontend (React)   │
       │   - AuthContext & useAuth()   │
       │   - ProtectedRoute Guards     │
       │   - Duolingo 3D UI & Player   │
       └──────────────┬────────────────┘
                      │ Bearer Token / Cookie
                      ▼
       ┌───────────────────────────────┐
       │     FastAPI Authentication    │
       │   - /api/auth/register        │
       │   - /api/auth/login, /me      │
       │   - get_current_user (JWT)    │
       └──────────────┬────────────────┘
                      │ Current User Injected
                      ▼
       ┌───────────────────────────────┐
       │         Service Layer         │
       │   - lesson_service.py         │
       │   - progress_service.py       │
       │   - streak_service.py         │
       │   - user_service.py           │
       └──────────────┬────────────────┘
                      │ SQLAlchemy ORM
                      ▼
       ┌───────────────────────────────┐
       │       SQLite Database         │
       │   - duolingo.db (Isolated)    │
       └───────────────────────────────┘
```

---

## 📁 Folder Structure

```text
Duolingo/
├── backend/
│   ├── app/
│   │   ├── auth/                   # Authentication module
│   │   │   ├── security.py         # bcrypt hashing & JWT generation/decoding
│   │   │   ├── dependencies.py     # get_current_user dependency
│   │   │   └── service.py          # register_user, authenticate_user
│   │   ├── database.py             # SQLite engine & session management
│   │   ├── main.py                 # FastAPI application & CORS
│   │   ├── seed.py                 # Seed script with demo account & course
│   │   ├── models/                 # SQLAlchemy ORM models
│   │   │   ├── user.py             # User with email, password_hash
│   │   │   ├── course.py           # Course, Unit, Skill, Lesson, Exercise
│   │   │   ├── progress.py         # UserSkillProgress, LessonAttempt
│   │   │   └── gamification.py     # DailyActivity, Achievement, UserAchievement
│   │   ├── schemas/                # Pydantic v2 schemas
│   │   │   ├── user.py             # UserRegister, UserLogin, UserResponse
│   │   │   ├── course.py
│   │   │   ├── lesson.py
│   │   │   └── gamification.py
│   │   ├── services/               # Core business logic services
│   │   │   ├── user_service.py
│   │   │   ├── progress_service.py
│   │   │   ├── lesson_service.py
│   │   │   └── streak_service.py
│   │   └── routers/                # REST API routers
│   │       ├── auth.py             # /api/auth/register, login, me, logout
│   │       ├── path.py             # /api/path, /api/progress
│   │       ├── lessons.py          # /api/lessons/{id}/...
│   │       ├── gamification.py     # /api/leaderboard, achievements, hearts
│   │       └── dev.py              # Streak simulation & progress reset
│   ├── tests/
│   │   ├── test_auth_and_isolation.py  # User registration, JWT, and multi-user isolation tests
│   │   └── test_services.py            # Answer validation, hearts, streak tests
│   ├── requirements.txt
│   └── pytest.ini
│
├── frontend/
│   ├── src/
│   │   ├── app/
│   │   │   ├── layout.tsx          # Wrapped in AuthProvider
│   │   │   ├── page.tsx            # Redirects to /learn or /login
│   │   │   ├── login/page.tsx      # Duolingo 3D Login Page with demo quick-fill
│   │   │   ├── register/page.tsx   # Duolingo 3D Registration Page
│   │   │   ├── learn/page.tsx      # Protected learning path
│   │   │   ├── lesson/[lessonId]/  # Protected lesson player
│   │   │   ├── leaderboard/        # Protected leaderboard
│   │   │   ├── profile/            # Protected profile & stats
│   │   │   └── settings/           # Protected settings & account logout
│   │   ├── context/
│   │   │   └── AuthContext.tsx     # React authentication context
│   │   ├── hooks/
│   │   │   └── useAuth.ts          # useAuth hook
│   │   ├── components/
│   │   │   ├── auth/               # ProtectedRoute wrapper
│   │   │   ├── layout/             # Sidebar with user pill & logout, TopHeader with avatar dropdown
│   │   │   ├── path/               # UnitHeader, SkillNode, PathRightSidebar
│   │   │   └── lesson/             # Exercise components, FeedbackBar, Modals
│   │   └── lib/
│   │       ├── api.ts              # Typed REST client with automatic Bearer tokens & cookies
│   │       ├── types.ts            # TypeScript interfaces
│   │       └── sound.ts            # Web Audio API synthesizers
│   └── package.json
│
└── README.md
```

---

## 📊 Database Schema & ER Diagram

```text
+-------------------------+             +-------------------+             +--------------------+
|          User           |             |      Course       |             |        Unit        |
+-------------------------+             +-------------------+             +--------------------+
| id (PK)                 |             | id (PK)           | 1         * | id (PK)            |
| username (UNIQUE)       |             | name              |-------------| course_id (FK)     |
| email (UNIQUE)          |             | source_language   |             | title              |
| password_hash           |             | target_language   |             | description        |
| display_name            |             +-------------------+             | order_index        |
| avatar                  |                                               +--------------------+
| xp                      |                                                         | 1
| gems                    |                                                         | *
| hearts                  |                                               +--------------------+
| streak                  |                                               |       Skill        |
| daily_goal              |                                               +--------------------+
| last_active_at          |                                               | id (PK)            |
| created_at, updated_at  |                                               | unit_id (FK)       |
+-------------------------+                                               | title              |
   | 1         | 1                                                        | description        |
   |           |                                                          | order_index        |
   | *         | *                                                        | xp_reward          |
+-------------------------+   +-------------------------+                 +--------------------+
|    UserSkillProgress    |   |      LessonAttempt      |                           | 1
| UNIQUE(user_id,skill_id)|   +-------------------------+                           | *
+-------------------------+   | id (PK)                 |                 +--------------------+
| id (PK)                 |   | user_id (FK)            |                 |       Lesson       |
| user_id (FK)            |   | lesson_id (FK)          |                 +--------------------+
| skill_id (FK)           |   | started_at              |                 | id (PK)            |
| status                  |   | completed_at            |                 | skill_id (FK)      |
| xp                      |   | correct_answers         |                 | title              |
| crown_level             |   | wrong_answers           |                 | order_index        |
| completed_lessons       |   | xp_earned               |                 | xp_reward          |
+-------------------------+   | completed               |                 +--------------------+
                              +-------------------------+                           | 1
                                                                                    | *
+-------------------------+   +-------------------------+                 +--------------------+
|      DailyActivity      |   |       Achievement       |                 |      Exercise      |
| UNIQUE(user_id,date)    |   +-------------------------+                 +--------------------+
+-------------------------+   | id (PK)                 | 1             * | id (PK)            |
| id (PK)                 |   | name                    |-----------------| lesson_id (FK)     |
| user_id (FK)            |   | requirement_type        |                 | type               |
| activity_date           |   | requirement_value       |                 | question           |
| xp_earned               |   +-------------------------+                 | correct_answer     |
| lessons_completed       |                | 1                            | xp                 |
+-------------------------+                | *                            +--------------------+
                              +-------------------------+                           | 1
                              |     UserAchievement     |                           | *
                              +-------------------------+                 +--------------------+
                              | user_id (FK)            |                 |   ExerciseOption   |
                              | achievement_id (FK)     |                 +--------------------+
                              | unlocked_at             |                 | id (PK)            |
                              +-------------------------+                 | exercise_id (FK)   |
                                                                          | text               |
                                                                          | is_correct         |
                                                                          +--------------------+
```

---

## 🔌 API Reference

### Authentication Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/api/auth/register` | Register new user, hash password, initialize fresh skill progression, return JWT |
| `POST` | `/api/auth/login` | Authenticate email/password, return JWT and set HTTP-only cookie |
| `GET` | `/api/auth/me` | Fetch authenticated user data from token (no passwords exposed) |
| `POST` | `/api/auth/logout` | Clear session cookie and invalidate client state |

### User & Learning Path Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/me` | Safe authenticated user profile summary |
| `GET` | `/api/profile` | Detailed stats, crowns, streak, league, achievements |
| `GET` | `/api/path` | Authenticated user's learning path with current unlocked/completed statuses |
| `GET` | `/api/progress` | User's skill progress list |
| `GET` | `/api/lessons/{id}` | Lesson detail (validates skill unlocked & user has hearts; answers hidden) |
| `POST` | `/api/lessons/{id}/start` | Initialize lesson attempt belonging to current user |
| `POST` | `/api/lessons/{id}/answer` | Validate answer, deduct hearts, award exercise XP on attempt |
| `POST` | `/api/lessons/{id}/complete` | Finalize attempt, award completion XP, update streak and unlock next skill |
| `GET` | `/api/leaderboard` | Ranked user standings and league brackets |
| `GET` | `/api/achievements` | Achievements list with authenticated user's unlock statuses |
| `POST` | `/api/hearts/refill` | Instantly restores hearts to full 5 |
| `POST` | `/api/hearts/practice` | Earns +1 heart via practice session |
| `POST` | `/api/dev/simulate-activity`| Simulate learning on specific date for streak verification |
| `POST` | `/api/dev/reset-progress` | Resets current user's progress for fresh testing |

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

# Seed the database (creates demo@example.com account and Spanish course)
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

The backend test suite covers:
1. **User Authentication & Data Isolation (`test_auth_and_isolation.py`)**:
   - Rejection of unauthenticated requests (`401 Unauthorized`)
   - User registration and login flow with password hashing and JWT token issuance
   - Verification that User A's XP, hearts, streak, and skill completions are 100% isolated from User B
   - Verification that User B cannot answer or complete User A's lesson attempt (`403 Forbidden`)
   - Verification that User B cannot access locked lessons by manipulating URLs (`403 Forbidden`)
2. **Core Services (`test_services.py`)**:
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
SQLite provides a zero-setup, serverless, self-contained SQL database stored in a single file (`duolingo.db`). It eliminates external database dependencies for evaluators while providing full ACID compliance, unique constraints, and foreign key relations.

### 2. Why SQLAlchemy?
SQLAlchemy 2.0 provides an enterprise ORM with strong relationship mapping, typed queries, and clear separation of database schemas. It allows seamless migration to PostgreSQL or MySQL simply by changing the connection string without rewriting business logic.

### 3. Why JWT & HTTP-Only Cookies?
The application implements hybrid token delivery:
- An **HTTP-only cookie** protects against XSS attacks in browser environments.
- A **Bearer Authorization header** is supported for standard REST clients and headless tests.
- Tokens encode `{"sub": "<user_id>", "exp": ...}` so the server validates authenticity without extra session lookups.

### 4. How Cross-User Tampering is Prevented
Every `LessonAttempt` row stores `user_id`. When submitting an exercise answer or finishing a lesson, the backend checks:
```python
if attempt.user_id != user.id:
    raise HTTPException(status_code=403, detail="Forbidden: You cannot modify another user's lesson attempt.")
```
Users cannot forge or hijack other users' in-progress lessons.
