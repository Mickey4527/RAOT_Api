from fastapi import APIRouter, Depends

from src.helpers.validate import is_valid_uuid
from src.routers.deps import SessionDep, get_current_user
from src.schemas import Result, CityWithIdSchema, BaseCitySchema, ProvinceSchema
from src.services import ProvinceService

router = APIRouter(prefix="/province", tags=["province"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=Result)
async def get_province_all(session: SessionDep):
    try:
        result = await ProvinceService.get_provinces(session)
        
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Provinces not found"
            })
        
        return Result.model_validate({
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": [ProvinceSchema.model_validate(province) for province in result]
        })
    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.get("/{province_id}", response_model=Result)
async def get_province_by_id(session: SessionDep, province_id: str):
    try:

        if is_valid_uuid(province_id) == False:
            return Result.model_validate({
                "success": False,
                "error_code": 400,
                "message": "Invalid province id"
            })

        result = await ProvinceService.get_province(session, province_id)
        
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Province not found"
            })
        
        return Result.model_validate({
            "success": True,
            "message": "Province retrieved successfully",
            "data": ProvinceSchema.model_validate(result)
        })

    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.post("/", response_model=Result)
async def create_province(session: SessionDep, data_create: BaseCitySchema):
    try:
        province = await ProvinceService.get_province_by_name(session, data_create.name_th, data_create.name_en)
    
        if province:
            return Result.model_validate({
                "success": False,
                "error_code": 400,
                "message": "Province already exists"
            })
       
        result = await ProvinceService.create_province(session, data_create)
        return Result.model_validate({
            "success": True,
            "message": "Province created successfully",
            "data": result
        })

    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })


@router.put("/{province_id}", response_model=Result)
async def update_province(session: SessionDep, province_id: str, province: BaseCitySchema):
    try:
        if is_valid_uuid(province_id) == False:
            return Result.model_validate({
                "success": False,
                "error_code": 400,
                "message": "Invalid province id"
            })
        
        result = await ProvinceService.update_province(session, province_id, province)
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Province not found"
            })
        
        return Result.model_validate({
            "success": True,
            "message": "Province updated successfully"
        })
    
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
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Province not found"
            })
        
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

@router.get("/{province_id}/list/district", response_model=Result)
async def get_province_by_district(session: SessionDep, province_id: str):
    try:
        result = await ProvinceService.get_districts_by_province(session, province_id)
        
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Province not found"
            })
        
        return Result.model_validate({
            "success": True,
            "message": "Province retrieved successfully",
            "data": [CityWithIdSchema.model_validate(district) for district in result]
        })

    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })