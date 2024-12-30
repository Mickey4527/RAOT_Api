from sqlalchemy import or_
from sqlalchemy.orm import Session
from src.schemas import UserSchema, UserLoginSchema, UserCreateSchema, UserDetailSchema
from src.models import UserAccount
from sqlalchemy.sql import select
from src.helpers.password_service import get_password_hash, verify_password
class UserService:
    
    @staticmethod
    def get_users(session: Session):
        stmp = select(UserAccount)
        result = session.execute(stmp)
        users = result.scalars().all()

        return users

    @staticmethod
    async def get_user_by_id(session: Session, user_id: str):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        user = result.scalars().first()

        return user

    @staticmethod
    async def get_user(session: Session, username: str):
        stmp = select(UserAccount).filter(or_(UserAccount.email == username, UserAccount.username == username))
        result = await session.execute(stmp)
        user = result.scalars().first()

        return user
    
    @staticmethod
    async def create_user(session: Session, user: UserCreateSchema):

        new_user = UserAccount(
            email=user.email,
            password_hash=get_password_hash(user.password),
            telephone=user.telephone,
            user_type=user.user_type
        )

        session.add(new_user)
        await session.commit()
        session.refresh(new_user)
        
        return UserDetailSchema.model_validate(new_user)
    
    @staticmethod
    async def authenticate_user(session: Session, user_auth: UserLoginSchema):

        user = await UserService.get_user(session, user_auth.username)
        
        if not user:
            return False
        if not verify_password(user_auth.password, user.password_hash):
            return False
        return UserDetailSchema.model_validate(user)
    
    @staticmethod
    async def update_user(session: Session, user_id: str, user: UserDetailSchema):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        existing_user = result.scalars().first()

        if not existing_user:
            return False

        existing_user.email = user.email
        existing_user.telephone = user.telephone
        existing_user.user_type = user.user_type
        await session.commit()

        return True
    
    @staticmethod
    async def update_password(session: Session, user_id: str, password: str):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        existing_user = result.scalars().first()

        if not existing_user:
            return False

        existing_user.password_hash = get_password_hash(password)
        await session.commit()

        return True
    
    @staticmethod
    async def delete_user(session: Session, user_id: str):
        stmp = select(UserAccount).where(UserAccount.id == user_id)
        result = await session.execute(stmp)
        existing_user = result.scalars().first()

        if not existing_user:
            return False

        session.delete(existing_user)
        await session.commit()

        return True