from sqlalchemy import or_
from sqlalchemy.sql import select
from sqlalchemy.orm import Session
from sqlalchemy.orm import joinedload

from src.models import Province, District
from src.schemas import ProvinceSchema, QueryGeographySchema

class ProvinceService:

    @staticmethod
    async def get_provinces(session: Session, query: QueryGeographySchema):

        if query.code and query.detail:
            stmp = (
                select(Province)
                .where(Province.code == query.code)
                .options(
                    joinedload(Province.districts).joinedload(District.sub_districts)
                )
                .order_by(Province.name_th)
            )
            result = await session.execute(stmp)
            provinces = result.scalars().unique().first()

            return provinces
   
        stmp = select(Province)
        result = await session.execute(stmp)
        provinces = result.scalars().all()

        return provinces


    @staticmethod
    async def create_province(session: Session, province: ProvinceSchema):

        new_province = Province(
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
    async def update_province(session: Session, province: ProvinceSchema, query: QueryGeographySchema):
        stmp = select(Province).where(Province.code == query.code)
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
    async def delete_province(session: Session, query: QueryGeographySchema):
        stmp = select(Province).where(Province.code == query.code)
        result = await session.execute(stmp)
        existing_province = result.scalars().first()

        if not existing_province:
            return False

        session.delete(existing_province)
        await session.commit()

        return True
    