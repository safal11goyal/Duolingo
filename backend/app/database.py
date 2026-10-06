import os
import logging
from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

logger = logging.getLogger("duolingo.database")

# Load environment variables from .env file if present
load_dotenv()

# Obtain database URL from environment variable
raw_db_url = os.getenv("DATABASE_URL", "").strip()

# Check if URL is provided and valid dialect (PostgreSQL or SQLite)
if not raw_db_url or raw_db_url.startswith("http://") or raw_db_url.startswith("https://"):
    if raw_db_url.startswith("http://") or raw_db_url.startswith("https://"):
        logger.warning(
            "DATABASE_URL is set to an HTTP/HTTPS API URL (%s), but SQLAlchemy requires a PostgreSQL URI. "
            "Falling back to local SQLite. Please update DATABASE_URL with your Supabase PostgreSQL connection string: "
            "postgresql://postgres:[PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres",
            raw_db_url
        )
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_PATH = os.path.join(BASE_DIR, "duolingo.db")
    DATABASE_URL = f"sqlite:///{DB_PATH}"
else:
    DATABASE_URL = raw_db_url

# Normalize URL: SQLAlchemy requires 'postgresql://' instead of legacy 'postgres://'
if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

# Configure engine appropriately based on dialect
if DATABASE_URL.startswith("sqlite"):
    engine = create_engine(
        DATABASE_URL,
        connect_args={"check_same_thread": False}
    )
else:
    # Supabase PostgreSQL configuration with connection health pre-ping
    engine = create_engine(
        DATABASE_URL,
        pool_pre_ping=True,
        pool_size=10,
        max_overflow=20,
    )

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
