from fastapi import APIRouter, Depends, Request

from app.schemas.geo_schema import ProvinceCreateSchema, ProvinceDetailSchema, ProvinceSchema, QueryGeoSchema
from app.schemas import Result
from app.services.province_service import ProvinceService
from app.api.deps import get_trace_id, SessionDep
from app.utilities.app_exceptions import APIException, DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException


router = APIRouter(prefix="/common", tags=["common"])

result = Result()

@router.get("/province", response_model=Result)
async def get_provinces(
    req: Request,
    session: SessionDep,
    query: QueryGeoSchema = Depends(QueryGeoSchema)
):
    
    province_service = ProvinceService(session)
    trace_id = get_trace_id(req)

    try:
        result.trace_id = trace_id
        provinces = await province_service.get_provinces(query = query)

        if query.detail and query.code:
            result.data = [ProvinceDetailSchema.model_validate(province) for province in provinces]
        else:
            result.data = [ProvinceSchema.model_validate(province) for province in provinces]
        
        result.success = True
        return result
    
    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(status_code=e.status_code, message=e.message, trace_id=trace_id, data=e.data)
    