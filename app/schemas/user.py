"""
User Request & Response Schemas.
==============================================================================
Pydantic v2 schemas for user creation, update, and serialized output.
==============================================================================
"""

from datetime import datetime
from pydantic import BaseModel, ConfigDict, Field

EMAIL_PATTERN = r"^[^@\s]+@[^@\s]+\.[^@\s]+$"


class UserBase(BaseModel):
    email: str = Field(..., pattern=EMAIL_PATTERN, description="Unique user email address")
    full_name: str | None = Field(default=None, description="User full display name")
    is_active: bool = Field(default=True, description="Account active status")


class UserCreate(UserBase):
    password: str = Field(..., min_length=8, description="Raw plaintext password")


class UserUpdate(BaseModel):
    email: str | None = Field(default=None, pattern=EMAIL_PATTERN, description="Updated email address")
    full_name: str | None = Field(default=None, description="Updated full display name")
    password: str | None = Field(default=None, min_length=8, description="Updated password")
    is_active: bool | None = Field(default=None, description="Updated active status")


class UserResponse(UserBase):
    id: str = Field(..., description="Unique user UUID")
    is_superuser: bool = Field(default=False, description="Superuser administrator flag")
    created_at: datetime = Field(..., description="Account creation timestamp")
    updated_at: datetime = Field(..., description="Last account update timestamp")

    model_config = ConfigDict(from_attributes=True)
