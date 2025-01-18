from sqlalchemy import or_
from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.user_profile import UserProfile
from app.schemas import UserLoginSchema, UserCreateSchema, UserDetailSchema, QuerySchema
from app.models import UserAccount
from app.helpers.password_service import get_password_hash, verify_password, random_password

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
    async def create_user(session: AsyncSession, user_create: UserCreateSchema):

        try:
            # TODO: เพิ่ม role in UserRole
            new_user = UserAccount(
                username=user_create.username,
                email_primary=user_create.email_primary,
                password_hash=get_password_hash(user_create.password),
                telephone=user_create.telephone
            )

            session.add(new_user)
            await session.commit()
            await session.refresh(new_user)

            new_user_profile = UserProfile(
                user_id=new_user.id,
                first_name=user_create.first_name,
                last_name=user_create.last_name,
                email_secondary=user_create.email_secondary
            )

            session.add(new_user_profile)
            await session.commit()
            await session.refresh(new_user_profile)
            
            return True
        
        except Exception as e:
            return False
    
    @staticmethod
    async def authenticate_user(session: AsyncSession, user_auth: UserLoginSchema):

        user = await UserService.get_user(session, user_auth.username)
        
        if not user:
            return False
        if not verify_password(user_auth.password, user.password_hash):
            return False
        return UserDetailSchema.model_validate(user)
    
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

