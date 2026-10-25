"""
Enterprise Base Schemas.
"""

from typing import Any, Generic, List, Optional, TypeVar
from pydantic import BaseModel, Field

DataT = TypeVar("DataT")


class ErrorDetail(BaseModel):
    code: str = Field(..., description="Machine-readable error code")
    message: str = Field(..., description="Human-readable error description")
    details: Optional[dict[str, Any]] = Field(default_factory=dict, description="Contextual validation/error data")
    path: Optional[str] = Field(default=None, description="Request path")


class StandardResponse(BaseModel, Generic[DataT]):
    """Unified API response wrapper for enterprise consistency."""
    success: bool = Field(default=True, description="Indicates request success status")
    data: Optional[DataT] = Field(default=None, description="Response payload")
    error: Optional[ErrorDetail] = Field(default=None, description="Error block if success is False")


class PaginationMeta(BaseModel):
    page: int = Field(default=1, ge=1)
    page_size: int = Field(default=20, ge=1, le=100)
    total_records: int = Field(default=0, ge=0)
    total_pages: int = Field(default=0, ge=0)


class PaginatedResponse(BaseModel, Generic[DataT]):
    items: List[DataT] = Field(default_factory=list)
    meta: PaginationMeta
