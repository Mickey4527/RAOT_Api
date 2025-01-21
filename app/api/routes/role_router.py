from fastapi import APIRouter, Depends, HTTPException

from app.api.deps import SessionDep, get_current_user
from app.models.role import Role
from app.schemas.role_schema import RoleSchema
from app.schemas.user_schema import UserCreateSchema
from app.services.role_service import RoleService
from app.config import settings
from app.services.user_service import UserService

router = APIRouter(prefix="/role", tags=["role"])

@router.post("/", dependencies=[Depends(get_current_user)])
async def create_role(session: SessionDep, role: RoleSchema):
    try:
        new_role = await RoleService.create_role(session, role)
        return new_role

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )