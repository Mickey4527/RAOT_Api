from fastapi import APIRouter, Depends, HTTPException, status

from src.routers.deps import SessionDep, get_current_user
from src.schemas import Result, ProvinceDetailSchema, ProvinceSchema, QueryGeographySchema
from src.services import ProvinceService

router = APIRouter(prefix="/province", tags=["province"], dependencies=[Depends(get_current_user)])

@router.get("/", response_model=Result)
async def get_provinces(session: SessionDep, query: QueryGeographySchema = Depends(QueryGeographySchema)):
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
        
        if query.detail and query.code:
            return Result.model_validate({
                "success": True,
                "message": "Provinces retrieved successfully",
                "data": ProvinceDetailSchema.model_validate(result)
            })
        
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
                "error_code": status.HTTP_500_INTERNAL_SERVER_ERROR,
                "message": str(e)
            })
        )

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


@router.put("/{code}", response_model=Result)
async def update_province(session: SessionDep, province: ProvinceSchema,query: QueryGeographySchema):
    try:

        result = await ProvinceService.update_province(session, province, query)
        
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


@router.delete("/{code}", response_model=Result)
async def delete_province(session: SessionDep, query: QueryGeographySchema):
    try:
        result = await ProvinceService.delete_province(session, query)
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

