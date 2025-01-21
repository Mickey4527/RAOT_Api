from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.authentication import AuthenticationMiddleware

from app.config import settings
from app.api.main import api_router
from app.middleware import CasbinMiddleware
from app.test_rbca import JWTAuthBackend


def get_app() -> FastAPI:
    app = FastAPI(
        title=settings.PROJECT_NAME,
        openapi_url=f"{settings.API_V1_STR}/openapi.json",
    )

    app.include_router(api_router, prefix=settings.API_V1_STR)
    
    if settings.all_cors_origins:
        app.add_middleware(
            CORSMiddleware,
            allow_origins=settings.all_cors_origins,
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )

    app.add_middleware(CasbinMiddleware)
    app.add_middleware(AuthenticationMiddleware, backend=JWTAuthBackend())

    
    return app

app = get_app()