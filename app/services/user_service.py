import logging
import casbin
from uuid import UUID
from sqlalchemy.sql import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError, CompileError, IntegrityError

from app.I18n.load_laguage import get_lang_content
from app.models.user_account import UserAccount
from app.models.user_profile import UserProfile
from app.schemas.base import QuerySchema
from app.schemas.token_schema import TokenSchema
from app.schemas.user_schema import UserCreateSchema, UserLoginSchema
from app.services.role_service import RoleService
from app.services.token_service import TokenService
from app.utilities.app_exceptions import DuplicateResourceException, InvalidAuthorizationException, InvalidOutputException, ResourceNotFoundException, SQLProcessException, ServerProcessException
from app.utilities.password_service import get_password_hash, verify_password

# Configure logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

class UserService:

    def __init__(self, 
                 session: AsyncSession
                 ):
        self.session = session
        self.t = get_lang_content().get("ErrorMessage")
        logger.debug("UserService initialized with session: %s", session)

    def _jsonify_user(self, user):
        return {
            "username": user.username,
            "email_primary": user.email_primary,
            "telephone": user.telephone,
            "firstname": user.profile.firstname if user.profile else None,
            "lastname": user.profile.lastname if user.profile else None,
            "user_roles": [role.name for role in user.roles],
        }
    
    async def get_users(self, query: QuerySchema):
        """
            ดึงข้อมูลผู้ใช้ทั้งหมดจากฐานข้อมูล \n
            Retrieve all user data from the database

            #### Parameters
                query: QuerySchema => ข้อมูล query ที่ใช้ในการดึงข้อมูล \n
                The query data used to retrieve data.

            #### Returns
                list => ข้อมูลผู้ใช้ทั้งหมด \n
                All user data

        """

        logger.debug("Retrieving users with query: %s", query)

        try:

            stmt = (
            select(UserAccount)
            .options(selectinload(UserAccount.profile), selectinload(UserAccount.roles))
            .limit(query.limit).offset(query.offset)
            )

            result = await self.session.execute(stmt)
            users = result.scalars().all()

            if not users:
                logger.debug("No users found")
                return []
            
            logger.debug("Users retrieved successfully")
            return users
        
        except InvalidOutputException as e:
            logger.error("Invalid output exception: %s", e)
            raise e
        
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
        

    async def _get_users_profile(self, users: list):
        """
            ดึงข้อมูลโปรไฟล์ผู้ใช้จากฐานข้อมูล \n
            Retrieve user profile data from the database
        """
        logger.debug("Retrieving user profiles for users: %s", users)

        try:
            user_ids = [user.id for user in users]

            stmp = select(UserProfile).where(UserProfile.user_id.in_(user_ids))
            result = await self.session.execute(stmp)
            user_profile = result.scalars().all()

            logger.debug("User profiles retrieved successfully")
            return user_profile
        
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
        

    async def get_user_by_username(self, username: str):
        """
            ดึงข้อมูลผู้ใช้จากฐานข้อมูลด้วย username \n
            Retrieve user data from the database by username
        """
        
        logger.debug("Retrieving user by username: %s", username)
        try:
            stmt = (
            select(UserAccount)
            .options(selectinload(UserAccount.profile), selectinload(UserAccount.roles))
            .filter(
                (UserAccount.email_primary == username) |
                (UserAccount.username == username))
            )

            result = await self.session.execute(stmt)
            user = result.scalar()

            if not user:
                logger.debug("User not found")
                return None

            logger.debug("User retrieved successfully")

            return user
        
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลผู้ใช้",
            )
        
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
        

    async def create_user(self, enforcer: casbin.AsyncEnforcer, user_create: UserCreateSchema):
        """
            สร้างผู้ใช้ใหม่ \n
            Create a new user
        """
        logger.debug("Creating user: %s", user_create)
        try:
            existing_user = await self.session.execute(
                    select(UserAccount).where(
                        (UserAccount.email_primary == user_create.email_primary) |
                        (UserAccount.username == user_create.username)
                    )
                )

            existing_user = existing_user.scalar()

            if existing_user:
                logger.debug("Duplicate user found")
                raise DuplicateResourceException(message=self.t.get("Conflict"))
                
            new_user = UserAccount(
                    username=user_create.username,
                    email_primary=user_create.email_primary,
                    password_hash=get_password_hash(user_create.password),
                    telephone=user_create.telephone
                )
            
            self.session.add(new_user)
            await self.session.flush()

            await RoleService(self.session).define_user_role(enforcer=enforcer, user_id=new_user.id, roles=user_create.user_roles)

            await self.create_user_profile(user_id=new_user.id, user_profile=user_create)

            await self.session.commit()
            await self.session.refresh(new_user)
                    
            logger.debug("User created successfully")
            return new_user
        
        except (DuplicateResourceException, ResourceNotFoundException) as e:
            await self.session.rollback()
            logger.error("Error creating user: %s", e)
            raise e
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการสร้างผู้ใช้",
            )
        
        except Exception as e:
            await self.session.rollback()
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
        

    async def create_user_profile(self, user_id: UUID, user_profile: UserProfile):
        """
            สร้างโปรไฟล์ผู้ใช้ใหม่ \n
            Create a new user profile
        """
        logger.debug("Creating user profile for user_id: %s", user_id)
        try:
            new_user_profile = UserProfile(
                user_id=user_id,
                firstname=user_profile.firstname,
                lastname=user_profile.lastname,
                email_secondary=user_profile.email_secondary
            )

            self.session.add(new_user_profile)
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการสร้างโปรไฟล์ผู้ใช้",
            )
        
        except Exception as e:
            await self.session.rollback()
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")

    async def update_user(self, user_id: UUID, user_update: UserCreateSchema):
        """
            อัพเดทข้อมูลผู้ใช้ \n
            Update user data
        """
        logger.debug("Updating user with user_id: %s", user_id)
        return None
    
    async def disable_user(self, user_id: UUID):
        """
            ปิดใช้งานผู้ใช้ \n
            Disable user
        """
        logger.debug("Disabling user with user_id: %s", user_id)
        return None
    
    async def enable_user(self, user_id: UUID):
        """
            เปิดใช้งานผู้ใช้ \n
            Enable user
        """
        logger.debug("Enabling user with user_id: %s", user_id)
        return None
    
    async def delete_user(self, user_id: UUID):
        """
            ลบผู้ใช้ \n
            Delete user
        """
        logger.debug("Deleting user with user_id: %s", user_id)
        return None
    
    async def login(self, user_auth: UserLoginSchema):
        """
            เข้าสู่ระบบ \n
            Sign in
        """
        try:
            logger.debug("User login attempt: %s", user_auth.username)
            user = await self.get_user_by_username(user_auth.username)

            if not user:
                logger.debug("User not found or invalid credentials")
                raise InvalidAuthorizationException(
                    message="บัญชีผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง"
                )
            
            if not verify_password(user_auth.password, user.password_hash):
                logger.debug("Invalid password")
                raise InvalidAuthorizationException(
                    message="บัญชีผู้ใช้งานหรือรหัสผ่านไม่ถูกต้อง"
                )
            user_dict = self._jsonify_user(user)

            logger.debug("User logged in successfully")
            token = TokenService().create_access_token(
                subject=user.id, 
                **user_dict
            )
            return TokenSchema(
                access_token=token, 
                token_type="bearer",
                expires_in=TokenService().access_token_expire_minutes()
            )
        
        except InvalidAuthorizationException as e:
            logger.error("Error logging in: %s", e)
            raise e
        
        except SQLAlchemyError as e:
            logger.error("SQLAlchemy error: %s", e)
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการเข้าสู่ระบบ",
            )
        
        except Exception as e:
            logger.error("Unknown error: %s", e)
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")