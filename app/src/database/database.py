from typing import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import (
    AsyncEngine, AsyncSession, async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from src.config.config import settings

DATABASE_URL: str = (
    f'{settings.POSTGRES_USER}:{settings.POSTGRES_PASSWORD}@'
    f'{settings.DB_HOST}:{settings.DB_PORT}/{settings.POSTGRES_DB}'
)

DATABASE_ASYNC_URL: str = f'postgresql+asyncpg://{DATABASE_URL}'

async_engine: AsyncEngine = create_async_engine(
    url=DATABASE_ASYNC_URL,
    echo=settings.DEBUG_DB,
)

async_session_maker: async_sessionmaker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session


DATABASE_SYNC_URL: str = f'postgresql+psycopg2://{DATABASE_URL}'

sync_engine = create_engine(
    url=DATABASE_SYNC_URL,
    echo=settings.DEBUG_DB,
)

sync_session_maker: sessionmaker = sessionmaker(bind=sync_engine)


class Base(DeclarativeBase):
    pass
