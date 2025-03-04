import asyncio
import os
import logging
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db_config import get_async_engine, init_db
from app.core.config import settings

async def init() -> None:
    async_engine = get_async_engine()
    async with AsyncSession(bind=async_engine) as session:
        try:
            logging.info("Creating initial data")
            await init_db(session)
            logging.info("Initial data created successfully")

        except Exception as e:
            logging.error(f"An error occurred: {e}")
            logging.error("Initial data creation failed")
            exit(1)

        
def main() -> None:
    asyncio.run(init())
    os.system('cls' if os.name == 'nt' else 'clear')
    logging.info("Initial data created successfully")


if __name__ == "__main__":
    main()