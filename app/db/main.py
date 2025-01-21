from __future__ import annotations
import os
import casbin
import casbin_async_sqlalchemy_adapter
from sqlalchemy import select, text

from sqlalchemy.ext.asyncio import AsyncEngine, create_async_engine, AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from loguru import logger

from app.config import settings
from app.models.user_account import UserAccount
from app.models.role import Role
from app.schemas.user_schema import UserCreateSchema
from app.services.role_service import RoleService
from app.services.user_service import UserService
from app.services.data_service import DataService

def get_async_engine() -> AsyncEngine:
    """
    Return async database engine
    """
    try:
        return create_async_engine(
            url=str(settings.SQLALCHEMY_DATABASE_URI),
            echo=True,
            future=True
        )
    except SQLAlchemyError as e:

        logger.warning("Unable to establish db engine, database might not exist yet")
        logger.warning(e)
        raise


async def get_casbin_enforcer() -> casbin.AsyncEnforcer:
    """
    Initialize Casbin AsyncEnforcer with the SQLAlchemy adapter
    """

    adapter = casbin_async_sqlalchemy_adapter.Adapter(str(settings.SQLALCHEMY_DATABASE_URI))
    path_enforcer = os.path.join(os.path.dirname(__file__), 'rbac_model.conf')
    
    enforcer = casbin.AsyncEnforcer(path_enforcer, adapter)
    await enforcer.load_policy()  # Load policies into memory

    return enforcer



async def init_db(session: AsyncSession):
    """
        Initialize the database with the first superuser and role

    """

    await DataService.import_csv_files(session=session, csv_files_import=settings.CSV_FILES_IMPORT)

    role = await RoleService.get_role_by_name(session=session, name=settings.FIRST_SUPERUSER_ROLE)
    user = await UserService.get_user(session=session, username=settings.FIRST_SUPERUSER)


    if not role and not user:
        user_in = UserCreateSchema(
            username=settings.FIRST_SUPERUSER,
            email_primary=settings.FIRST_SUPERUSER_EMAIL,
            telephone=settings.FIRST_SUPERUSER_PHONE,
            password=settings.FIRST_SUPERUSER_PASSWORD,
            firstname=settings.FIRST_SUPERUSER,
            user_roles=[settings.FIRST_SUPERUSER_ROLE]
        )

        role_in = Role(
            name=settings.FIRST_SUPERUSER_ROLE,
            description="Superuser role"
        )  
        
        await RoleService.create_role(session=session, role_create=role_in)

        enforcer = await get_casbin_enforcer()

        await enforcer.add_policy(settings.FIRST_SUPERUSER_ROLE, "/api/*", "*")
        await UserService.create_user(session=session, enforcer=enforcer, user_create=user_in)
        await enforcer.add_policy("*", "/docs", "*")
        await enforcer.add_policy("*", "/api/v1/u/register", "*")
        await enforcer.add_policy("*", "/api/v1/openapi.json", "*")
        await enforcer.add_policy("*", "/api/v1/u/login/auth", "*")
        await enforcer.add_policy("user", "/api/*", "GET")
        await enforcer.save_policy()

        


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

        # Clear Casbin policies
    enforcer = await get_casbin_enforcer()
    enforcer.clear_policy()
    await enforcer.save_policy()

