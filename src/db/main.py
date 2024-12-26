from __future__ import annotations
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

from src.config import settings

def get_async_engine() -> AsyncEngine:
    
    """
        Return async database engine

    """

    try:
        async_engine: AsyncEngine = create_async_engine(
            url=str(settings.SQLALCHEMY_DATABASE_URI),
            echo=True,
            future=True
        )
    except SQLAlchemyError as e:
        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)

    return async_engine

async def init_db():
    """
        Create table in metadata if they don't exist yet.
    
        This uses a sync connection because the 'create_all' doesn't
        feature async yet.

    """
    
    async_engine = get_async_engine()
    
    async with async_engine.begin() as async_conn:
        # await async_conn.run_sync(Base.metadata.create_all)
        logger.success("Initializing database was successfull.")

    await async_engine.dispose()
