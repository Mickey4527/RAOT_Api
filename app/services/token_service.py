from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi.security import OAuth2PasswordBearer
import jwt

from app.schemas import UserDetailSchema
from app.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


class TokenService:

    def create_jwt_token(self, data: dict) -> str:
        payload = {
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES),
            "aud": settings.JWT_AUDIENCE,
            "data": data
        }
        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt
   
    @staticmethod
    def create_access_token(subject: UserDetailSchema | Any, expires_delta: timedelta) -> str:

        to_encode = subject.model_dump()

        expire = datetime.now(timezone.utc) + expires_delta
        to_encode.update({"exp": expire})

        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return encoded_jwt
    

 