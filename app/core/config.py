"""
Enterprise Configuration Management Module.
==============================================================================
Loads settings via Pydantic Settings dynamically from either `.env.dev`
or `.env.prod`, as determined by `app.core.environment`.
==============================================================================
"""

import json
from functools import lru_cache
from typing import Any
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.environment import (
    EnvironmentType,
    get_active_environment,
    get_env_file_path,
)


class AppSettings(BaseSettings):
    """
    Enterprise Application Settings Schema.
    Strictly validated with typed attributes and default fallbacks.
    """

    # -------------------------------------------------------------------------
    # Core Application Attributes
    # -------------------------------------------------------------------------
    APP_ENV: str = Field(default=EnvironmentType.DEV.value, description="Active environment name (dev/prod)")
    APP_NAME: str = Field(default="Enterprise FastAPI Backend", description="Application Title")
    APP_VERSION: str = Field(default="1.0.0", description="Semantic service version")
    DEBUG: bool = Field(default=False, description="Debug mode toggle")
    LOG_LEVEL: str = Field(default="INFO", description="Standard logging level")
    HOST: str = Field(default="127.0.0.1", description="Binding host IP")
    PORT: int = Field(default=8000, description="Listening TCP port")
    RELOAD: bool = Field(default=False, description="Auto-reload on code change")

    # -------------------------------------------------------------------------
    # Security, Auth & CORS
    # -------------------------------------------------------------------------
    SECRET_KEY: str = Field(..., description="Cryptographic secret key for signing")
    ALGORITHM: str = Field(default="HS256", description="JWT signing algorithm")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=60, description="JWT lifetime in minutes")
    CORS_ORIGINS: list[str] = Field(default=["*"], description="Allowed CORS origin domains")

    @field_validator("CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Any) -> list[str]:
        if isinstance(v, str):
            try:
                parsed = json.loads(v)
                if isinstance(parsed, list):
                    return [str(item) for item in parsed]
            except Exception:
                return [origin.strip() for origin in v.split(",") if origin.strip()]
        elif isinstance(v, (list, tuple)):
            return [str(item) for item in v]
        return ["*"]

    # -------------------------------------------------------------------------
    # Storage & Cache
    # -------------------------------------------------------------------------
    DATABASE_URL: str = Field(..., description="Asynchronous database connection URI")
    DB_ECHO: bool = Field(default=False, description="Enable SQLAlchemy engine SQL echoing")
    REDIS_URL: str = Field(default="redis://127.0.0.1:6379/0", description="Redis connection URI")


    # -------------------------------------------------------------------------
    # Helper Properties
    # -------------------------------------------------------------------------
    @property
    def is_development(self) -> bool:
        return self.APP_ENV.lower() in (EnvironmentType.DEV.value, "development")

    @property
    def is_production(self) -> bool:
        return self.APP_ENV.lower() in (EnvironmentType.PROD.value, "production")

    def get_masked_secret(self, secret: str, visible_suffix_len: int = 4) -> str:
        """Utility to safely mask sensitive tokens for diagnostics/logs."""
        if not secret or len(secret) <= visible_suffix_len:
            return "******"
        return f"{'*' * (len(secret) - visible_suffix_len)}{secret[-visible_suffix_len:]}"

    # Pydantic Settings Configuration
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
    )


def load_settings_for_env(env: EnvironmentType | None = None) -> AppSettings:
    """
    Factory function to instantiate AppSettings pointing explicitly
    to the target environment file (.env.dev or .env.prod).
    """
    target_env = env or get_active_environment()
    env_file = get_env_file_path(target_env)

    return AppSettings(
        _env_file=str(env_file),
        _env_file_encoding="utf-8",
        APP_ENV=target_env.value,
    )



@lru_cache()
def get_settings() -> AppSettings:
    """
    Cached settings provider for dependency injection across FastAPI endpoints.
    Uses the active environment defined in `app.core.environment`.
    """
    return load_settings_for_env()


def reload_settings() -> AppSettings:
    """
    Clear the cached settings instance and re-read configuration.
    Useful after swapping environments dynamically or updating .env files.
    """
    get_settings.cache_clear()
    return get_settings()
