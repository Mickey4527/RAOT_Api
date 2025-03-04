from fastapi import APIRouter, Depends, Request

from app.schemas import Result
from app.schemas.role_schema import RoleSchema
from app.services.province_service import ProvinceService
from app.api.deps import get_trace_id, SessionDep
from app.services.role_service import RoleService
from app.utilities.app_exceptions import APIException, DuplicateResourceException, ResourceNotFoundException, SQLProcessException, ServerProcessException


router = APIRouter(prefix="/role", tags=["role"])

result = Result()

@router.get("/", response_model=Result)
async def get_role_all(
    req: Request,
    session: SessionDep,
):
    
    role_service = RoleService(session)
    trace_id = get_trace_id(req)

    try:
        result.trace_id = trace_id
        roles = await role_service.get_roles()

        result.data = [RoleSchema.model_validate(province) for province in roles]
     
        
        result.success = True
        return result
    
    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(status_code=e.status_code, message=e.message, trace_id=trace_id, data=e.data)
    