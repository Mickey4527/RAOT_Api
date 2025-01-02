from collections.abc import AsyncGenerator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker

from src.db.main import get_async_engine
from src.config import settings
from src.helpers.error import raise_http_exception
from src.schemas import TokenData
from src.services import UserService

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/u/login/auth"
)

async_session_maker = async_sessionmaker(
    bind=get_async_engine(),
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session_maker() as session:
        yield session

SessionDep = Annotated[AsyncSession, Depends(get_db)]
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session:SessionDep ,token: TokenDep):

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("username")
        if username is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        token_data = TokenData(username=username)

    except (jwt.InvalidTokenError, ValidationError):
        raise raise_http_exception(
            status_code=status.HTTP_403_FORBIDDEN,
            message="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    user = await UserService.get_user(session, token_data.username)
    if user is None:
        raise raise_http_exception(
            status_code=status.HTTP_401_UNAUTHORIZED,
            message="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        
    return user


async def get_current_active_user(current_user: UserService = Depends(get_current_user)):
    if not current_user.is_active:
        raise raise_http_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="Inactive user"
        )
    return current_user

async def get_current_active_superuser(current_user: UserService = Depends(get_current_user)):
    if not current_user.is_superuser:
        raise raise_http_exception(
            status_code=status.HTTP_400_BAD_REQUEST,
            message="The user doesn't have enough privileges"
        )
    return current_user


