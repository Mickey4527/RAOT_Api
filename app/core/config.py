from typing import Annotated, Any, Literal
from pydantic import (
    AnyUrl, 
    BeforeValidator, 
    HttpUrl, 
    PostgresDsn, 
    computed_field
    )
from pydantic_settings import BaseSettings, SettingsConfigDict

def parse_cors(v: Any) -> list[str] | str:
        """
        Parse the CORS origins from the environment variable
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, list | str):
            return v
        raise ValueError(v)

class Settings(BaseSettings):
    """
    Settings class for the FastAPI application
    """

    # Environment variable
    ENVIRONMENT: Literal["local", "staging", "production", "datasci_test"] = "local"

    # Config for the API
    PROJECT_NAME: str
    SENTRY_DSN: HttpUrl | None = None
    DEBUG: bool = False
    API_V1_STR: str = "/api/v1"

    # Config for the database
    POSTGRES_SERVER: str
    POSTGRES_PORT: int = 5432
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str = ""
    POSTGRES_DB: str = ""
    PREDICT_API_URL: str

    # Config for the first superuser (info: superuser is a user with all permissions)
    FIRST_SUPERUSER: str
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str
    FIRST_SUPERUSER_PHONE: str

    # Config for the first superuser role
    FIRST_SUPERUSER_ROLE: str
    FIRST_SUPERUSER_ROLE_DESCRIPTION: str

    # Config for the JWT
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    JWT_SUBJECT: str
    EXLUDED_PATHS: list[str] = []

    # Config for the CSV files import
    CSV_FILES_IMPORT: list[dict] = []

    # Config for the frontend host
    FRONTEND_HOST: str = "http://localhost:3000"

    # Config for the CORS origins
    BACKEND_CORS_ORIGINS: Annotated[
        list[AnyUrl] | str, BeforeValidator(parse_cors)
    ] = []

    # Config for the model
    model_config = SettingsConfigDict(
        env_file = ".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def all_cors_origins(self) -> list[str]:
        return [str(origin).rstrip("/") for origin in self.BACKEND_CORS_ORIGINS] + [
            self.FRONTEND_HOST
        ]
    
    # Computed field
    @computed_field
    def SQLALCHEMY_DATABASE_URI(self) -> PostgresDsn:
        """
        Return the SQLAlchemy database URI
        """
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_SERVER,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DB,
        )
    
settings = Settings()