# import base64
# import binascii

# from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials


# class BasicAuth(AuthenticationBackend):
#     async def authenticate(self, request):

#         if "Authorization" not in request.headers:
#             return None

#         auth = request.headers["Authorization"]

#         try:
            
#             scheme, credentials = auth.split()
#             decoded = base64.b64decode(credentials).decode("ascii")

#         except (ValueError, UnicodeDecodeError, binascii.Error):
#             raise AuthenticationError("Invalid basic auth credentials")

#         username, _, password = decoded.partition(":")
#         return AuthCredentials(["authenticated"]), SimpleUser(username)


import base64
import binascii
import jwt
from jwt import PyJWTError
from starlette.authentication import AuthenticationBackend, AuthenticationError, SimpleUser, AuthCredentials
from app.config import settings

SECRET_KEY = settings.SECRET_KEY
ALGORITHM = settings.ALGORITHM


class JWTAuthBackend(AuthenticationBackend):
    async def authenticate(self, request):

        if "Authorization" not in request.headers:
            return None
        
        auth = request.headers["Authorization"]
        scheme, credentials = auth.split(" ", 1)

        if scheme.lower() == "bearer":
            return await self._authenticate_jwt(credentials)
        
        elif scheme.lower() == "basic":
            return await self._authenticate_basic(credentials)
        
        else:
            raise AuthenticationError("Unsupported authentication scheme")

    async def _authenticate_jwt(self, token: str):
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            username = payload.get("sub")
            roles = payload.get("user_roles", ["authenticated"])

            if not username:
                raise AuthenticationError("Invalid JWT token")
            
            return AuthCredentials(roles), SimpleUser(username), 
        
        except PyJWTError:
            raise AuthenticationError("Invalid JWT token")

    async def _authenticate_basic(self, credentials: str):
        try:
            decoded = base64.b64decode(credentials).decode("ascii")
            username, _, password = decoded.partition(":")

            return AuthCredentials(["authenticated"]), SimpleUser(username)
        
        except (ValueError, UnicodeDecodeError, binascii.Error):
            raise AuthenticationError("Invalid basic auth credentials")
