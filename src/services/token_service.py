from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi.security import OAuth2PasswordBearer
from src.config import settings
import jwt

from src.schemas import UserDetailSchema

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


class TokenService:
   
    @staticmethod
    def create_access_token(subject: UserDetailSchema | Any, expires_delta: timedelta) -> str:

        to_encode = subject.model_dump()

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return encoded_jwt
    

 