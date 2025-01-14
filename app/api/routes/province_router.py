from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.exc import SQLAlchemyError

from app.api.deps import get_current_user, SessionDep
from app.schemas import Result, ProvinceDetailSchema, ProvinceSchema, QueryGeographySchema
from app.services import ProvinceService

router = APIRouter(prefix="/province", tags=["province"])

@router.get("/", response_model=Result)
async def get_provinces(session: SessionDep, query: QueryGeographySchema = Depends(QueryGeographySchema)):
    try:
        result = await ProvinceService.get_provinces(session, query)
        
        if not result:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail={
                    "success": False,
                    "error_code": status.HTTP_404_NOT_FOUND,
                    "message": "Provinces not found"
                }
            )
        
        if query.detail and query.code:
            return {
                "success": True,
                "message": "Provinces retrieved successfully",
                "data": ProvinceDetailSchema.model_validate(result)
            }
        
        return {
            "success": True,
            "message": "Provinces retrieved successfully",
            "data": [ProvinceSchema.model_validate(province) for province in result]
        }
    
    except SQLAlchemyError as e:
        return HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            }
        )

@router.post("/", response_model=Result, dependencies=[Depends(get_current_user)])
async def create_province(session: SessionDep, data_create: ProvinceSchema):
    try:
        result = await ProvinceService.create_province(session, data_create)

        if not result:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=Result.model_validate({
                    "success": False,
                    "error_code": 400,
                    "message": "Province already exists"
                })
            )
        
        return Result.model_validate({
            "success": True,
            "message": "Province created successfully",
            "data": ProvinceSchema.model_validate(result)
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

@router.put("/{code}", response_model=Result, dependencies=[Depends(get_current_user)])
async def update_province(session: SessionDep, province: ProvinceSchema, code: int):
    try:

        result = await ProvinceService.update_province(session, province, code)
        
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
    
    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=Result.model_validate({
                "success": False,
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )


@router.delete("/{code}", response_model=Result, dependencies=[Depends(get_current_user)])
async def delete_province(session: SessionDep, code: int):
    try:
        result = await ProvinceService.delete_province(session, code)

        if not result:
            raise HTTPException(
                status_code=404,
                detail=Result.model_validate({
                    "success": False,
                    "error_code": 404,
                    "message": "Province not found"
                })
            )
        
        return Result.model_validate({
            "success": True,
            "message": "Province deleted successfully"
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
