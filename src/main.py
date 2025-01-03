from fastapi import FastAPI
from loguru import logger

from src.db.main import init_db
from src.config import settings
from src.routers.main import api_router

def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    return app

app = get_app()