from sqlalchemy.sql import select, desc
from sqlalchemy.orm import joinedload
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Province, District
from app.schemas import ProvinceSchema, QueryGeographySchema

class ProvinceService:

    @staticmethod
    def _populate_sub_district_fields(
            province: Province, data: ProvinceSchema
        ) -> None:
        
        """
        Populate fields of a Province instance with data from ProvinceSchema.
        """
        province.name_th = data.name_th
        province.name_en = data.name_en
        province.code = data.code
        province.geography_id = data.geography_id



    @staticmethod
    async def get_provinces(session: AsyncSession, query: QueryGeographySchema):

        if query.code and query.detail:
            stmp = (
                select(Province)
                .where(Province.code == query.code)
                .options(
                    joinedload(Province.districts).joinedload(District.sub_districts)
                )
                .order_by(query.order_by)
            )
            result = await session.execute(stmp)
            provinces = result.scalars().first()

            return provinces
   
        stmp = select(Province).order_by(Province.name_th)
        result = await session.execute(stmp)
        provinces = result.scalars().all()

        return provinces


    @staticmethod
    async def _get_province_by_code(session: AsyncSession, code: int):
        
        stmp = select(Province).where(Province.code == code)
        result = await session.execute(stmp)

        return result.scalars().first()
    

    @staticmethod
    async def create_province(session: AsyncSession, province: ProvinceSchema):
            
        try:

            existing_province = await ProvinceService._get_province_by_code(session, province.code)

            if existing_province:
                return False

            new_province = ProvinceService._populate_sub_district_fields(Province(), province)

            session.add(new_province)
            await session.commit()
            session.refresh(new_province)

            return new_province
        
        except Exception as e:

            session.rollback()
            raise e
        
        finally:
            
            session.close()
            
    @staticmethod
    async def update_province(session: AsyncSession, province: ProvinceSchema, code: int):
            
        try:
            existing_province = await ProvinceService._get_province_by_code(session, code)

            if not existing_province:
                return False

            ProvinceService._populate_sub_district_fields(existing_province, province)
            await session.commit()
            await session.refresh(existing_province)

            return True
        
        except Exception as e:
            
            session.rollback()
            raise e
        
        finally:
            
            session.close()
        

    @staticmethod
    async def delete_province(session: AsyncSession, code: int):

        existing_province = await ProvinceService._get_province_by_code(session, code)

        if not existing_province:
            return False

        session.delete(existing_province)
        await session.commit()

        return True
    