from uuid import UUID
import casbin
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.role import Role
from app.models.user_role import UserRole

class RoleService:
    @staticmethod
    async def get_roles(session: AsyncSession):
        stmp = select(Role)
        result = await session.execute(stmp)
        roles = result.scalars().all()

        return roles
    
    @staticmethod
    async def get_role_by_id(session: AsyncSession, role_id: str):
        stmp = select(Role).where(Role.id == role_id)
        result = await session.execute(stmp)
        role = result.scalars().first()

        return role
    
    @staticmethod
    async def get_role_by_name(session: AsyncSession, name: str):
        stmp = select(Role).where(Role.name == name)
        result = await session.execute(stmp)
        role = result.scalars().first()

        return role
    
    @staticmethod
    async def create_role(session: AsyncSession, role_create: Role):
        new_role = Role(
            name=role_create.name,
            description=role_create.description
        )

        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)

        return new_role
    
    @staticmethod
    async def define_user_role(session: AsyncSession, enforcer: casbin.AsyncEnforcer, user_id: str, roles: list):
        try:
            user_roles = []

            for role in roles:
                role_id = await RoleService.get_role_by_name(session, role)
                if not role_id:
                    raise ValueError(f"Role '{role}' not found")

                new_user_role = UserRole(user_id=user_id, role_id=role_id.id)
                session.add(new_user_role)
                user_roles.append(new_user_role)

                await enforcer.add_grouping_policy(str(user_id), role)

            await session.flush()
            return True

        except SQLAlchemyError as e:
            await session.rollback()
            raise SQLAlchemyError(f"SQLAlchemy error in define_user_role: {str(e)}")

        except ValueError as e:
            await session.rollback()
            raise ValueError(f"Validation error in define_user_role: {str(e)}")
    
    @staticmethod
    async def get_roles_by_user_id(session: AsyncSession, user_id: UUID):
        stmp = (
        select(Role.name)
        .join(UserRole, UserRole.role_id == Role.id)
        .where(UserRole.user_id == user_id)
        )

        result = await session.execute(stmp)
        role_names = result.scalars().all()
        
        return role_names