"""
Generic Async Database Repository.
==============================================================================
Implements the Repository Pattern for abstracting SQLAlchemy 2.0 async queries
from business logic services, providing clean type-safe CRUD operations.
==============================================================================
"""

from typing import Any
from pydantic import BaseModel
from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.base import Base


class BaseRepository[ModelT: Base, CreateSchemaT: BaseModel, UpdateSchemaT: BaseModel]:
    """
    Generic Asynchronous Repository providing reusable CRUD operations.
    """

    def __init__(self, model: type[ModelT], session: AsyncSession):
        self.model = model
        self.session = session

    async def get(self, id: Any) -> ModelT | None:
        """Fetch a single record by primary key."""
        stmt = select(self.model).where(self.model.id == id)
        result = await self.session.execute(stmt)
        return result.scalars().first()

    async def list(self, skip: int = 0, limit: int = 100) -> list[ModelT]:
        """Fetch a paginated list of records."""
        stmt = select(self.model).offset(skip).limit(limit)
        result = await self.session.execute(stmt)
        return list(result.scalars().all())

    async def count(self) -> int:
        """Count total records in the entity table."""
        stmt = select(func.count()).select_from(self.model)
        result = await self.session.execute(stmt)
        return int(result.scalar_one_or_none() or 0)

    async def create(self, schema: CreateSchemaT | dict[str, Any]) -> ModelT:
        """Create and persist a new record."""
        if isinstance(schema, dict):
            create_data = schema
        else:
            create_data = schema.model_dump(exclude_unset=True)

        db_obj = self.model(**create_data)
        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def update(self, db_obj: ModelT, schema: UpdateSchemaT | dict[str, Any]) -> ModelT:
        """Update an existing record with partial values."""
        if isinstance(schema, dict):
            update_data = schema
        else:
            update_data = schema.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if hasattr(db_obj, field):
                setattr(db_obj, field, value)

        self.session.add(db_obj)
        await self.session.flush()
        await self.session.refresh(db_obj)
        return db_obj

    async def delete(self, id: Any) -> bool:
        """Delete a record by primary key."""
        db_obj = await self.get(id)
        if db_obj is None:
            return False
        await self.session.delete(db_obj)
        await self.session.flush()
        return True
