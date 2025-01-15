from fastapi import APIRouter, Depends, HTTPException
import requests

from app.api.deps import get_current_user
from app.schemas import ProductPredictSchema, Result
from app.services.predict_service import PredictService

from app.config import settings

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("/product", response_model=Result)
async def predict_product(user_input: ProductPredictSchema):

    payload = await PredictService.data_predict_product(user_input)

    # กำหนด headers สำหรับการส่งข้อมูล
    headers = {"Content-Type": "application/json"}

    # ส่งคำขอไปยัง API สำหรับการทำนาย
    url = f'{settings.PREDICT_API_URL}/v1/models/model_1:predict'
    response = requests.post(url, json=payload, headers=headers)

    # ตรวจสอบผลลัพธ์จากการทำนาย
    if response.status_code == 200:
        predicted_yield = response.json()

        return predicted_yield

    # return {"message": "Predicted product successfully", "item": user_input}