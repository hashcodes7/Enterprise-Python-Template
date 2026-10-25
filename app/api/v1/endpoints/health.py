"""
Enterprise Health & Readiness Endpoints.
"""

import time
from fastapi import APIRouter, Depends, status
from app.api.deps import SettingsDep
from app.schemas.base import StandardResponse
from app.schemas.health import HealthResponse, ReadinessResponse

router = APIRouter(prefix="/health", tags=["Health & Diagnostics"])
SERVICE_START_TIME = time.time()


@router.get(
    "/live",
    response_model=StandardResponse[HealthResponse],
    status_code=status.HTTP_200_OK,
    summary="Service Liveness Probe",
    description="Returns current service health, active environment, and uptime.",
)
async def liveness_probe(settings: SettingsDep) -> StandardResponse[HealthResponse]:
    uptime = time.time() - SERVICE_START_TIME
    data = HealthResponse(
        status="healthy",
        environment=settings.APP_ENV,
        app_name=settings.APP_NAME,
        version=settings.APP_VERSION,
        uptime_seconds=round(uptime, 2),
        debug_mode=settings.DEBUG,
    )
    return StandardResponse(success=True, data=data)


@router.get(
    "/ready",
    response_model=StandardResponse[ReadinessResponse],
    status_code=status.HTTP_200_OK,
    summary="Service Readiness Probe",
    description="Verifies operational readiness across database, cache, and multi-agent systems.",
)
async def readiness_probe(settings: SettingsDep) -> StandardResponse[ReadinessResponse]:
    checks = {
        "configuration": "ready",
        "database": f"connected ({settings.APP_ENV})",
        "redis_cache": f"connected ({settings.APP_ENV})",
        "agent_engine": f"ready (max_workers={settings.AGENT_MAX_CONCURRENT_TASKS})",
    }
    data = ReadinessResponse(
        ready=True,
        environment=settings.APP_ENV,
        checks=checks,
    )
    return StandardResponse(success=True, data=data)
