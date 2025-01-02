from __future__ import annotations
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncEngine
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from loguru import logger

from src.config import settings
from src.models.user_account import UserAccount
from src.models.user_role import UserRole
from src.schemas.user_schema import UserCreateSchema
from src.services.role_service import RoleService
from src.services.user_service import UserService

def get_async_engine() -> AsyncEngine:
    
    """
        Return async database engine

    """

    try:
        async_engine: AsyncEngine = create_async_engine(
            url=str(settings.SQLALCHEMY_DATABASE_URI),
            echo=True,
            future=True
        )
    except SQLAlchemyError as e:
        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)

    return async_engine

async def init_db(session: Session):
    """
        Create table in metadata if they don't exist yet.
    
        This uses a sync connection because the 'create_all' doesn't
        feature async yet.

    """
    
    async_engine = get_async_engine()

    
    roles = await session.execute(
        select(UserRole).where(UserRole.role_name == settings.FIRST_SUPERUSER_ROLE)
        ).first()
    user = session.execute(
        select(UserAccount).where(UserAccount.email == settings.FIRST_SUPERUSER)
    ).first()

    if not roles and not user:
        role_in = UserRole(
            role_name=settings.FIRST_SUPERUSER_ROLE,
            role_description=settings.FIRST_SUPERUSER_ROLE_DESCRIPTION
        )
        user_in = UserCreateSchema(
            email=settings.FIRST_SUPERUSER,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            is_superuser=True,
        )

        await RoleService.create_role(session=session, role=role_in)
        await UserService.create_user(session=session, user_create=user_in)

    # await async_conn.run_sync(Base.metadata.create_all)

    logger.success("Initializing was successfull.")

    await async_engine.dispose()
