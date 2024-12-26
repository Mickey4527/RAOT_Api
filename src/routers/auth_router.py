from fastapi import APIRouter

from src.schemas import Result, UserLoginSchema

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Result)
async def login(data: UserLoginSchema):
    return Result.model_validate({
        "success": True,
        "message": "Login successful",
        "data": {
            "token": "fake_token"
        }
    })