import asyncio
from loguru import logger
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.main import get_async_engine, init_db
from app.config import settings

async def init() -> None:
    async_engine = get_async_engine()
    async with AsyncSession(bind=async_engine) as session:
        try:
            logger.info("Creating initial data")
            await init_db(session)
            logger.success("Initial data created successfully")

        except Exception as e:
            logger.error(f"An error occurred: {e}")
            logger.error("Initial data creation failed")
            # exit(1)

        
def main() -> None:
    asyncio.run(init())


if __name__ == "__main__":
    main()