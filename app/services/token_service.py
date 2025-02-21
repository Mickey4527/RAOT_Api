import jwt
from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi.security import OAuth2PasswordBearer

from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth")


class TokenService:

    def __init__(self):
        self.expires_delta = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
   
    def create_access_token(self, subject: str, **kwargs: Any) -> str:

        payload = {
            "sub": str(subject),
            "iat": datetime.now(timezone.utc),
            "exp": datetime.now(timezone.utc) + self.expires_delta,
            **kwargs
        }

        encoded_jwt = jwt.encode(payload, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        
        return encoded_jwt
    
    def access_token_expire_minutes(self):
        return self.expires_delta.total_seconds()

 