"""
Authentication & JWT Schemas.
==============================================================================
Pydantic contracts for login requests and JWT token responses.
==============================================================================
"""

from pydantic import BaseModel, Field


class LoginRequest(BaseModel):
    username: str = Field(..., description="User email or login identifier")
    password: str = Field(..., description="Plaintext user password")


class TokenResponse(BaseModel):
    access_token: str = Field(..., description="Signed JWT Bearer token")
    token_type: str = Field(default="bearer", description="Token authentication scheme")
    expires_in: int = Field(..., description="Lifetime in seconds")


class TokenPayload(BaseModel):
    sub: str | None = Field(default=None, description="Subject identifier (User ID)")
    exp: int | None = Field(default=None, description="Expiration UNIX epoch timestamp")
