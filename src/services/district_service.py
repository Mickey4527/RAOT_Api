from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from src.models import District
from src.schemas import DistrictSchema

class DistrictService:

    @staticmethod
    async def get_districts(session: Session):
        stmp = select(District)
        result = await session.execute(stmp)
        districts = result.scalars().all()

        return districts

       
    @staticmethod
    async def get_district(session: Session, district_id: str):
        stmp = select(District).where(District.id == district_id)
        result = await session.execute(stmp)
        district = result.scalars().first()

        return district
    
    @staticmethod
    async def get_district_by_province(session: Session, province_id: str):
        stmp = select(District).where(District.province_id == province_id)
        result = await session.execute(stmp)
        districts = result.scalars().all()

        return districts
    
    @staticmethod
    async def create_district(session: Session, district: DistrictSchema):
        
        new_district = District(
            name_th=district.name_th,
            name_en=district.name_en,
            province_id=district.province_id,
            code=district.code
        )

        session.add(new_district)
        await session.commit()

        return DistrictSchema.model_validate(new_district)
    
    