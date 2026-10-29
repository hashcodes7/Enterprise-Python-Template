"""
Security, Cryptography & Authentication Primitives.
==============================================================================
Provides password hashing via bcrypt, signed JWT token generation/validation,
and internal API key verification.
==============================================================================
"""

from datetime import datetime, timedelta, timezone
from typing import Any
import bcrypt
import jwt
from fastapi import HTTPException, Security, status
from fastapi.security import APIKeyHeader, OAuth2PasswordBearer

from app.core.config import get_settings

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)
OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="/api/v1/auth/login", auto_error=False)


def get_password_hash(password: str) -> str:
    """Hash plaintext password using direct bcrypt with salt."""
    salt = bcrypt.gensalt()
    return bcrypt.hashpw(password.encode("utf-8"), salt).decode("utf-8")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify plaintext password against stored bcrypt hash."""
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"), hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def create_access_token(
    subject: str,
    expires_delta: timedelta | None = None,
    extra_claims: dict[str, Any] | None = None,
) -> str:
    """Generate a signed cryptographic JWT access token."""
    settings = get_settings()
    now = datetime.now(timezone.utc)
    if expires_delta:
        expire = now + expires_delta
    else:
        expire = now + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)

    payload: dict[str, Any] = {
        "sub": str(subject),
        "iat": now,
        "exp": expire,
    }
    if extra_claims:
        payload.update(extra_claims)

    encoded_jwt = jwt.encode(
        payload,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM,
    )
    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any]:
    """Decode and cryptographically verify a JWT access token."""
    settings = get_settings()
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM],
        )
        return payload
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Access token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )


def mask_sensitive_value(value: str | None, unmasked_chars: int = 4) -> str:
    """Mask secret tokens while preserving trailing characters for verification."""
    if not value:
        return "<not-set>"
    if len(value) <= unmasked_chars:
        return "******"
    return f"{'*' * (len(value) - unmasked_chars)}{value[-unmasked_chars:]}"


async def verify_internal_api_key(api_key: str | None = Security(API_KEY_HEADER)) -> bool:
    """Validates internal service-to-service API key."""
    settings = get_settings()
    if settings.is_development and not api_key:
        return True

    if not api_key or api_key != settings.SECRET_KEY:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or missing X-API-Key header",
        )
    return True
