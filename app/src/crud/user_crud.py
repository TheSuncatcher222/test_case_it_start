from typing import Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.crud.base_crud import BaseAsyncCrud
from src.models.user import User
from src.schemas.user import UserCreate, UserUpdate


class CrudUser(BaseAsyncCrud[User, UserCreate, UserUpdate]):

    async def retrieve_by_email(
        self,
        *,
        session: AsyncSession,
        email: str
    ) -> Optional[User]:
        query = select(self.model).where(self.model.email == email)
        result = await session.execute(query)
        return result.scalars().first()


user_crud = CrudUser(User)
