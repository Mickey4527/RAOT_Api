from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import SessionDep, get_current_user
from app.schemas import Result, DistrictCreateSchema
from app.services import DistrictService

router = APIRouter(prefix="/district", tags=["district"], dependencies=[Depends(get_current_user)])


@router.post("/")
async def create_district(session: SessionDep, data_create: DistrictCreateSchema):
    try:
        
        new_district = await DistrictService.create_district(session, data_create)

        if not new_district:
            raise HTTPException(
                status_code=400,
                detail=Result.model_validate({
                    "success": False,
                    "message": "District already exists"
                })
            )

        return Result.model_validate({
            "success": True,
            "message": "District created successfully",
            "data": DistrictCreateSchema.model_validate(new_district)
        })
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )
    
@router.put("/{code}")
async def update_district(session: SessionDep, data_update: DistrictCreateSchema, code: int):
    try:
        result = await DistrictService.update_district(session, data_update, code)

        return Result(
            success=True,
            message="District updated successfully",
            data=DistrictCreateSchema.model_validate(result)
        )
  
    except HTTPException as e:
        raise HTTPException(
            status_code=e.status_code,
            detail=Result(
                success=False,
                message=e.detail
            ).model_dump()
        )
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result(
                success=False,
                message=str(e)
            )
        )
    
@router.delete("/{code}")
async def delete_district(session: SessionDep, code: int):
    try:

        result = await DistrictService.delete_district(session, code)

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
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "message": str(e)
            })
        )