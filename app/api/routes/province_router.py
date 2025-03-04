from fastapi import APIRouter, Depends, Request

from app.schemas.geo_schema import ProvinceCreateSchema, ProvinceDetailSchema, ProvinceSchema, QueryGeoSchema
from app.schemas import Result
from app.services.province_service import ProvinceService
from app.api.deps import get_trace_id, SessionDep
from app.utilities.app_exceptions import APIException, DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException


router = APIRouter(prefix="/province", tags=["province"])

result = Result()

@router.post("/", response_model=Result)
async def create_province(
    req: Request,
    session: SessionDep, 
    data_create: ProvinceCreateSchema
):
    province_service = ProvinceService(session)
    trace_id = get_trace_id(req)

    try:
        result.trace_id = trace_id
        create_result = await province_service.create_province(data_create)
    
        result.data = ProvinceCreateSchema.model_validate(create_result)
        result.success = True

        return result

    except DuplicateResourceException as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id
        )
    except (SQLProcessException, ServerProcessException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )

@router.put("/{code}", response_model=Result)
async def update_province(
    req:Request,
    session: SessionDep, 
    province: ProvinceCreateSchema, 
    code: int
):
    
    province_service = ProvinceService(session)
    trace_id = get_trace_id(req)
    
    try:
        result.trace_id = trace_id
        province_updated = await province_service.update_province(province, code)

        result.success = True
        result.data = ProvinceCreateSchema.model_validate(province_updated)
        
        return result
    
    except ResourceNotFoundException as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id
        )
    except (SQLProcessException, ServerProcessException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )
    
@router.delete("/{code}", response_model=Result)
async def delete_province(
    req: Request,
    session: SessionDep,
    code: int
):
    
    province_service = ProvinceService(session)
    trace_id = get_trace_id(req)
    
    try:
        result.trace_id = trace_id
        delete_result = await province_service.delete_province(code)
        
        result.success = delete_result
        return result
    
    except ResourceNotFoundException as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id
        )
    except (SQLProcessException, ServerProcessException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )
