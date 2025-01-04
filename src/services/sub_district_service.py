from sqlalchemy import or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.models import SubDistrict
from src.schemas import SubDistrictCreateSchema

class SubDistrictService:
 
    @staticmethod
    async def create_subdistrict(session: AsyncSession, sub_district: SubDistrictCreateSchema):
        
        new_district = SubDistrict(
            name_th=sub_district.name_th,
            name_en=sub_district.name_en,
            province_id=sub_district.province_id,
            code=sub_district.code,
            zipCode=sub_district.zipCode
        )

        session.add(new_district)
        await session.commit()
        await session.refresh(new_district)

        return SubDistrictSchema.model_validate(new_district)
    
    @staticmethod
    async def update_subdistrict(session: AsyncSession, district_id: str, district: DistrictSchema):
        stmp = select(SubDistrict).where(SubDistrict.id == district_id)
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
    async def delete_subdistrict(session: AsyncSession, district_id: str):
        stmp = select(SubDistrict).where(SubDistrict.id == district_id)
        result = await session.execute(stmp)
        existing_district = result.scalars().first()

        if not existing_district:
            return False

        session.delete(existing_district)
        await session.commit()
        await session.refresh(existing_district)

        return True