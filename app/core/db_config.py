from __future__ import annotations

import logging
from sqlalchemy import select, text

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.core.casbin import get_casbin_enforcer
from app.core.config import settings
from app.models.role import Role
from app.schemas.user_schema import UserCreateSchema
from app.services.file_service import FileService
from app.services.role_service import RoleService
from app.services.user_service import UserService

def get_async_engine() -> AsyncEngine:
    """
    Return async database engine
    """
    try:
        logging.info("Creating async database engine")
        return create_async_engine(
            url=str(settings.SQLALCHEMY_DATABASE_URI),
            echo=True,
            future=True
        )
    except SQLAlchemyError:
        logging.error("Unable to establish db engine, database might not exist yet")
        raise


async def init_db(session: AsyncSession):
    """
        Initialize the database with the first superuser and role
    """

    try:
        user_service = UserService(session=session)
        role_service = RoleService(session=session)
        file_service = FileService(session=session)
        enforcer=await get_casbin_enforcer()
        
        role = await role_service.get_role_by_name(name=settings.FIRST_SUPERUSER_ROLE)
        user = await user_service.get_user_by_username(username=settings.FIRST_SUPERUSER_EMAIL)

        if not role and not user:

            role_in = Role(
                name=settings.FIRST_SUPERUSER_ROLE,
                description="Superuser role"
            )

            await role_service.create_role(role_create=role_in)

            user_in = UserCreateSchema(
                username=settings.FIRST_SUPERUSER,
                email_primary=settings.FIRST_SUPERUSER_EMAIL,
                telephone=settings.FIRST_SUPERUSER_PHONE,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                firstname=settings.FIRST_SUPERUSER,
                user_roles=[settings.FIRST_SUPERUSER_ROLE]
            )

            await user_service.create_user(user_create=user_in, enforcer=enforcer)
            await enforcer.add_policy(settings.FIRST_SUPERUSER_ROLE, "/api/*", "*")
            await enforcer.add_policy("*", "/docs", "*")
            await enforcer.add_policy("*", "/api/v1/user/register", "*")
            await enforcer.add_policy("*", "/api/v1/openapi.json", "*")
            await enforcer.add_policy("*", "/api/v1/user/login/auth", "*")
            await enforcer.add_policy("*", "/api/v1/common/*", "*")
            await enforcer.add_policy("user", "/api/*", "GET")
            await enforcer.add_policy("academic", "/api/*", "*")
            await enforcer.save_policy()
            await file_service.import_csv_files(csv_files_import=settings.CSV_FILES_IMPORT)
    
        logging.info("Database initialized")

    except SQLAlchemyError as e:
        logging.debug(f"An error occurred: {e}")
        logging.error("Database initialization failed")
        raise

    except Exception as e:
        logging.debug(f"An error occurred: {e}")
        logging.error("Database initialization failed")
        raise


async def delete_all_data():
    """
    Delete all data from the database
    """
    engine = get_async_engine()

    async with engine.begin() as conn:
        
        tables_query = """
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public' AND tablename != 'alembic_version';
        """

        tables = await conn.execute(text(tables_query))
        table_names = ", ".join([f'"{row.tablename}"' for row in tables])

        if table_names:
            await conn.execute(text(f"TRUNCATE TABLE {table_names} CASCADE;"))
        
        await conn.commit()

    # Clear Casbin policies
    enforcer = await get_casbin_enforcer()
    enforcer.clear_policy()
    await enforcer.save_policy()