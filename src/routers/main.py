from fastapi import APIRouter

from src.routers.province_router import router as province_router
from src.routers.auth_router import router as auth_router
# from app.core.config import settings

api_router = APIRouter()
api_router.include_router(province_router)
api_router.include_router(auth_router)

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)