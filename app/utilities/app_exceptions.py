from fastapi import status
from fastapi.responses import ORJSONResponse
from sqlalchemy.exc import CompileError, IntegrityError, SQLAlchemyError

from app.schemas.result import Result

class BaseAppException(Exception):
    """
    Base class for API errors.
    """

    def __init__(self, message: str = None, trace_id: str = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, data: dict = None):
        self.trace_id = trace_id
        self.message = message
        self.data = data
        self.status_code = status_code


class ServerProcessException(BaseAppException):
    """
    A server error.
    """

    def __init__(self, message: str = "Internal server error"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class SQLProcessException(BaseAppException):
    """
    A SQL error.
    """

    def __init__(self, message: str = "SQL error", is_syntax_error: bool = False, is_duplicate_or_foreign_key_error: bool = False, event: SQLAlchemyError = None):
        self.event = event
        self.is_syntax_error = isinstance(event, CompileError)
        self.is_duplicate_or_foreign_key_error = isinstance(event, IntegrityError)
        
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, data={
            "is_syntax_error":  self.is_syntax_error,
            "is_duplicate_or_foreign_key_error": self.is_duplicate_or_foreign_key_error
        })


class ResourceNotFoundException(BaseAppException):
    """
    A resource not found error.
    """

    def __init__(self, message: str = "Resource not found"):
        super().__init__(message, status_code=status.HTTP_404_NOT_FOUND)

class DuplicateResourceException(BaseAppException):
    """
    A duplicate resource error.
    """

    def __init__(self, message: str = "Resource already exists"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)
    
class UnauthorizedException(BaseAppException):
    """
    An unauthorized error.
    """

    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)
        
class RequestErrorHandler(BaseAppException):
    """
    A request error.
    """

    def __init__(self, error: Exception):
        self.error = error
        super().__init__(str(error), status_code=status.HTTP_400_BAD_REQUEST)

class InvalidInputException(BaseAppException):
    """
    An invalid input error.
    """

    def __init__(self, message: str = "Invalid input"):
        super().__init__(message, status_code=status.HTTP_400_BAD_REQUEST)

class InvalidOutputException(BaseAppException):
    """
    An invalid output error.
    """

    def __init__(self, message: str = "Invalid output"):
        super().__init__(message, status_code=status.HTTP_500_INTERNAL_SERVER_ERROR)

class InvalidAuthorizationException(BaseAppException):
    """
    An invalid authorization error.
    """

    def __init__(self, message: str = "Invalid authorization"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)
        
class APIException(BaseAppException):
    """
    A generic API error.
    """

    def __init__(self, message: str = None, trace_id: str = None, status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR, data: dict = None):
        super().__init__(message, trace_id, status_code, data)
        self.result = Result(trace_id=trace_id, message=message, data=data)

    def to_response(self):
        return ORJSONResponse(
            status_code=self.status_code,
            content=self.result.model_dump(),
            media_type="application/json",
        )