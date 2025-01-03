from fastapi import APIRouter, Depends

from src.helpers.validate import is_valid_uuid
from src.routers.deps import SessionDep, get_current_user
from src.schemas import Result, BaseGeographySchema
from src.services.geography_service import GeographyService

router = APIRouter(prefix="/geography", tags=["geography"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=Result)
async def get_geography_all(session: SessionDep):
    # try:
        result = await GeographyService.get_geographys(session)
        
        if not result:
            return Result.model_validate({
                "success": False,
                "error_code": 404,
                "message": "Provinces not found"
            })
        
        return Result.model_validate({
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": [BaseGeographySchema.model_validate(geography) for geography in result]
        })
    
    # except Exception as e:
    #     return Result.model_validate({
    #         "success": False,
    #         "error_code": 500,
    #         "message": str(e)
    #     })

@router.post("/", response_model=Result)
async def create_geography(geography: BaseGeographySchema, session: SessionDep):
    try:
        result = await GeographyService.create_geography(session, geography)
        
        return Result.model_validate({
            "success": True,
            "message": "Province created successfully",
            "data": BaseGeographySchema.model_validate(result)
        })
    
    except Exception as e:
        return Result.model_validate({
            "success": False,
            "error_code": 500,
            "message": str(e)
        })