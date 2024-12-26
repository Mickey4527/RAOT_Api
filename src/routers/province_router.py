from fastapi import APIRouter

from src.routers.deps import SessionDep
from src.schemas import Result, ProvinceBaseSchema
from src.services import ProvinceService

router = APIRouter(prefix="/provinces", tags=["provinces"])

@router.get("/", response_model=Result)
async def get_province_all(session: SessionDep):
    try:
        result = await ProvinceService.get_provinces(session)
        return result

    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.get("/{province_id}", response_model=Result)
async def get_province(session: SessionDep, province_id: str):
    try:
        result = await ProvinceService.get_province(session, province_id)
        return result
    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.post("/", response_model=Result)
async def create_province(session: SessionDep, province: ProvinceBaseSchema):
    try:
        result = await ProvinceService.create_province(session, province)
        return result
    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })


@router.put("/{province_id}", response_model=Result)
async def update_province(session: SessionDep, province_id: str, province: ProvinceBaseSchema):
    try:
        result = await ProvinceService.update_province(session, province_id, province)
        return result
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })


@router.delete("/{province_id}", response_model=Result)
async def delete_province(session: SessionDep, province_id: str):
    try:
        result = await ProvinceService.delete_province(session, province_id)
        return result
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })
