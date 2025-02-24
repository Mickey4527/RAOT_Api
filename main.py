import uvicorn
import asyncio

from app.initial_data import main
from app.core.db_config import delete_all_data
from app.core.config import settings

if __name__ == "__main__":
    main()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    if settings.ENVIRONMENT == "local":
        asyncio.run(delete_all_data())

    if settings.ENVIRONMENT == "test":
        asyncio.run(delete_all_data())