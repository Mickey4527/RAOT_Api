from datetime import timedelta
from typing import Annotated
from sqlalchemy.exc import SQLAlchemyError
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas import Result, UserLoginSchema, UserCreateSchema, Token, UserDetailSchema, QuerySchema
from app.services import UserService, TokenService
from app.api.deps import SessionDep, get_current_user
from app.config import settings

router = APIRouter(prefix="/u", tags=["user"])

@router.get("/", response_model=Result)
async def get_user_all(session: SessionDep, query: QuerySchema = Depends()):
    
    try:

        result = await UserService.get_users(session, query)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=Result.model_validate({
                    "success": False,
                    "message": "Users not found"
                })
            )

        return Result.model_validate({
            "success": True,
            "message": "Users retrieved successfully",
            "data": [UserDetailSchema.model_validate(user) for user in result]
        })
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )
    
@router.post("/login/auth")
async def login_for_access_token(session: SessionDep, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
   
    try:

        user = await UserService.authenticate_user(session, form_data)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={
                    "success": False,
                    "message": "Incorrect username or password"
                }
            )
        
        access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = TokenService.create_access_token(
            subject=user, expires_delta=access_token_expires
        )

        return Token(access_token=access_token, token_type="bearer", expires_in=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )
    
@router.post("/register", response_model=Result)
async def register_user(session: SessionDep, user_create: UserCreateSchema):
    try:
        email_check = await UserService.get_user(session, user_create.email)
        username_check = await UserService.get_user(session, user_create.username)

        if email_check or username_check:
            return HTTPException(
                status_code=400,
                detail=Result.model_validate({
                    "success": False,
                    "message": "User already exists"
                })
            )
        
        new_user = await UserService.create_user(session, user_create)
        return Result.model_validate({
            "success": True,
            "message": "User created successfully",
            "data": UserDetailSchema.model_validate(new_user)
        })
    
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )
    
# @router.get("/create", response_model=Result)
# async def create_user(session: SessionDep):
#     try:
#         user = await UserService.create_user(session)

#         return Result.model_validate({
#             "success": True,
#             "message": "User created successfully",
#             "data": user
#         })
    
#     except Exception as e:
#         return raise_http_exception(
#             status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
#             message=str(e)
#         )
    
    
@router.get("/me", dependencies=[Depends(get_current_user)])
async def read_users_me():
    return "Hello, "

