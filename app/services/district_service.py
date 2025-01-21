from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import SQLAlchemyError
from fastapi import HTTPException, status

from app.models import District
from app.schemas import DistrictCreateSchema

class DistrictService:

    @staticmethod
    def _populate_district_fields(
            sub_district: District, data: DistrictCreateSchema
        ) -> None:
        
        """
        Populate fields of a SubDistrict instance with data from SubDistrictCreateSchema.
        """

        sub_district.name_th = data.name_th
        sub_district.name_en = data.name_en
        sub_district.code = data.code
        sub_district.province_id = data.province_id


    @staticmethod
    async def _get_district_by_code(session: AsyncSession, code: int):
        
        stmp = select(District).where(District.code == code)
        result = await session.execute(stmp)

        return result.scalars().first()
    
    
    @staticmethod
    async def create_district(session: AsyncSession, district: DistrictCreateSchema):
            
        try:
            existing_district = await DistrictService._get_district_by_code(session, district.code)

            if existing_district:
                return False
            
            new_district = DistrictService._populate_district_fields(District(), district)
            
            session.add(new_district)
            await session.commit()
            await session.refresh(new_district)

            return new_district
        
        except SQLAlchemyError as e:

            session.rollback()
            raise e
    

    @staticmethod
    async def update_district(session: AsyncSession, district: DistrictCreateSchema, code: int):
            
        try:
        
            existing_district = await DistrictService._get_district_by_code(session, code)

            if not existing_district:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="ไม่พบข้อมูลอำเภอ"
                )

            DistrictService._populate_district_fields(existing_district, district)

            await session.commit()
            await session.refresh(existing_district)

            return existing_district
        
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        
    
    @staticmethod
    async def delete_district(session: AsyncSession, code: int):

        existing_district = await DistrictService._get_district_by_code(session, code)

        if not existing_district:
            return False

        session.delete(existing_district)
        await session.commit()

        return True