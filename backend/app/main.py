from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .models import *  # Ensure all models are registered
from .routers import auth, path, lessons, gamification, dev

# Create tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Duolingo Clone API",
    description="Full-stack Duolingo-style language learning platform backend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(auth.router)
app.include_router(path.router)
app.include_router(lessons.router)
app.include_router(gamification.router)
app.include_router(dev.router)

@app.get("/")
def root():
    return {
        "name": "Duolingo Clone API",
        "status": "online",
        "docs_url": "/docs"
    }

@app.get("/api/health")
def health():
    return {"status": "ok"}
