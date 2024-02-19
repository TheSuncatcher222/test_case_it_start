from typing import Generic, Optional, Type, TypeVar

from pydantic import BaseModel
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from sqlalchemy.orm.decl_api import DeclarativeBase

ModelType = TypeVar("ModelType", bound=DeclarativeBase)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class BaseAsyncCrud(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    """
    Класс, предоставляющий базовые методы: Create, Retrieve, Update, Delete.

    Используемые параметры:
        - ModelType: модель SQLAlchemy
        - CreateSchemaType: модель Pydantic для создания данных
        - UpdateSchemaType: модель Pydantic для обновления данных
    """

    def __init__(self, model: Type[ModelType]):
        self.model = model

    async def create(
        self,
        *,
        session: AsyncSession,
        obj_data: CreateSchemaType,
    ) -> ModelType:
        """Создает объект в базе данных."""
        data = obj_data.model_dump(exclude_unset=True)
        stmt = insert(self.model).values(**data).returning(self.model)
        res = await session.execute(stmt)
        await session.commit()
        return res.scalars().first()

    async def retrieve_by_id(
        self,
        *,
        session: AsyncSession,
        obj_id: int,
    ) -> Optional[ModelType]:
        """Возвращает объект с указанным ID из базы данных."""
        return await session.get(self.model, obj_id)

    async def retrieve_multi(
        self,
        *,
        session: AsyncSession,
        limit: int = 15,
        offset: int = 0,
    ) -> list[ModelType]:
        """Возвращает все объекты из базы данных в соответствии с параметрами пагинации."""
        query = select(self.model).limit(limit).offset(offset)
        result = await session.execute(query)
        return result.scalars().all()

    async def retrieve_by_uid(
        self,
        *,
        session: AsyncSession,
        uid: str,
    ) -> Optional[ModelType]:
        """Возвращает объект с указанным uuid из базы данных."""
        statement = select(self.model).where(self.model.uid == uid)
        result = await session.execute(statement)
        return result.scalars().first()
