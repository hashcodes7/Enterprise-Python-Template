"""
Shared FastAPI Route Dependencies.
"""

from typing import Annotated
from fastapi import Depends
from app.core.config import AppSettings, get_settings
from app.core.environment import EnvironmentType, get_active_environment

SettingsDep = Annotated[AppSettings, Depends(get_settings)]
EnvironmentDep = Annotated[EnvironmentType, Depends(get_active_environment)]


def get_current_settings() -> AppSettings:
    """Dependency helper to retrieve cached settings instance."""
    return get_settings()


def get_current_environment() -> EnvironmentType:
    """Dependency helper to retrieve current environment."""
    return get_active_environment()
