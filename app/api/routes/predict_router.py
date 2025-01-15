from fastapi import APIRouter, Depends, HTTPException, status
import requests

from app.api.deps import get_current_user
from app.schemas import ProductPredictSchema, Result
from app.services.predict_service import PredictService

from app.config import settings

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("/product", response_model=Result)
async def predict_product(user_input: ProductPredictSchema):

    try:

        payload = await PredictService.data_predict_product(user_input)
        headers = {"Content-Type": "application/json"}

        url = f'{settings.PREDICT_API_URL}/v1/models/model_1:predict'
        response = requests.post(url, json=payload, headers=headers)

        if response.status_code == 200:
            predicted_yield = response.json()

            return {
                "success": True,
                "message": "Predicted product successfully",
                "data": predicted_yield
            }
        
        else:
            raise HTTPException(
                status_code=response.status_code,
                detail={
                    "success": False,
                    "message": "Predicted product failed"
                }
            )
        
    except Exception as e:

        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "message": str(e)
            }
       )
