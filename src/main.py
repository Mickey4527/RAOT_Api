from fastapi import FastAPI
from loguru import logger

from src.db.main import init_db
from src.config import settings
from src.routers.main import api_router


async def lifespan(app: FastAPI):
    try:
        await init_db()
        yield
    except Exception as e:
        logger.error(f"Error during startup: {e}")
        raise
    finally:
        logger.info("Server is shutting down")


def get_app() -> FastAPI:
    app = FastAPI(
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        lifespan=lifespan
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = get_app()