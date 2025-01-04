from fastapi import APIRouter, Depends, status, HTTPException

from src.routers.deps import SessionDep, get_current_user
from src.schemas import Result, DistrictSchema
from src.services import DistrictService, ProvinceService

router = APIRouter(prefix="/district", tags=["district"], dependencies=[Depends(get_current_user)])


@router.post("/")
async def create_district(session: SessionDep, data_create: DistrictSchema):
    try:

        province = await ProvinceService.get_province(session, data_create.province_id)

        if not province:
            raise HTTPException(
                status_code=404,
                detail=Result.model_validate({
                    "success": False,
                    "message": "Province not found"
                })
            )
        
        new_district = await DistrictService.create_district(session, data_create)
        return Result.model_validate({
            "success": True,
            "message": "District created successfully",
            "data": DistrictSchema.model_validate(new_district)
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )
    
@router.put("/{district_id}")
async def update_district(session: SessionDep, district_id: str, data_update: DistrictSchema):
    try:

        district = await DistrictService.update_district(session, district_id, data_update)

        if not district:
            raise HTTPException(
                status_code=404,
                detail=Result.model_validate({
                    "success": False,
                    "message": "District not found"
                })
            )

        return Result.model_validate({
            "success": True,
            "message": "District updated successfully",
            "data": DistrictSchema.model_validate(district)
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )
    
@router.delete("/{district_id}")
async def delete_district(session: SessionDep, district_id: str):
    try:

        result = await DistrictService.delete_district(session, district_id)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=Result.model_validate({
                    "success": False,
                    "message": "District not found"
                })
            )

        return Result.model_validate({
            "success": True,
            "message": "District deleted successfully"
        })
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )