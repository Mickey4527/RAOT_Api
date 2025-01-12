import asyncio
import uvicorn
from loguru import logger
from src.config import settings
from src.db.main import delete_all_data

from src.initial_data import main

if __name__ == "__main__":
    main()
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)

    if settings.ENVIRONMENT == "local":
        logger.info("Dropping all data")
        logger.warning(f'Environment: {settings.ENVIRONMENT}')
        asyncio.run(delete_all_data())
        logger.success("All data dropped successfully")