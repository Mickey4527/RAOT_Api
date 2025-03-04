from fastapi import Request, status
from fastapi.responses import ORJSONResponse
from app.utilities.app_exceptions import APIException

def exception_handler(_: Request, exc: APIException) -> ORJSONResponse:
    return exc.to_response()

def auth_exception_handler(_: Request, exc: Exception) -> ORJSONResponse:
    return APIException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        message=str(exc)
    ).to_response()