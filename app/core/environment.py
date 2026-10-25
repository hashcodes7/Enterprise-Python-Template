"""
Environment Switcher & Resolution Module.
==============================================================================
MULTI-AGENT BUSINESS OPERATIONS PLATFORM

HOW TO SWAP VARIABLES BETWEEN DEV AND PROD:
------------------------------------------------------------------------------
Option 1 (Direct File Toggle - Primary):
    Change the `ACTIVE_ENVIRONMENT` constant below to either:
        ACTIVE_ENVIRONMENT = EnvironmentType.DEV
        - or -
        ACTIVE_ENVIRONMENT = EnvironmentType.PROD

Option 2 (System Environment Variable Override):
    Export `APP_ENV=prod` or `APP_ENV=dev` in your shell, container, or CI/CD.
    If APP_ENV is set in the OS environment, it takes precedence over Option 1.
==============================================================================
"""

import os
from enum import Enum
from pathlib import Path


class EnvironmentType(str, Enum):
    """Supported deployment environments."""
    DEV = "dev"
    PROD = "prod"


# ============================================================================
# >>> SWAP ENVIRONMENT HERE <<<
# Change this constant to switch between development and production variables:
# ============================================================================
ACTIVE_ENVIRONMENT: EnvironmentType = EnvironmentType.DEV
# ============================================================================


# Project root path (resolves directory containing .env.dev and .env.prod)
PROJECT_ROOT: Path = Path(__file__).resolve().parent.parent.parent


def get_active_environment() -> EnvironmentType:
    """
    Resolve the current environment type.
    Order of precedence:
    1. System environment variable 'APP_ENV' (if explicitly defined)
    2. The `ACTIVE_ENVIRONMENT` toggle declared in this file
    """
    env_from_os = os.getenv("APP_ENV", "").strip().lower()
    if env_from_os in (EnvironmentType.DEV.value, "development"):
        return EnvironmentType.DEV
    elif env_from_os in (EnvironmentType.PROD.value, "production"):
        return EnvironmentType.PROD

    return ACTIVE_ENVIRONMENT


def get_env_file_path(env: EnvironmentType | None = None) -> Path:
    """
    Get the absolute Path to the corresponding .env file (.env.dev or .env.prod).
    Falls back gracefully if specific file does not exist.
    """
    target_env = env or get_active_environment()

    if target_env == EnvironmentType.PROD:
        target_path = PROJECT_ROOT / ".env.prod"
    else:
        target_path = PROJECT_ROOT / ".env.dev"

    return target_path


def set_active_environment(new_env: EnvironmentType | str) -> None:
    """
    Programmatically swap the active environment in-memory.
    Primarily utilized by test suites or dynamic run launchers.
    """
    global ACTIVE_ENVIRONMENT
    if isinstance(new_env, str):
        new_env = EnvironmentType(new_env.lower())
    ACTIVE_ENVIRONMENT = new_env
    os.environ["APP_ENV"] = new_env.value
