"""
Enterprise Base Schemas.
"""

from typing import Any
from pydantic import BaseModel, Field


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    details: dict[str, Any] = Field(default_factory=dict, description="Contextual validation/error data")
    path: str | None = Field(default=None, description="Request path")


class StandardResponse[DataT](BaseModel):
    """Unified API response wrapper for enterprise consistency."""
    success: bool = Field(default=True, description="Indicates request success status")
    data: DataT | None = Field(default=None, description="Response payload")
    error: ErrorDetail | None = Field(default=None, description="Error block if success is False")


class PaginationMeta(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    total_records: int = Field(default=0, ge=0)
    total_pages: int = Field(default=0, ge=0)


class PaginatedResponse[DataT](BaseModel):
    items: list[DataT] = Field(default_factory=list)
    meta: PaginationMeta

