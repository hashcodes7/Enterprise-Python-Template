"""
Schemas Package Initialization.
==============================================================================
Exports API data transfer objects, request/response models, and standardized
response envelopes.
==============================================================================
"""

from app.schemas.auth import LoginRequest, TokenPayload, TokenResponse
from app.schemas.base import ErrorDetail, PaginatedResponse, PaginationMeta, StandardResponse
from app.schemas.health import HealthResponse, ReadinessResponse
from app.schemas.system import EnvSwitchRequest, EnvSwitchResponse, SystemConfigResponse
from app.schemas.user import UserBase, UserCreate, UserResponse, UserUpdate

__all__ = [
    # Base Envelopes
    "StandardResponse",
    "ErrorDetail",
    "PaginatedResponse",
    "PaginationMeta",
    # Health & System
    "HealthResponse",
    "ReadinessResponse",
    "SystemConfigResponse",
    "EnvSwitchRequest",
    "EnvSwitchResponse",
    # Auth & User
    "LoginRequest",
    "TokenResponse",
    "TokenPayload",
    "UserBase",
    "UserCreate",
    "UserUpdate",
    "UserResponse",
]
