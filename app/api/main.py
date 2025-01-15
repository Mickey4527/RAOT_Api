from fastapi import APIRouter

from app.api.routes import province_router, user_router, district_router, geography_router, sub_district_router, private_router, predict_router
from app.config import settings

api_router = APIRouter()
api_router.include_router(province_router.router)
api_router.include_router(user_router.router)
api_router.include_router(district_router.router)
api_router.include_router(geography_router.router)
api_router.include_router(sub_district_router.router)
api_router.include_router(predict_router.router)

if settings.ENVIRONMENT == "local":
    api_router.include_router(private_router.router)