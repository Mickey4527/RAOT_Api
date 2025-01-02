from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.user_role import UserRole

class RoleService:
    @staticmethod
    async def get_roles(session: Session):
        stmp = select(UserRole)
        result = await session.execute(stmp)
        roles = result.scalars().all()

        return roles
    
    @staticmethod
    async def get_role(session: Session, role_id: str):
        stmp = select(UserRole).where(UserRole.id == role_id)
        result = await session.execute(stmp)
        role = result.scalars().first()

        return role
    
    @staticmethod
    async def get_role_by_name(session: Session, role_name: str):
        stmp = select(UserRole).where(UserRole.role_name == role_name)
        result = await session.execute(stmp)
        role = result.scalars().first()

        return role
    
    @staticmethod
    async def create_role(session: Session, role: UserRole):
        new_role = UserRole(
            role_name=role.role_name,
            role_description=role.role_description
        )

        session.add(new_role)
        await session.commit()
        session.refresh(new_role)

        return new_role