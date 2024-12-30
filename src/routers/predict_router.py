from fastapi import APIRouter, Depends

from src.routers.deps import get_current_user


router = APIRouter(prefix="/predict", tags=["predict"], dependencies=[Depends(get_current_user)])