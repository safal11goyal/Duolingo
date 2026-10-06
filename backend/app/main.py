import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base, DATABASE_URL
from .models import *  # Ensure all models are registered
from .routers import auth, path, lessons, gamification, dev

# In local SQLite development, ensure tables exist if migrations were not run
if DATABASE_URL.startswith("sqlite") or os.getenv("AUTO_CREATE_TABLES", "").lower() in ("true", "1"):
    Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Duolingo Clone API",
    description="Full-stack Duolingo-style language learning platform backend backed by Supabase PostgreSQL",
    version="1.0.0"
)

# CORS configuration supporting local dev, deployed frontends, and Render/Vercel
frontend_url = os.getenv("FRONTEND_URL")
allowed_origins = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]
if frontend_url:
    allowed_origins.append(frontend_url.strip())

app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_origin_regex=r"^https?://(localhost|127\.0\.0\.1|.*\.vercel\.app|.*\.onrender\.com)(:\d+)?$",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers under /api (standard frontend prefix) and root aliases
app.include_router(auth.router, prefix="/api")
app.include_router(auth.router)
app.include_router(path.router, prefix="/api")
app.include_router(path.router)
app.include_router(lessons.router)
app.include_router(gamification.router)
app.include_router(dev.router)

@app.get("/")
def root():
    return {
        "name": "Duolingo Clone API",
        "status": "online",
        "database": "postgresql" if not DATABASE_URL.startswith("sqlite") else "sqlite",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "database": "postgresql" if not DATABASE_URL.startswith("sqlite") else "sqlite"
    }
