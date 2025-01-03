from fastapi import APIRouter, Depends, HTTPException, status

from src.helpers.validate import is_valid_uuid
from src.routers.deps import SessionDep, get_current_user
from src.schemas import Result, BaseCitySchema, DistrictOfProvinceSchema, ProvinceSchema, QuerySchema
from src.services import ProvinceService

router = APIRouter(prefix="/province", tags=["province"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=Result)
async def get_provinces(session: SessionDep, query: QuerySchema = Depends(QuerySchema)):
    try:
        result = await ProvinceService.get_provinces(session, query)
        
        if not result:
            raise HTTPException(
                status_code=404,
                detail=Result.model_validate({
                    "success": False,
                    "message": "Provinces not found"
                })
            )
        
        return Result.model_validate({
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": [ProvinceSchema.model_validate(province) for province in result]
        })
    
    except Exception as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "message": str(e)
            })
        )

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
async def create_province(session: SessionDep, data_create: ProvinceSchema):
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
async def update_province(session: SessionDep, province_id: str, province: ProvinceSchema):
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

from fastapi import HTTPException

@router.get("/{province_id}/list/district", response_model=Result)
async def get_province_by_district(session: SessionDep, province_id: int):
    try:
        # Fetch districts by province_id
        districts = await ProvinceService.get_districts_by_province(session, province_id)

        if not districts:
            raise HTTPException(
                status_code=404, detail="No districts found for the given province."
            )
        
        # Construct the response using DistrictOfProvinceSchema
        district_data = DistrictOfProvinceSchema(
            name_th="Province Name (example)",
            name_en="Province Name (example)",
            districts=[BaseCitySchema.model_validate(district) for district in districts],
        )
        
        return Result.model_validate({
            "success": True,
            "message": "Districts retrieved successfully",
            "data": district_data
        })

    except HTTPException as http_exc:
        return Result.model_validate({
            "success": False,
            "error_code": http_exc.status_code,
            "message": http_exc.detail
        })

    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })
