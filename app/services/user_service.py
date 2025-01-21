import casbin
from fastapi import HTTPException, status
from sqlalchemy import or_
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError

from app.models.user_profile import UserProfile
from app.schemas import UserLoginSchema, UserCreateSchema, UserDetailSchema, QuerySchema
from app.models import UserAccount
from app.helpers.password_service import get_password_hash, verify_password, random_password
from app.services.role_service import RoleService

class UserService:
    
    @staticmethod
    async def get_users(session: AsyncSession, query: QuerySchema):

        stmp = select(UserAccount).limit(query.limit).offset(query.offset)
        result = await session.execute(stmp)
        users = result.scalars().all()

        return users

    @staticmethod
    async def get_user_by_id(session: AsyncSession, user_id: str):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        user = result.scalars().first()

        return user

    @staticmethod
    async def get_user(session: AsyncSession, username: str):
        stmp = select(UserAccount).filter(or_(UserAccount.email_primary == username, UserAccount.username == username))
        result = await session.execute(stmp)
        user = result.scalars().first()

        return user
    
    @staticmethod
    async def get_user_profile(session: AsyncSession, user_id: str):
        try:
            stmp = select(UserProfile).where(UserProfile.user_id == user_id)
            result = await session.execute(stmp)
            user_profile = result.scalars().first()

            return user_profile
        
        except SQLAlchemyError as e:
            raise SQLAlchemyError(str(e))
    
    @staticmethod
    async def create_user(session: AsyncSession, enforcer: casbin.AsyncEnforcer, user_create: UserCreateSchema):

        try:

            existing_user = await session.execute(
                select(UserAccount).where(
                    (UserAccount.email_primary == user_create.email_primary) |
                    (UserAccount.username == user_create.username)
                )
            )
            existing_user = existing_user.scalar()

            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="มีผู้ใช้งานนี้อยู่ในระบบแล้ว"
                )

            new_user = UserAccount(
                username=user_create.username,
                email_primary=user_create.email_primary,
                password_hash=get_password_hash(user_create.password),
                telephone=user_create.telephone
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            role = await RoleService.define_user_role(session,enforcer, new_user.id, user_create.user_roles)

            if not role:
                raise ValueError("ไม่สามารถกำหนดสิทธิ์ผู้ใช้งานได้")

            new_user_profile = UserProfile(
                user_id=new_user.id,
                firstname=user_create.firstname,
                lastname=user_create.lastname,
                email_secondary=user_create.email_secondary
            )

            session.add(new_user_profile)
            await session.commit()
            await session.refresh(new_user_profile)
                
            return new_user

        except SQLAlchemyError as e:
            await session.rollback()
            raise SQLAlchemyError(str(e))
        
        except ValueError as e:
            await session.rollback()
            raise ValueError(str(e))
        
    
    @staticmethod
    async def authenticate_user(session: AsyncSession, user_auth: UserLoginSchema):

        user = await UserService.get_user(session, user_auth.username)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="บัญชีผู้ใช้งานไม่ถูกต้อง1"
            )
        
        if not verify_password(user_auth.password, user.password_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="รหัสผ่านไม่ถูกต้อง2"
            )

        return user
    
    
    @staticmethod
    async def update_user(session: AsyncSession, user_id: str, user: UserDetailSchema):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        existing_user = result.scalars().first()

        if not existing_user:
            return False

        existing_user.email = user.email
        existing_user.telephone = user.telephone
        await session.commit()

        return True
    
    @staticmethod
    async def update_password(session: AsyncSession, user_id: str, password: str):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        existing_user = result.scalars().first()

        if not existing_user:
            return False

        existing_user.password_hash = get_password_hash(password)
        await session.commit()

        return True
    
    @staticmethod
    async def delete_user(session: AsyncSession, user_id: str):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        existing_user = result.scalars().first()

        if not existing_user:
            return False

        session.delete(existing_user)
        await session.commit()
        await session.refresh(existing_user)

        return True
    
    # @staticmethod
    # async def create_user(session: AsyncSession, user_create: UserCreateSchema):
    #     password_random = random_password()
    #     new_user = UserAccount(
    #         email=user_create.email,
    #         password_hash=get_password_hash(password_random)
    #     )
        
    #     session.add(new_user)
    #     await session.commit()
    #     await session.refresh(new_user)

    #     return UserDetailSchema.model_validate(new_user), password_random

