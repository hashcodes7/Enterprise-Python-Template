"""
Schemas Package Initialization.
"""

from app.schemas.base import StandardResponse, ErrorDetail, PaginatedResponse, PaginationMeta
from app.schemas.health import HealthResponse, ReadinessResponse
from app.schemas.system import SystemConfigResponse, EnvSwitchRequest, EnvSwitchResponse

__all__ = [
    "StandardResponse",
    "ErrorDetail",
    "PaginatedResponse",
    "PaginationMeta",
    "HealthResponse",
    "ReadinessResponse",
    "SystemConfigResponse",
    "EnvSwitchRequest",
    "EnvSwitchResponse",
]
