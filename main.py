import uvicorn
import asyncio

from app.initial_data import main
from app.core.db_config import delete_all_data

if __name__ == "__main__":
    main()
    uvicorn.run("app.main:app", host="127.0.0.1", port=8000, reload=True)
    asyncio.run(delete_all_data())