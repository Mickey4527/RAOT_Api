from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.models.role import Role

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
    async def get_role_by_name(session: AsyncSession, role_name: str):
        stmp = select(Role).where(Role.role_name == role_name)
        result = await session.execute(stmp)
        role = result.scalars().first()

        return role
    
    @staticmethod
    async def create_role(session: AsyncSession, role_create: Role):
        new_role = Role(
            role_name=role_create.role_name,
            role_description=role_create.role_description
        )

        session.add(new_role)
        await session.commit()
        await session.refresh(new_role)

        return new_role
    

    # Example 
    # Permission.read.permission_name