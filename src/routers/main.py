from fastapi import APIRouter

from src.routers.routes.province_router import router as province_router
from src.routers.routes.user_router import router as user_router
from src.routers.routes.district_router import router as district_router
from src.routers.routes.geography_router import router as geography_router
from src.routers.routes.sub_district_router import router as sub_district_router

# from app.core.config import settings

api_router = APIRouter()
api_router.include_router(province_router)
api_router.include_router(user_router)
api_router.include_router(district_router)
api_router.include_router(geography_router)
api_router.include_router(sub_district_router)

# if settings.ENVIRONMENT == "local":
#     api_router.include_router(private.router)