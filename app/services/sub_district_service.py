from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.exc import SQLAlchemyError

from app.models import SubDistrict
from app.schemas import SubDistrictCreateSchema

class SubDistrictService:

    @staticmethod
    def _populate_sub_district_fields(
            sub_district: SubDistrict, data: SubDistrictCreateSchema
        ) -> None:
        
        """
        Populate fields of a SubDistrict instance with data from SubDistrictCreateSchema.
        """

        sub_district.name_th = data.name_th
        sub_district.name_en = data.name_en
        sub_district.code = data.code
        sub_district.district_id = data.district_id
        sub_district.zip_code = data.zip_code 


    @staticmethod
    async def _get_sub_district_by_code(session: AsyncSession, code: int):
        
        stmp = select(SubDistrict).where(SubDistrict.code == code)
        result = await session.execute(stmp)

        return result.scalars().first()
    

    @staticmethod
    async def create_sub_district(session: AsyncSession, sub_district: SubDistrictCreateSchema):
        
        try:
            existing_sub_district = await SubDistrictService._get_sub_district_by_code(session, sub_district.code)
            

            if existing_sub_district:
                return False
            
            new_sub_district = SubDistrictService._populate_sub_district_fields(SubDistrict(), sub_district)

            session.add(new_sub_district)
            await session.commit()
            await session.refresh(new_sub_district)

            return new_sub_district
        
        except SQLAlchemyError as e:

            session.rollback()
            raise e
        
        finally:
            
            session.close()
    

    @staticmethod
    async def update_sub_district(session: AsyncSession, update_sub_district: SubDistrictCreateSchema, code: int):
            
        try:

            existing_sub_district = await SubDistrictService._get_sub_district_by_code(session, code)

            if not existing_sub_district:
                return False
            
            new_sub_district = SubDistrictService._populate_sub_district_fields(existing_sub_district, update_sub_district)

            await session.commit()
            await session.refresh(new_sub_district)

            return existing_sub_district
        
        except SQLAlchemyError as e:

            session.rollback()
            raise e
        
        finally:

            session.close()

    @staticmethod
    async def delete_sub_district(session: AsyncSession, code: int):

        existing_sub_district = await SubDistrictService._get_sub_district_by_code(session, code)

        if not existing_sub_district:
            return False

        session.delete(existing_sub_district)
        await session.commit()

        return True