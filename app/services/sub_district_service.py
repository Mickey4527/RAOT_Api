from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError

from app.models import SubDistrict
from app.schemas import SubDistrictCreateSchema
from app.utilities.app_exceptions import DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException

class SubDistrictService:

    def __init__(self, session: AsyncSession):
        self.session = session


    def _populate_sub_district_fields(
            self,
            sub_district: SubDistrict, 
            data: SubDistrictCreateSchema
        ) -> None:
        
        """
        Populate fields of a SubDistrict instance with data from SubDistrictCreateSchema.
        """

        sub_district.name_th = data.name_th
        sub_district.name_en = data.name_en
        sub_district.code = data.code
        sub_district.district_id = data.district_id
        sub_district.zip_code = data.zip_code 



    async def _get_sub_district_by_code(self, code: int):
        
        try:
            stmp = select(SubDistrict).where(SubDistrict.code == code)
            result = await self.session.execute(stmp)

            return result.scalars().first()
        
        except SQLAlchemyError as e:
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการดึงข้อมูลตำบลจากรหัส"
            )
        
        except Exception as e:

            raise ServerProcessException(
                message="เกิดข้อผิดพลาดที่ไม่รู้จัก"
            )


    async def create_sub_district(self, sub_district: SubDistrictCreateSchema):
        """
        Create sub district data.
        """
        
        try:
            existing_sub_district = await SubDistrictService._get_sub_district_by_code(sub_district.code)
            

            if existing_sub_district:
                raise DuplicateResourceException(
                    message="ตำบลนี้มีอยู่ในระบบแล้ว"
                )
            
            new_sub_district = SubDistrictService._populate_sub_district_fields(SubDistrict(), sub_district)

            self.session.add(new_sub_district)
            await self.session.commit()
            await self.session.refresh(new_sub_district)

            return new_sub_district
        
        except DuplicateResourceException as e:
            raise e
        
        except SQLAlchemyError as e:

            self.session.rollback()
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการสร้างข้อมูลตำบล"
            )
        
        except Exception as e:
            self.session.rollback()
            raise ServerProcessException(
                message="เกิดข้อผิดพลาดที่ไม่รู้จัก"
            )
        
        finally:
            self.session.close()
    

    async def update_sub_district(self, update_sub_district: SubDistrictCreateSchema, code: int):
        """
        Update sub district data.
        """
            
        try:

            existing_sub_district = await self._get_sub_district_by_code(code)

            if not existing_sub_district:
                raise ResourceNotFoundException(
                    message="ไม่พบข้อมูลตำบลที่ต้องการแก้ไข"
                )
            
            new_sub_district = self._populate_sub_district_fields(existing_sub_district, update_sub_district)

            await self.session.commit()
            await self.session.refresh(new_sub_district)

            return existing_sub_district
        
        except ResourceNotFoundException as e:
            raise e
        
        except SQLAlchemyError as e:

            self.session.rollback()
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการแก้ไขข้อมูลตำบล"
            )
        
        except Exception as e:
            self.session.rollback()
            raise ServerProcessException(
                message="เกิดข้อผิดพลาดที่ไม่รู้จัก"
            )
        
        finally:
            self.session.close()
    

    async def delete_sub_district(self, code: int):
        """
        Delete sub district data.
        """

        try:

            existing_sub_district = await SubDistrictService._get_sub_district_by_code(code)

            if not existing_sub_district:
                raise ResourceNotFoundException(
                    message="ไม่พบข้อมูลตำบลที่ต้องการลบ"
                )

            self.session.delete(existing_sub_district)
            await self.session.commit()

            return True
        
        except ResourceNotFoundException as e:
            raise e
        
        except SQLAlchemyError as e:
            
            self.session.rollback()
            raise SQLProcessException(
                event=e,
                message="เกิดข้อผิดพลาดในการลบข้อมูลตำบล"
            )
        
        except Exception as e:
            self.session.rollback()
            raise ServerProcessException(
                message="เกิดข้อผิดพลาดที่ไม่รู้จัก"
            )
