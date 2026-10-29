"""
Shared FastAPI Route Dependencies.
==============================================================================
Provides reusable dependency injection providers for settings, environment,
database sessions, and domain repositories.
==============================================================================
"""

from typing import Annotated
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import AppSettings, get_settings
from app.core.environment import EnvironmentType, get_active_environment
from app.db.session import get_db
from app.repositories.user_repository import UserRepository


def reset_dependencies_cache() -> None:
    """Clear cached dependency singletons (useful in testing)."""
    get_settings.cache_clear()


# Type Aliases for Route Dependency Injection
type SettingsDep = Annotated[AppSettings, Depends(get_settings)]
type EnvironmentDep = Annotated[EnvironmentType, Depends(get_active_environment)]
type SessionDep = Annotated[AsyncSession, Depends(get_db)]


def get_user_repository(session: SessionDep) -> UserRepository:
    """Dependency provider for UserRepository."""
    return UserRepository(session=session)


type UserRepositoryDep = Annotated[UserRepository, Depends(get_user_repository)]


def get_current_settings() -> AppSettings:
    """Dependency helper to retrieve cached settings instance."""
    return get_settings()


def get_current_environment() -> EnvironmentType:
    """Dependency helper to retrieve current environment."""
    return get_active_environment()
