from __future__ import annotations
from sqlalchemy import select, text

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from loguru import logger

from src.config import settings
from src.models.user_account import UserAccount
from src.models.user_role import UserRole
from src.schemas.user_schema import UserCreateSchema
from src.services.role_service import RoleService
from src.services.user_service import UserService
from src.services.data_service import DataService
from src.models import Geography

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


async def init_db(session: AsyncSession):
    """
        Initialize the database with the first superuser and role

    """

    role = await RoleService.get_role_by_name(session=session, role_name=settings.FIRST_SUPERUSER_ROLE)
    user = await UserService.get_user(session=session, username=settings.FIRST_SUPERUSER)


    if not role and not user:
        
        role_in = UserRole(
            role_name=settings.FIRST_SUPERUSER_ROLE,
            role_description=settings.FIRST_SUPERUSER_ROLE_DESCRIPTION
        )

        role_result = await RoleService.create_role(session=session, role_create=role_in)

        user_in = UserCreateSchema(
            username=settings.FIRST_SUPERUSER,
            email=settings.FIRST_SUPERUSER_EMAIL,
            telephone=settings.FIRST_SUPERUSER_PHONE,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            user_role_id=role_result.id
        )
        
        await UserService.create_user(session=session, user_create=user_in)
        await DataService.import_csv_files(session=session, csv_files_import=settings.CSV_FILES_IMPORT)
    
    


async def delete_all_data():

    engine = get_async_engine()

    async with engine.begin() as conn:
        
        tables_query = """
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public';
        """

        tables = await conn.execute(text(tables_query))
        table_names = ", ".join([f'"{row.tablename}"' for row in tables])

        if table_names:
            await conn.execute(text(f"TRUNCATE TABLE {table_names} CASCADE;"))
        
        await conn.commit()
