"""
Database engine, session, and base — shared across all services.

Uses DATABASE_URL from environment (defaults to local PostgreSQL).
For testing, override with SQLite in-memory via get_engine().
"""

import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase


def get_database_url() -> str:
    """Get database URL from environment, with a sensible default."""
    return os.getenv(
        "DATABASE_URL",
        "postgresql://netguard:netguard@localhost:5432/netguard",
    )


def get_engine(url: str | None = None):
    """Create a SQLAlchemy engine. Pass a URL to override (useful for tests)."""
    return create_engine(url or get_database_url())


class Base(DeclarativeBase):
    """Base class for all ORM models."""
    pass


def _create_default_engine():
    """Try to create the default engine; fall back to SQLite if driver missing."""
    try:
        return get_engine()
    except Exception:
        # psycopg2 not installed or DB unreachable — use in-memory SQLite
        return get_engine("sqlite:///:memory:")


# Default session factory (can be overridden in tests)
engine = _create_default_engine()
SessionLocal = sessionmaker(bind=engine)


def get_db():
    """FastAPI dependency that yields a DB session and closes it after."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
