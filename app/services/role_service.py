from uuid import UUID
import casbin
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import join, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.I18n.load_laguage import get_lang_content
from app.models.role import Role
from app.models.user_role import UserRole
from app.utilities.app_exceptions import ResourceNotFoundException, SQLProcessException, ServerProcessException

class RoleService:
   
    def __init__(self, session: AsyncSession):
        self.session = session
        self.t = get_lang_content().get("ErrorMessage")

    async def get_role_by_name(self, name: str):
        """
            ดึงข้อมูลบทบาทจากฐานข้อมูลตามชื่อบทบาทที่กำหนด \n
            Retrieve role data from the database based on the specified role name.

            #### Parameters
                name: str => ชื่อบทบาทที่ต้องการดึงข้อมูล \n
                The name of the role to retrieve data.

            #### Returns
                Role => ข้อมูลบทบาทจากฐานข้อมูล \n
                Role data from the database.

        """

        try:
            stmp = select(Role).where(Role.name == name)
            result = await self.session.execute(stmp)
            role = result.scalars().first()

            return role
            
        except SQLAlchemyError as e:
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )
        
        except Exception as e:
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        
    async def define_user_role(self, enforcer: casbin.AsyncEnforcer, user_id: str, roles: list):
        """
            กำหนดบทบาทให้กับผู้ใช้ \n
            กำหนดบทบาทให้กับผู้ใช้ในฐานข้อมูลและในนโยบาย Casbin

            Define the roles for a user. \n
            Define the roles for a user in the database and in the Casbin policy.

            #### Parameters
                user_id: str => รหัสผู้ใช้ \n
                The user ID.
                roles: list => รายชื่อบทบาทที่ต้องการกำหนด \n
                The list of roles to be defined.

            #### Returns
                bool => สถานะการกำหนดบทบาท \n
                The status of the role definition.

        """

        try:
            user_roles = []

            for role in roles:
                    role_id = await self.get_role_by_name(role)

                    if not role_id:
                        raise ResourceNotFoundException(
                            message=self.t.get("NotFound"),
                        )

                    new_user_role = UserRole(user_id=user_id, role_id=role_id.id)
                    self.session.add(new_user_role)
                    user_roles.append(new_user_role)

                    await enforcer.add_grouping_policy(str(user_id), role)

            
        except ResourceNotFoundException as e:
            await self.session.rollback()
            raise e
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )

        except Exception as e:
            await self.session.rollback()
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        
    async def create_role(self, role_create: Role):

        try:
            new_role = Role(
                name=role_create.name,
                description=role_create.description
            )

            self.session.add(new_role)
            await self.session.commit()
            await self.session.refresh(new_role)

            return new_role
        
        except SQLAlchemyError as e:
            await self.session.rollback()
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )
        
        except Exception as e:
            await self.session.rollback()
            raise ServerProcessException(message=self.t.get("InternalServerError"))
        
    async def get_roles_by_users(self, users: list):
        """
            ดึงข้อมูลบทบาทจากฐานข้อมูลตามรายชื่อผู้ใช้งานที่กำหนด \n
            Retrieve role data from the database based on the specified user names.

            #### Parameters
                users: list => รายชื่อผู้ใช้งานที่ต้องการดึงข้อมูลบทบาท \n
                The list of user names for which to retrieve role data.

            #### Returns
                dict => ข้อมูลบทบาทจากฐานข้อมูล \n
                Role data from the database.

        """

        try:
            user_ids = [user.id for user in users]

            stmp = select(UserRole.user_id, Role.name).select_from(
                join(UserRole, Role, UserRole.role_id == Role.id)
            ).where(UserRole.user_id.in_(user_ids))

            result = await self.session.execute(stmp)
            user_roles = result.fetchall()

            # เตรียม dictionary โดยให้ทุก user_id มีค่า default เป็น []
            roles_by_user = {str(user_id): [] for user_id in user_ids}

            # เพิ่ม role_name ลงใน dictionary ที่สร้างไว้
            for user_id, role_name in user_roles:
                roles_by_user[str(user_id)].append(role_name)

            return roles_by_user

        except SQLAlchemyError as e:
            raise SQLProcessException(
                event=e,
                message=self.t.get("SQLServerQueryError"),
            )

        except Exception as e:
            raise ServerProcessException(message=self.t.get("InternalServerError"))

    