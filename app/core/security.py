"""
Security & Authentication Core Primitives.
"""

from typing import Optional
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader
from app.core.config import get_settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


def mask_sensitive_value(value: Optional[str], unmasked_chars: int = 4) -> str:
    """Masks secret tokens while preserving trailing characters for verification."""
    if not value:
        return "<not-set>"
    if len(value) <= unmasked_chars:
        return "******"
    return f"{'*' * (len(value) - unmasked_chars)}{value[-unmasked_chars:]}"


async def verify_internal_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> bool:
    """
    Validates internal service-to-service API key.
    Allows bypassing when DEBUG=True in development environment if desired.
    """
    settings = get_settings()

    # In dev, allow if configured
    if settings.is_development and not api_key:
        return True

    if not api_key or api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return True
