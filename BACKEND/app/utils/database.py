from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, AsyncEngine
from sqlalchemy.orm import sessionmaker
from models.database import Base
from repositories import *
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from cfg import cfg


DATABASE_URL = f"sqlite+aiosqlite:///./database.db" # Заменится на ссылку на реальную базу

engine: AsyncEngine = create_async_engine(DATABASE_URL, echo=True)

AsyncSessionLocal = sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False
)



class UnitOfWork:
    def __init__(self, session_factory):
        self.session_factory = session_factory
        self.session: AsyncSession | None = None

    async def __aenter__(self):
        self.session = self.session_factory()
        await self.session.begin()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            await self.session.rollback()
        else:
            await self.session.commit()
        await self.session.close()

    @property
    def user_repository(self) -> UserRepository:
        return UserRepository(self.session)

    @property
    def redis_repository(self) -> RedisRepository:
        return RedisRepository(cfg.get_redis_url())

    @property
    def ticket_repository(self) -> TicketRepository:
        return TicketRepository(self.session)


@asynccontextmanager
async def get_uow() -> AsyncGenerator[UnitOfWork, None]:
    session = AsyncSessionLocal()
    try:
        async with session.begin():
            uow = UnitOfWork(session)
            try:
                yield uow
            except Exception as e:
                await session.rollback()
                raise

    finally:
        session.close()

async def get_uow_dep() -> AsyncGenerator[UnitOfWork, None]:
    async with UnitOfWork(AsyncSessionLocal) as uow:
        yield uow