"""
Integration Tests for FastAPI Endpoints and Runtime Environment Switching.
"""

from fastapi.testclient import TestClient


def test_health_live_endpoint(client: TestClient):
    """Test /api/v1/health/live returns healthy status."""
    response = client.get("/api/v1/health/live")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["status"] == "healthy"
    assert json_data["data"]["environment"] == "dev"
    assert "uptime_seconds" in json_data["data"]


def test_health_ready_endpoint(client: TestClient):
    """Test /api/v1/health/ready returns readiness components."""
    response = client.get("/api/v1/health/ready")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    assert json_data["data"]["ready"] is True
    assert "database" in json_data["data"]["checks"]
    assert "cache" in json_data["data"]["checks"]


def test_system_config_endpoint(client: TestClient):
    """Test /api/v1/system/config returns masked configurations."""
    response = client.get("/api/v1/system/config")
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["success"] is True
    data = json_data["data"]
    assert data["environment"] == "dev"
    assert data["debug"] is True
    assert "database_url_masked" in data
    assert "redis_url_masked" in data
    assert ".env.dev" in data["env_file_source"]


def test_runtime_env_switch_endpoint(client: TestClient):
    """Test dynamic API endpoint to switch environment from dev to prod."""
    # 1. Trigger switch to prod
    switch_res = client.post("/api/v1/system/env-switch", json={"environment": "prod"})
    assert switch_res.status_code == 200
    switch_data = switch_res.json()["data"]
    assert switch_data["active_environment"] == "prod"
    assert ".env.prod" in switch_data["active_env_file"]

    # 2. Check config now reflects PROD variables
    config_res = client.get("/api/v1/system/config")
    assert config_res.status_code == 200
    config_data = config_res.json()["data"]
    assert config_data["environment"] == "prod"
    assert config_data["debug"] is False
    assert "backend_prod" in config_data["database_url_masked"]

    # 3. Switch back to dev
    switch_back_res = client.post("/api/v1/system/env-switch", json={"environment": "dev"})
    assert switch_back_res.status_code == 200
    assert switch_back_res.json()["data"]["active_environment"] == "dev"
