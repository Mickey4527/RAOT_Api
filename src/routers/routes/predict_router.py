from fastapi import APIRouter, Depends, HTTPException

from src.routers.deps import get_current_user
from src.schemas.predict_schema import PredictSchema
from src.services.predict_service import PredictService

router = APIRouter(prefix="/predict", tags=["predict"], dependencies=[Depends(get_current_user)])

# TODO fix this
@router.post("/")
async def predict_endpoint(data: PredictSchema):
    try:
        result = PredictService.predict_rubber_content(data)
        # result = predict_rubber_content(data)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))