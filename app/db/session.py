"""
Database Session & Connection Management.
==============================================================================
Provides production-grade async SQLAlchemy 2.0 session factory, connection
pooling, health pings, and FastAPI dependency lifecycle management.
==============================================================================
"""

import logging
from collections.abc import AsyncIterator
from sqlalchemy.ext.asyncio import (
    AsyncEngine,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy import text

from app.core.config import get_settings
from app.db.base import Base

logger = logging.getLogger("app.db")

_engine: AsyncEngine | None = None
_session_factory: async_sessionmaker[AsyncSession] | None = None


def get_engine() -> AsyncEngine:
    """Lazy initialize and return singleton AsyncEngine."""
    global _engine
    if _engine is None:
        settings = get_settings()
        connect_args = {}
        if "sqlite" in settings.DATABASE_URL:
            connect_args["check_same_thread"] = False

        _engine = create_async_engine(
            settings.DATABASE_URL,
            echo=settings.DB_ECHO,
            future=True,
            connect_args=connect_args,
        )
    return _engine


def get_session_factory() -> async_sessionmaker[AsyncSession]:
    """Lazy initialize and return singleton async_sessionmaker."""
    global _session_factory
    if _session_factory is None:
        engine = get_engine()
        _session_factory = async_sessionmaker(
            bind=engine,
            class_=AsyncSession,
            autoflush=False,
            autocommit=False,
            expire_on_commit=False,
        )
    return _session_factory


async def init_db() -> None:
    """Create database tables if they do not exist (useful for dev / tests)."""
    engine = get_engine()
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    logger.info("Database schema verified and initialized.")


async def close_db() -> None:
    """Dispose of engine connection pool on application shutdown."""
    global _engine, _session_factory
    if _engine is not None:
        await _engine.dispose()
        _engine = None
        _session_factory = None
        logger.info("Database connection pool gracefully closed.")


async def ping_db() -> bool:
    """Perform a lightweight SELECT 1 check to verify database connectivity."""
    try:
        session_factory = get_session_factory()
        async with session_factory() as session:
            await session.execute(text("SELECT 1"))
        return True
    except Exception as exc:
        logger.warning(f"Database ping check failed: {exc}")
        return False


async def get_db() -> AsyncIterator[AsyncSession]:
    """FastAPI route dependency yielding an async database session."""
    session_factory = get_session_factory()
    async with session_factory() as session:
        try:
            yield session
            await session.commit()
        except Exception:
            await session.rollback()
            raise
        finally:
            await session.close()
