from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import get_current_user
from app.schemas import ProductPredictSchema, Result

router = APIRouter(prefix="/predict", tags=["predict"])

@router.post("/product", response_model=Result)
async def predict_product(item: ProductPredictSchema):
    return {"message": "Predicted product successfully", "item": item}