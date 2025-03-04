import jwt
from fastapi import Request, status
from jwt import PyJWTError
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials

from app.I18n.load_laguage import get_lang_content
from app.core.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM
t = get_lang_content().get("ErrorMessage")


class JWTAuthBackend(AuthenticationBackend):
    
    async def authenticate(self, request: Request):
        if "Authorization" not in request.headers:
            return None
        
        auth = request.headers["Authorization"]
        scheme, credentials = auth.split(" ", 1)

        if scheme.lower() == "bearer":
            return await self._authenticate_jwt(credentials)
        
        else:
            raise AuthenticationError('Invalid authentication scheme')


    async def _authenticate_jwt(self, token: str):
        """
        Authenticate the request using JWT token.\n
        Return the user and roles if the token is valid.\n
        """
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            roles = payload.get("user_roles", ["authenticated"])

            if not username:
                raise AuthenticationError(t.get("InvalidToken"))
            
            return AuthCredentials(roles), SimpleUser(username)
        
        except PyJWTError as e:
            raise AuthenticationError(t.get("InvalidToken"))