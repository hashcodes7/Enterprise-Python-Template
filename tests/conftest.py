import pytest
from fastapi.testclient import TestClient

from app.api.deps import reset_dependencies_cache
from app.core.config import reload_settings
from app.core.environment import EnvironmentType, set_active_environment
from app.main import create_application


@pytest.fixture(autouse=True)
def reset_to_dev_env():
    """Ensure every test begins with a clean DEV environment."""
    set_active_environment(EnvironmentType.DEV)
    reload_settings()
    reset_dependencies_cache()
    yield
    set_active_environment(EnvironmentType.DEV)
    reload_settings()
    reset_dependencies_cache()


@pytest.fixture
def client() -> TestClient:
    """Create a TestClient instance against the FastAPI app."""
    app = create_application()
    return TestClient(app)

