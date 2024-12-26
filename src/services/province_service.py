from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import select

from src.db.models import Provinces
from src.schemas import Result, ProvinceBaseSchema, ProvinceSchema
from src.db.main import get_async_engine

class ProvinceService:
    async_session = AsyncSession(get_async_engine(), expire_on_commit=False)

    @staticmethod
    async def get_provinces():
        stmp = select(Provinces)
        result = await async_session.execute(stmp)
        provinces = result.scalars().all()

        serialized_provinces = [ProvinceSchema.model_validate(province) for province in provinces]
        response = Result.model_validate({
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": serialized_provinces
        })

        return response
        
    @staticmethod
    async def get_province(province_id: str):
        async with AsyncSession() as session:
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
    async def create_province(province: ProvinceBaseSchema):
        async with AsyncSession() as session:
            async with session.begin():
                new_province = Provinces(
                    name_th=province.name_th,
                    name_en=province.name_en
                )

                session.add(new_province)
                await session.commit()

                return Result.model_validate({
                    "success": True,
                    "message": "Province created successfully",
                    "data": ProvinceSchema.model_validate(new_province)
                })
            
    @staticmethod
    async def update_province(province_id: str, province: ProvinceBaseSchema):
        async with AsyncSession() as session:
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

                session.add(existing_province)
                await session.commit()

                return Result.model_validate({
                    "success": True,
                    "message": "Province updated successfully",
                    "data": ProvinceSchema.model_validate(existing_province)
                })

    @staticmethod
    async def delete_province(province_id: str):
        async with AsyncSession() as session:
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

                await session.delete(existing_province)
                await session.commit()

                return Result.model_validate({
                    "success": True,
                    "message": "Province deleted successfully"
                })
