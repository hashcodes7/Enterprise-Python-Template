"""
Unit Tests for Environment Swapping and Variable Resolution.
==============================================================================
Validates that changing the environment cleanly swaps between .env.dev
and .env.prod and retrieves the correct respective configuration parameters.
==============================================================================
"""

from app.core.config import load_settings_for_env, reload_settings
from app.core.environment import (
    EnvironmentType,
    get_active_environment,
    get_env_file_path,
    set_active_environment,
)


def test_dev_environment_variables():
    """Verify loading from .env.dev correctly parses development variables."""
    dev_settings = load_settings_for_env(EnvironmentType.DEV)

    assert dev_settings.APP_ENV == "dev"
    assert "DEV" in dev_settings.APP_NAME
    assert dev_settings.DEBUG is True
    assert dev_settings.LOG_LEVEL == "DEBUG"
    assert dev_settings.HOST == "127.0.0.1"
    assert dev_settings.RELOAD is True
    assert "sqlite" in dev_settings.DATABASE_URL
    assert dev_settings.AGENT_MAX_CONCURRENT_TASKS == 5
    assert dev_settings.AGENT_MOCK_EXTERNAL_APIS is True
    assert dev_settings.ENABLE_AGENT_TELEMETRY is False
    assert dev_settings.is_development is True
    assert dev_settings.is_production is False


def test_prod_environment_variables():
    """Verify loading from .env.prod correctly parses production variables."""
    prod_settings = load_settings_for_env(EnvironmentType.PROD)

    assert prod_settings.APP_ENV == "prod"
    assert "Multi-Agent Business Operations Platform" == prod_settings.APP_NAME
    assert prod_settings.DEBUG is False
    assert prod_settings.LOG_LEVEL == "INFO"
    assert prod_settings.HOST == "0.0.0.0"
    assert prod_settings.RELOAD is False
    assert "postgresql" in prod_settings.DATABASE_URL
    assert prod_settings.AGENT_MAX_CONCURRENT_TASKS == 50
    assert prod_settings.AGENT_MOCK_EXTERNAL_APIS is False
    assert prod_settings.ENABLE_AGENT_TELEMETRY is True
    assert prod_settings.is_development is False
    assert prod_settings.is_production is True


def test_environment_swapping_in_memory():
    """Verify that toggling the active environment switches settings and file sources."""
    # 1. Switch to DEV
    set_active_environment(EnvironmentType.DEV)
    assert get_active_environment() == EnvironmentType.DEV
    assert get_env_file_path().name == ".env.dev"

    dev_settings = reload_settings()
    assert dev_settings.APP_ENV == "dev"
    assert dev_settings.DEBUG is True
    assert dev_settings.AGENT_MAX_CONCURRENT_TASKS == 5

    # 2. Swap to PROD
    set_active_environment(EnvironmentType.PROD)
    assert get_active_environment() == EnvironmentType.PROD
    assert get_env_file_path().name == ".env.prod"

    prod_settings = reload_settings()
    assert prod_settings.APP_ENV == "prod"
    assert prod_settings.DEBUG is False
    assert prod_settings.AGENT_MAX_CONCURRENT_TASKS == 50
    assert "postgresql" in prod_settings.DATABASE_URL
