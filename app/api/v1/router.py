"""
API v1 Router Aggregator.
"""

from fastapi import APIRouter
from app.api.v1.endpoints import health, system

api_v1_router = APIRouter(prefix="/v1")

# Mount endpoints
api_v1_router.include_router(health.router)
api_v1_router.include_router(system.router)
