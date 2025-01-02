from sqlalchemy import or_
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from src.models import Provinces, Districts
from src.schemas import BaseCitySchema, ProvinceSchema

class ProvinceService:

    @staticmethod
    async def get_provinces(session: Session):
        stmp = select(Provinces)
        result = await session.execute(stmp)
        provinces = result.scalars().all()

        return provinces

       
    @staticmethod
    async def get_province(session: Session, province_id: str):
        stmp = select(Provinces).where(Provinces.id == province_id)
        result = await session.execute(stmp)
        province = result.scalars().first()

        return province
    
    @staticmethod
    async def get_province_by_name(session: Session, name_th: str, name_en: str):
        stmp = select(Provinces).filter(or_(Provinces.name_th == name_th, Provinces.name_en == name_en))
        result = await session.execute(stmp)
        province = result.scalars().first()

        return province

    
    @staticmethod
    async def create_province(session: Session, province: ProvinceSchema):

        new_province = Provinces(
            name_th=province.name_th,
            name_en=province.name_en,
            code=province.code,
            geography_id=province.geography_id
        )

        session.add(new_province)
        await session.commit()
        session.refresh(new_province)

        return ProvinceSchema.model_validate(new_province)
            
    @staticmethod
    async def update_province(session: Session, province_id: str, province: ProvinceSchema):
        stmp = select(Provinces).where(Provinces.id == province_id)
        result = await session.execute(stmp)
        existing_province = result.scalars().first()

        if not existing_province:
            return False

        existing_province.name_th = province.name_th
        existing_province.name_en = province.name_en
        existing_province.code = province.code
        existing_province.geography_id = province.geography_id

        await session.commit()

        return True

    @staticmethod
    async def delete_province(session: Session, province_id: str):
        stmp = select(Provinces).where(Provinces.id == province_id)
        result = await session.execute(stmp)
        existing_province = result.scalars().first()

        if not existing_province:
            return False

        session.delete(existing_province)
        await session.commit()

        return True
    
    @staticmethod
    async def get_districts_by_province(session: Session, province_id: int):
        stmp = select(Districts).where(Districts.province_id == province_id)
        result = await session.execute(stmp)
        districts = result.scalars().all()

        return districts