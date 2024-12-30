from fastapi import APIRouter, Depends, status

from src.helpers.error import raise_http_exception
from src.routers.deps import SessionDep, get_current_user
from src.schemas import Result, DistrictCreateSchema, DistrictSchema
from src.services import DistrictService, ProvinceService

router = APIRouter(prefix="/district", tags=["district"], dependencies=[Depends(get_current_user)])
@router.get("/", response_model=Result)
async def get_district_all(session: SessionDep):
    try:
        result = await DistrictService.get_districts(session)
        
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Districts not found"
            })
        
        return Result.model_validate({
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": [DistrictSchema.model_validate(district) for district in result]
        })
    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })

@router.post("/")
async def create_district(session: SessionDep, data_create: DistrictCreateSchema):
    try:

        province = await ProvinceService.get_province(session, data_create.province_id)

        if not province:
            raise raise_http_exception(
                status_code=status.HTTP_404_NOT_FOUND,
                message="Province not found"
            )
        
        new_district = await DistrictService.create_district(session, data_create)
        return Result.model_validate({
            "success": True,
            "message": "District created successfully",
            "data": new_district
        })
    
    except Exception as e:
        raise raise_http_exception(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            message=str(e)
        )
    