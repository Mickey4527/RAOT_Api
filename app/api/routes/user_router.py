from typing import Annotated
from fastapi import APIRouter, Depends, Request
from fastapi.security import OAuth2PasswordRequestForm

from app.schemas.base import QuerySchema
from app.schemas.result import Result
from app.schemas.user_schema import UserCreateSchema, UserViewSchema
from app.services.user_service import UserService
from app.api.deps import get_trace_id, SessionDep, enforcerDep
from app.utilities.app_exceptions import APIException, DuplicateResourceException, InvalidAuthorizationException, InvalidOutputException, ResourceNotFoundException, SQLProcessException, ServerProcessException


router = APIRouter(prefix="/user", tags=["users"])

result = Result()

@router.get("/", response_model=Result)
async def get_user_all(
    req: Request,
    enforcer: enforcerDep,
    session: SessionDep,
    query: QuerySchema = Depends(QuerySchema)
):
    
    user_service = UserService(session)
    trace_id = get_trace_id(req)

    try:
        result.trace_id = trace_id
        users = await user_service.get_users(query = query)

        users = [
                user_service._jsonify_view_user(user)
                for user in users
            ]
        
        result.data = {
            "users": [UserViewSchema.model_validate(user) for user in users],
            "total": len(users),
            "limit": query.limit,
            "offset": query.offset
        }
        
        result.success = True

        return result

    except InvalidOutputException as e:
        raise APIException(
            message=e.message,
            trace_id=trace_id
        )

    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(
            status_code=e.status_code, 
            message=e.message, 
            trace_id=trace_id, 
            data=e.data
        )
    
@router.post("/add", response_model=Result)
async def add_user(
    req: Request,
    session: SessionDep, 
    enforcer: enforcerDep, 
    user_create: UserCreateSchema):
    
    user_service = UserService(session)
    trace_id = get_trace_id(req)

    try:

        await user_service.create_user(enforcer=enforcer, user_create=user_create)

        result.trace_id = trace_id
        result.success = True
        
        return result
    
    except (DuplicateResourceException, ResourceNotFoundException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )
    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )
    
@router.delete("/delete/{user_id}", response_model=Result)
async def delete_user(
    req: Request,
    session: SessionDep,
    enforcer: enforcerDep,
    user_id: str):
    
    user_service = UserService(session)
    trace_id = get_trace_id(req)

    try:
        # await user_service.delete_user(enforcer=enforcer, user_id=user_id)

        result.trace_id = trace_id
        result.success = True

        return result
    
    except (ResourceNotFoundException, InvalidAuthorizationException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )
    except (ServerProcessException, SQLProcessException) as e:
        raise APIException(
            status_code=e.status_code,
            message=e.message,
            trace_id=trace_id,
            data=e.data
        )
    

@router.post("/login/auth")
async def login_for_access_token(
    session: SessionDep,
    req: Request,
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):

    user_service = UserService(session)
    trace_id = get_trace_id(req)

    try:
        token = await user_service.login(form_data)
        return token
    
    except (InvalidAuthorizationException, ServerProcessException, SQLProcessException) as e:
        raise APIException(
            status_code=e.status_code,
            trace_id=trace_id,
            message=e.message
        )
    