"""Database configuration and session management."""

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker


def _build_database_url() -> str:
    """Build a PostgreSQL SQLAlchemy URL from environment variables.

    Priority:
    1) DATABASE_URL if provided (takes precedence)
    2) Compose from DB_* variables
    """

    explicit_url = os.getenv("DATABASE_URL")
    if explicit_url:
        return explicit_url

    db_user = os.getenv("DB_USER", "postgres")
    db_password = os.getenv("DB_PASSWORD", "postgres")
    db_host = os.getenv("DB_HOST", "170.78.97.36")
    db_port = os.getenv("DB_PORT", "5400")
    db_name = os.getenv("DB_NAME", "checkin")

    return f"postgresql+psycopg2://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"


DATABASE_URL = _build_database_url()

# Create engine and session factory
engine = create_engine(
    DATABASE_URL,
    pool_pre_ping=True,
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()


def get_db():
    """Provide a transactional scope around a series of operations."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()