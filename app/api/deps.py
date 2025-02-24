from fastapi.security import OAuth2PasswordBearer
import jwt
import logging
from collections.abc import AsyncGenerator
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from fastapi import Depends, Request
from typing import Annotated
from pydantic import ValidationError


from app.core.db_config import get_async_engine, get_casbin_enforcer
from app.core.config import settings
from app.services.user_service import UserService
from app.schemas import TokenData
from app.utilities.app_exceptions import APIException

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

async_engine = get_async_engine()

async_session_maker = async_sessionmaker(
    bind=async_engine,
    expire_on_commit=False,
    class_=AsyncSession,
)

async def get_db() -> AsyncGenerator[AsyncSession, None]:
    logger.debug("Creating a new database session")
    async with async_session_maker() as session:
        yield session
    logger.debug("Database session closed")

SessionDep = Annotated[AsyncSession, Depends(get_db)]

def get_casbin_dependency() -> AsyncGenerator:
    logger.debug("Getting Casbin dependency")
    return Depends(get_casbin_enforcer)

enforcerDep = Annotated[AsyncGenerator, Depends(get_casbin_dependency)]

def get_trace_id(request: Request) -> str | None:

    """
    Get the trace ID from the request.
    """
    trace_id = getattr(request.state, "trace_id", None)
    logger.debug(f"Retrieved trace ID: {trace_id}")

    return trace_id

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/user/login/auth"
)
TokenDep = Annotated[str, Depends(reusable_oauth2)]

async def get_current_user(session: SessionDep, token: TokenDep, req: Request):
    
    trace_id = get_trace_id(req)
    logger.debug(f"Authenticating user with trace ID: {trace_id}")

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
        username: str = payload.get("username")
        logger.debug(f"Decoded JWT payload: {payload}")

        if username is None:
            logger.warning("Token missing username")
            raise APIException(status_code=400, message="Invalid token", trace_id=trace_id)

        token_data = TokenData(username=username)
    
    except (jwt.InvalidTokenError, ValidationError) as e:
        logger.error(f"Token validation error: {str(e)}")
        raise APIException(status_code=400, message="Could not validate credentials", trace_id=trace_id)

    user = await UserService.get_user(session, token_data.username)
    logger.debug(f"User lookup result: {user}")

    if user is None:
        logger.warning(f"User not found: {token_data.username}")
        raise APIException(status_code=404, message="User not found", trace_id=trace_id)
        
    logger.debug(f"Authenticated user: {user}")
    return user
