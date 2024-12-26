from uuid import uuid4
from fastapi import APIRouter
from sqlalchemy.ext.asyncio import AsyncSession
from src.db.main import get_async_engine
from sqlalchemy.sql import select

from src.models import Provinces
from src.schemas import ProvinceSchema, Result, ProvinceBaseSchema

router = APIRouter(prefix="/provinces", tags=["provinces"])

async_session = AsyncSession(get_async_engine(), expire_on_commit=False)


@router.get("/", response_model=Result)
async def get_province_all():
    try:
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
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.get("/{province_id}", response_model=Result)
async def get_province_all(province_id: str):
    try:
        stmp = select(Provinces).where(Provinces.id == province_id)
        result = await async_session.execute(stmp)
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
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.post("/", response_model=Result)
async def create_province(province: ProvinceBaseSchema):
    try:
        new_province = Provinces(
        id=uuid4(),
        name_th=province.name_th,
        name_en=province.name_en,
    )
    
        async with async_session as session:
            async with session.begin():
                session.add(new_province)
                session.commit()
        
        return Result.model_validate({
            "success": True,
            "message": "Province created successfully",
            "data": ProvinceSchema.model_validate(new_province)
        })
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })


@router.put("/{province_id}", response_model=Result)
async def update_province(province_id: str, province: ProvinceBaseSchema):
    try:
        async with async_session as session:
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
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.delete("/{province_id}", response_model=Result)
async def delete_province(province_id: str):
    try:
        async with async_session as session:
            async with session.begin():
                # Fetch the province by ID
                stmp = select(Provinces).where(Provinces.id == province_id)
                result = await session.execute(stmp)
                existing_province = result.scalars().first()

                if not existing_province:
                    return Result.model_validate({
                        "success": False,
                        "error_code": 404,
                        "message": "Province not found"
                    })

                # Delete the province
                await session.delete(existing_province)
                await session.commit()

        return Result.model_validate({
            "success": True,
            "message": "Province deleted successfully"
        })
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })
    

#     from fastapi import APIRouter

# from src.schemas import Result, ProvinceBaseSchema
# from src.services import ProvinceService

# router = APIRouter(prefix="/provinces", tags=["provinces"])


# @router.get("/", response_model=Result)
# async def get_province_all():
#     try:
#         result = await ProvinceService.get_provinces()
#         return result

#     except Exception as e:
#         return Result.model_validate({
#             "success": False,
#             "error_code": 500,
#             "message": str(e)
#         })

# @router.get("/{province_id}", response_model=Result)
# async def get_province(province_id: str):
#     try:
#         result = await ProvinceService.get_province(province_id)
#         return result
    
#     except Exception as e:
#         return Result.model_validate({
#             "success": False,
#             "error_code": 500,
#             "message": str(e)
#         })

# @router.post("/", response_model=Result)
# async def create_province(province: ProvinceBaseSchema):
#     try:
#         result = await ProvinceService.create_province(province)
#         return result
    
#     except Exception as e:
#         return Result.model_validate({
#             "success": False,
#             "error_code": 500,
#             "message": str(e)
#         })


# @router.put("/{province_id}", response_model=Result)
# async def update_province(province_id: str, province: ProvinceBaseSchema):
#     try:
#         result = await ProvinceService.update_province(province_id, province)
#         return result
#     except Exception as e:
#         return Result.model_validate({
#             "success": False,
#             "error_code": 500,
#             "message": str(e)
#         })


# @router.delete("/{province_id}", response_model=Result)
# async def delete_province(province_id: str):
#     try:
#         result = await ProvinceService.delete_province(province_id)
#         return result
#     except Exception as e:
#         return Result.model_validate({
#             "success": False,
#             "error_code": 500,
#             "message": str(e)
#         })
