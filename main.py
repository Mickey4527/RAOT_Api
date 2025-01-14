import asyncio
import uvicorn
from loguru import logger
from app.config import settings
from app.db.main import delete_all_data

from app.initial_data import main

if __name__ == "__main__":

    main()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)

    if settings.ENVIRONMENT == "local":
        logger.info("Dropping all data")
        logger.warning(f'Environment: {settings.ENVIRONMENT}')
        asyncio.run(delete_all_data())
        logger.success("All data dropped successfully")

    if settings.ENVIRONMENT == "test":
        logger.info("Dropping all data")
        logger.warning(f'Environment: {settings.ENVIRONMENT}')
        asyncio.run(delete_all_data())
        logger.success("All data dropped successfully")
