from fastapi import APIRouter
from app.api.routes import (
    province_router, 
    user_router,
    predict_router,
    common_router
)
    

def get_api_router():
    """
    Return APIRouter
    """

    api_router = APIRouter()
    api_router.include_router(province_router.router)
    api_router.include_router(user_router.router)
    api_router.include_router(predict_router.router)
    api_router.include_router(common_router.router)

    return api_router