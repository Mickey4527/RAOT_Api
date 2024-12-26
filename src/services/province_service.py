from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select
from sqlalchemy.orm import Session

from src.models import Provinces
from src.schemas import Result, ProvinceBaseSchema, ProvinceSchema

class ProvinceService:
    @staticmethod
    async def get_provinces(session: Session):
        stmp = select(Provinces)
        result = await session.execute(stmp)
        provinces = result.scalars().all()

        serialized_provinces = [ProvinceSchema.model_validate(province) for province in provinces]
        response = Result.model_validate({
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": serialized_provinces
        })

        return response
        
    @staticmethod
    async def get_province(session: Session, province_id: str):
        stmp = select(Provinces).where(Provinces.id == province_id)
        result = await session.execute(stmp)
        province = result.scalars().first()

        if not province:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Province not found"
            })
            
        return Result.model_validate({
            "success": True,
            "message": "Province retrieved successfully",
            "data": ProvinceSchema.model_validate(province)
        })
    
    @staticmethod
    async def create_province(session: Session, province: ProvinceBaseSchema):
        new_province = Provinces(
            name_th=province.name_th,
            name_en=province.name_en
        )

        async with session.begin():
            session.add(new_province)
            await session.commit()

            return Result.model_validate({
                "success": True,
                "message": "Province created successfully",
                "data": ProvinceSchema.model_validate(new_province)
            })
            
    @staticmethod
    async def update_province(session: Session, province_id: str, province: ProvinceBaseSchema):
        async with session.begin():
            stmp = select(Provinces).where(Provinces.id == province_id)
            result = await session.execute(stmp)
            existing_province = result.scalars().first()

            if not existing_province:
                return Result.model_validate({
                    "success": False,
                    "error_code": 404,
                    "message": "Province not found"
                })

            existing_province.name_th = province.name_th
            existing_province.name_en = province.name_en
            await session.commit()

            return Result.model_validate({
                "success": True,
                "message": "Province updated successfully",
                "data": ProvinceSchema.model_validate(existing_province)
            })

    @staticmethod
    async def delete_province(session: Session, province_id: str):
        async with session.begin():
            stmp = select(Provinces).where(Provinces.id == province_id)
            result = await session.execute(stmp)
            existing_province = result.scalars().first()

            if not existing_province:
                return Result.model_validate({
                    "success": False,
                    "error_code": 404,
                    "message": "Province not found"
                })

            session.delete(existing_province)
            await session.commit()

            return Result.model_validate({
                "success": True,
                "message": "Province deleted successfully"
            })