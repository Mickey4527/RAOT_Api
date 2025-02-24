from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from app.core.auth import JWTAuthBackend
from app.core.config import settings
from app.api.main import get_api_router
from app.core.middleware import CasbinMiddleware, TraceIDMiddleware
from app.utilities.app_config import auth_exception_handler, exception_handler
from app.utilities.app_exceptions import APIException

def get_app() -> FastAPI:
    
    """
    Return the FastAPI application
    """

    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
        default_response_class=ORJSONResponse,
        debug=settings.DEBUG,
    )

    app.add_exception_handler(APIException, exception_handler)

    app.add_middleware(TraceIDMiddleware)  # Logging Trace ID
    app.add_middleware(CasbinMiddleware)  # Authorization Middleware
    app.add_middleware(AuthenticationMiddleware,
                       backend=JWTAuthBackend(), 
                       on_error=auth_exception_handler)
    

    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.all_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.include_router(get_api_router(), prefix=settings.API_V1_STR)

    return app

app = get_app()
print("✅ FastAPI app created successfully!")
