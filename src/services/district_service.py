from sqlalchemy.sql import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.models import District
from src.schemas import DistrictSchema

class DistrictService:

    @staticmethod
    async def create_district(session: AsyncSession, district: DistrictSchema):
        
        new_district = District(
            name_th=district.name_th,
            name_en=district.name_en,
            province_id=district.province_id,
            code=district.code
        )

        session.add(new_district)
        await session.commit()
        await session.refresh(new_district)

        return new_district
    
    @staticmethod
    async def update_district(session: AsyncSession, district_id: str, district: DistrictSchema):
        stmp = select(District).where(District.id == district_id)
        result = await session.execute(stmp)
        existing_district = result.scalars().first()

        if not existing_district:
            return False

        existing_district.name_th = district.name_th
        existing_district.name_en = district.name_en
        existing_district.province_id = district.province_id
        existing_district.code = district.code

        await session.commit()
        await session.refresh(existing_district)

        return DistrictSchema.model_validate(existing_district)
    
    @staticmethod
    async def delete_district(session: AsyncSession, district_id: str):
        stmp = select(District).where(District.id == district_id)
        result = await session.execute(stmp)
        existing_district = result.scalars().first()

        if not existing_district:
            return False

        session.delete(existing_district)
        await session.commit()
        await session.refresh(existing_district)

        return True