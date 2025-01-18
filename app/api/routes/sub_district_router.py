from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import SessionDep, get_current_user
from app.schemas import Result, SubDistrictCreateSchema
from app.services import SubDistrictService

router = APIRouter(prefix="/sub_district", tags=["sub_district"], dependencies=[Depends(get_current_user)])

@router.post("/")
async def create_sub_district(session: SessionDep, data_create: SubDistrictCreateSchema):
    try:
        
        new_sub_district = await SubDistrictService.create_sub_district(session, data_create)

        if not new_sub_district:
            raise HTTPException(
                status_code=400,
                detail=Result.model_validate({
                    "success": False,
                    "message": "Sub district already exists"
                })
            )

        return Result.model_validate({
            "success": True,
            "message": "District created successfully",
            "data": SubDistrictCreateSchema.model_validate(new_sub_district)
        })
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "message": str(e)
            })
        )
    
@router.put("/{code}")
async def update_district(session: SessionDep, data_update: SubDistrictCreateSchema, code: int):
    try:

        result = await SubDistrictService.update_sub_district(session, data_update, code)

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
            "message": "District updated successfully",
            "data": SubDistrictCreateSchema.model_validate(result)
        })
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "message": str(e)
            })
        )
    
@router.delete("/{code}")
async def delete_district(session: SessionDep, code: int):
    try:

        result = await SubDistrictService.delete_sub_district(session, code)

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