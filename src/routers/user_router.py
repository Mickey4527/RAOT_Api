from datetime import timedelta
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from src.helpers.error import raise_http_exception, error_response
from src.schemas import Result, UserLoginSchema, UserCreateSchema, Token, UserDetailSchema
from src.services import UserService, TokenService
from src.routers.deps import SessionDep, get_current_user
from src.config import settings

router = APIRouter(prefix="/u", tags=["user"])

@router.get("/", response_model=Result)
async def get_user_all(session: SessionDep):
    try:
        result = await UserService.get_users(session)
        
        if not result:
            raise raise_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Users not found"
            )

        return Result.model_validate({
            "success": True,
            "message": "Users retrieved successfully",
            "data": [UserDetailSchema.model_validate(user) for user in result]
        })
    
    except Exception as e:
        return raise_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    
@router.post("/login/auth")
async def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    try:
        user = await UserService.authenticate_user(session, form_data)
        if not user:
            return error_response(
                status_code=status.HTTP_401_UNAUTHORIZED,
                message="Incorrect username or password"
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenService.create_access_token(
            subject=user, expires_delta=access_token_expires
        )
        return Token(access_token=access_token, token_type="bearer").model_dump()
        
    except Exception as e:
        return raise_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    
@router.post("/register", response_model=Result)
async def register_user(session: SessionDep, user_create: UserCreateSchema):
    try:
        email_check = await UserService.get_user(session, user_create.email)
        username_check = await UserService.get_user(session, user_create.username)

        if email_check or username_check:
            return raise_http_exception(
                status_code=status.HTTP_400_BAD_REQUEST,
                message="User already exists"
            )
        
        new_user = await UserService.create_user(session, user_create)
        return Result.model_validate({
            "success": True,
            "message": "User created successfully",
            "data": new_user
        })
    
    except Exception as e:
        return raise_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    
@router.get("/me", dependencies=[Depends(get_current_user)])
async def read_users_me():
    return "Hello, "