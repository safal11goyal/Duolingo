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

---

## 🔌 API Reference

### Core & Migration Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `POST` | `/register` or `/api/auth/register` | Register new user, hash password, initialize fresh skill progression, return JWT |
| `POST` | `/login` or `/api/auth/login` | Authenticate email/password, return JWT and set HTTP-only cookie |
| `POST` | `/logout` or `/api/auth/logout` | Clear session cookie and invalidate client state |
| `GET` | `/me` or `/api/auth/me` | Safe authenticated user profile (password hash never exposed) |
| `GET` | `/courses` or `/api/courses` | List all available language courses |
| `GET` | `/lessons` or `/api/lessons` | List all lessons with order, XP reward, and exercise counts |
| `GET` | `/questions` or `/api/questions` | List questions/exercises with options (optional `?lesson_id=...` filter) |
| `GET` | `/progress` or `/api/progress` | Authenticated user's overall progress (XP, streak, lesson attempts, skills) |
| `GET` | `/answers` or `/api/answers` | Authenticated user's answer submission history |

### User & Learning Path Endpoints

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| `GET` | `/api/profile` | Detailed stats, crowns, streak, league, achievements |
| `GET` | `/api/path` | Authenticated user's learning path with current unlocked/completed statuses |
| `GET` | `/api/lessons/{id}` | Lesson detail (validates skill unlocked & user has hearts; answers hidden) |
| `POST` | `/api/lessons/{id}/start` | Initialize lesson attempt belonging to current user (increments attempts) |
| `POST` | `/api/lessons/{id}/answer` | Validate answer, deduct hearts, record `UserAnswer`, award exercise XP |
| `POST` | `/api/lessons/{id}/complete` | Finalize attempt, award completion XP, update streak and unlock next skill |
| `GET` | `/api/leaderboard` | Ranked user standings and league brackets |
| `GET` | `/api/achievements` | Achievements list with authenticated user's unlock statuses |
| `POST` | `/api/hearts/refill` | Instantly restores hearts to full 5 |
| `POST` | `/api/hearts/practice` | Earns +1 heart via practice session |
| `POST` | `/api/dev/simulate-activity`| Simulate learning on specific date for streak verification |
| `POST` | `/api/dev/reset-progress` | Resets current user's progress for fresh testing |

---

## 🗄️ Database Architecture & Migrations

The application uses **Supabase PostgreSQL** as its production database and **SQLAlchemy** as the ORM, with schema management powered by **Alembic**.

### 1. Supabase PostgreSQL Configuration

1. Log in to [Supabase](https://supabase.com) and create a new project (e.g. `duolingo-clone`).
2. Go to **Project Settings** -> **Database** -> **Connection string**.
3. Copy the **URI** (or **Transaction Pooler** URI for serverless/pooled environments):
   ```text
   postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   ```
4. Put this connection string in your `.env` file:
   ```env
   DATABASE_URL=postgresql://postgres:[YOUR-PASSWORD]@db.[YOUR-PROJECT-REF].supabase.co:5432/postgres
   SECRET_KEY=your_jwt_secret_key_here
   ```
5. *(Fallback behavior)*: If `DATABASE_URL` is omitted, the application automatically falls back to local SQLite (`sqlite:///./duolingo.db`) for offline development or automated CI testing.

### 2. Alembic Database Migrations

Database tables are managed with versioned migrations:
```bash
cd backend

# Apply migrations to the database configured in DATABASE_URL
alembic upgrade head

# Check current revision status
alembic current
```

The initial migration `0001_initial_schema` creates all 13 required tables:
- `users`
- `courses`
- `units`
- `skills`
- `lessons`
- `exercises`
- `exercise_options`
- `user_skill_progress`
- `lesson_attempts`
- `user_answers`
- `daily_activities`
- `achievements`
- `user_achievements`

### 3. Idempotent Database Seeding

To populate the database with courses, lessons, exercises, options, and achievements:
```bash
cd backend
python -m app.seed
```
The seed script is **fully idempotent**: it can be run multiple times safely without creating duplicate courses, lessons, or exercises.

---

## 🚀 Local Setup Instructions

Follow these step-by-step instructions to run locally with Supabase PostgreSQL:

```bash
# 1. Clone the repository
git clone https://github.com/safal11goyal/Duolingo.git
cd Duolingo

# 2. Configure environment variables
# Copy .env.example to .env
cp .env.example .env
# Edit .env and supply your Supabase connection string and SECRET_KEY:
# DATABASE_URL=postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres
# SECRET_KEY=generate_a_random_32_char_secret_key

# 3. Setup Backend
cd backend
python -m venv venv
# On Windows:
.\venv\Scripts\activate
# On macOS/Linux:
# source venv/bin/activate

pip install -r requirements.txt

# 4. Run Alembic migrations against Supabase
alembic upgrade head

# 5. Seed initial course curriculum & achievements
python -m app.seed

# 6. Start FastAPI server
uvicorn app.main:app --port 8000 --reload

# 7. Start Next.js Frontend (in a separate terminal)
cd ../frontend
npm install
npm run dev
```

Visit:
- **Frontend App**: `http://localhost:3000`
- **FastAPI Interactive Docs**: `http://localhost:8000/docs`

---

## 🌐 Production Deployment Guide (Render)

Deploying the FastAPI backend to [Render](https://render.com):

### 1. Create a Web Service on Render
1. Connect your GitHub repository `https://github.com/safal11goyal/Duolingo`.
2. Configure service settings:
   - **Environment**: `Python 3`
   - **Root Directory**: `backend`
   - **Build Command**:
     ```bash
     pip install -r requirements.txt && alembic upgrade head && python -m app.seed
     ```
   - **Start Command**:
     ```bash
     uvicorn app.main:app --host 0.0.0.0 --port $PORT
     ```

### 2. Environment Variables on Render
Add the following in Render's **Environment** tab:
- `DATABASE_URL`: Your Supabase PostgreSQL connection string (Transaction Pooler or direct URI).
- `SECRET_KEY`: A secure 32+ character random string for signing JWT tokens.
- `FRONTEND_URL`: The URL of your deployed frontend (e.g. `https://duolingo-frontend.vercel.app`).
- `PYTHON_VERSION`: `3.11.0` or higher.

---

## 🧪 Automated Testing

The backend test suite covers:
1. **User Authentication & Data Isolation (`test_auth_and_isolation.py`)**:
   - Rejection of unauthenticated requests (`401 Unauthorized`)
   - User registration and login flow with password hashing and JWT token issuance
   - Verification that User A's XP, hearts, streak, and skill completions are 100% isolated from User B
   - Cross-user attempt tampering protection (`403 Forbidden`)
2. **PostgreSQL Migration Endpoints (`test_postgres_migration.py`)**:
   - Registration, login, and `/me` profile retrieval
   - `/courses`, `/lessons`, `/questions` listing with options
   - `/progress` returns attempts, XP, and streak
   - `/answers` tracks user-submitted answers and correctness
3. **Core Services (`test_services.py`)**:
   - Answer normalization & validation
   - Heart deduction and non-negative boundaries
   - Streak calculation across calendar days

Run all tests:
```bash
cd backend
.\venv\Scripts\pytest -v
```

