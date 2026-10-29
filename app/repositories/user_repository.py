"""
User Database Repository.
==============================================================================
Specialized repository for querying and managing User entities in the database.
==============================================================================
"""

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user import User
from app.repositories.base import BaseRepository
from app.schemas.user import UserCreate, UserUpdate


class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    """Repository handling database queries for User entities."""

    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_by_email(self, email: str) -> User | None:
        """Find a user by normalized lowercase email address."""
        stmt = select(User).where(User.email == email.strip().lower())
        result = await self.session.execute(stmt)
        return result.scalars().first()
