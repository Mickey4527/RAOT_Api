from fastapi import APIRouter

from src.routers.province_router import router as province_router
from src.routers.user_router import router as user_router
from src.routers.district_router import router as district_router
from src.routers.geography_router import router as geography_router
# from app.core.config import settings

api_router = APIRouter()
api_router.include_router(province_router)
api_router.include_router(user_router)
api_router.include_router(district_router)
api_router.include_router(geography_router)

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)