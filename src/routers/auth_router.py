from fastapi import APIRouter

from src.schemas import Result, UserLoginSchema
from src.routers.deps import SessionDep

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/login", response_model=Result)
async def login(session: SessionDep, user: UserLoginSchema):
    return Result.model_validate({
        "success": True,
        "message": "Login successful",
        "data": {
            "token": "fake_token"
        }
    })