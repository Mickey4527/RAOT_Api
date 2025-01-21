import casbin
from starlette.authentication import BaseUser
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN
from starlette.types import ASGIApp, Receive, Scope, Send

from app.db.main import get_casbin_enforcer


class CasbinMiddleware:
    """
    Middleware for Casbin
    """

    def __init__(self, app: ASGIApp) -> None:
        """
        Configure Casbin Middleware

        :param app: Retain for ASGI.
        """
        self.app = app
        self.enforcer = None  # Defer Casbin enforcer loading to __call__

    async def __call__(self, scope: Scope, receive: Receive, send: Send) -> None:
        if scope["type"] not in ("http", "websocket"):
            await self.app(scope, receive, send)
            return

        if await self._enforce(scope, receive) or scope["method"] == "OPTIONS":
            await self.app(scope, receive, send)

        else:
            response = JSONResponse(
                status_code=HTTP_403_FORBIDDEN,
                content="Forbidden"
            )
            await response(scope, receive, send)

    async def _enforce(self, scope: Scope, receive: Receive) -> bool:
        """
        Enforce a request.

        :param scope: ASGI request scope.
        :param receive: ASGI receive function.
        :return: Enforce Result (True/False).
        """
        request = Request(scope, receive)
        path = request.url.path
        method = request.method

        if 'user' not in scope:
            raise RuntimeError("Casbin Middleware must work with an Authentication Middleware")

        assert isinstance(request.user, BaseUser)
        user = request.user.display_name if request.user.is_authenticated else 'anonymous'

        if not self.enforcer:
            self.enforcer = await get_casbin_enforcer()

        return self.enforcer.enforce(user, path, method)