from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models import District
from app.schemas import DistrictCreateSchema
from app.utilities.app_exceptions import DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException

class DistrictService:

    def __init__(self, session: AsyncSession):
        self.session = session

    def _populate_district_fields(
            self,
            sub_district: District, 
            data: DistrictCreateSchema
        ) -> None:
        
        """
        Populate fields of a SubDistrict instance with data from SubDistrictCreateSchema.
        """

        sub_district.name_th = data.name_th
        sub_district.name_en = data.name_en
        sub_district.code = data.code
        sub_district.province_id = data.province_id



    async def _get_district_by_code(self, code: int):
        """
        Retrieve district data from the database based on the specified district code.
        """
        
        stmp = select(District).where(District.code == code)
        result = await self.session.execute(stmp)

        return result.scalars().first()
    
    
    async def create_district(self, district: DistrictCreateSchema):
        """
        Create district data.
        """
            
        try:
            existing_district = await self._get_district_by_code(district.code)

            if existing_district:

                raise DuplicateResourceException(
                    message="อำเภอนี้มีอยู่ในระบบแล้ว"
                )
            
            new_district = self._populate_district_fields(District(), district)
            
            self.session.add(new_district)
            await self.session.commit()
            await self.session.refresh(new_district)

            return new_district
        
        except DuplicateResourceException as e:
            raise e
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLProcessException(event=e)
        
        except Exception as e:
            self.session.rollback()
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
    

    async def update_district(self, district: DistrictCreateSchema, code: int):
        """
            Update district data.
        """
            
        try:
        
            existing_district = await DistrictService._get_district_by_code(code)

            if not existing_district:
                raise ResourceNotFoundException(
                    message="ไม่พบข้อมูลอำเภอที่ต้องการแก้ไข"
                )

            DistrictService._populate_district_fields(existing_district, district)

            await self.session.commit()
            await self.session.refresh(existing_district)

            return existing_district
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLProcessException(event=e)
        
        except ResourceNotFoundException as e:
            self.session.rollback()
            raise e
        
        except Exception as e:
            self.session.rollback()
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")
        
    
    async def delete_district(self, code: int):
        """
            Delete district data.
        """

        try:

            existing_district = await DistrictService._get_district_by_code(self, code)

            if not existing_district:
                raise ResourceNotFoundException(
                    message="ไม่พบข้อมูลอำเภอที่ต้องการลบ"
                )

            self.session.delete(existing_district)
            await self.session.commit()

            return True
        
        except SQLAlchemyError as e:
            self.session.rollback()
            raise SQLProcessException(event=e)
        
        except ResourceNotFoundException as e:
            self.session.rollback()
            raise e
        
        except Exception as e:
            self.session.rollback()
            raise ServerProcessException(message="เกิดข้อผิดพลาดที่ไม่รู้จัก")