from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.main import get_async_engine

async_session_maker = async_sessionmaker(
    bind=get_async_engine(),
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]

