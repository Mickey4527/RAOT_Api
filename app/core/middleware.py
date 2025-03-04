import logging

from fastapi import Request, status
from starlette.requests import Request
from starlette.types import ASGIApp, Receive, Scope, Send
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.authentication import BaseUser
from starlette.types import ASGIApp, Receive, Scope, Send

from app.core.casbin import get_casbin_enforcer
from app.utilities.app_exceptions import APIException
from app.utilities.app_utilities import generate_trace_id
from app.utilities.trace_config import TraceIDFilter

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
            response = APIException(
                status_code=status.HTTP_403_FORBIDDEN,
                message="Permission denied",
            ).to_response()
            
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

class TraceIDMiddleware(BaseHTTPMiddleware):
    """
    Middleware to add a trace ID to the request and response.
    """

    async def dispatch(self, request: Request, call_next):
        """
        Add a trace ID to the request and response.
        """
        
        trace_id = generate_trace_id()
        request.state.trace_id = trace_id

        for handler in logging.getLogger().handlers:
            for filter in handler.filters:
                if isinstance(filter, TraceIDFilter):
                    filter.trace_id = trace_id
        
        response = await call_next(request)
        response.headers["X-Trace-ID"] = trace_id

        return response
    
