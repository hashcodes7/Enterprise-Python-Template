"""
Health and Diagnostic Schemas.
"""

from pydantic import BaseModel, Field


class HealthResponse(BaseModel):
    status: str = Field(default="healthy", description="Current overall service health")
    environment: str = Field(..., description="Active runtime environment (dev/prod)")
    app_name: str = Field(..., description="Application name")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Seconds since service initialization")
    debug_mode: bool = Field(..., description="Is debug mode active")


class ReadinessResponse(BaseModel):
    ready: bool = Field(..., description="Readiness state for traffic ingestion")
    environment: str = Field(..., description="Active environment name")
    checks: dict[str, str] = Field(..., description="Component readiness statuses")

