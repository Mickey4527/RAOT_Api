from typing import Any, Optional
from fastapi import HTTPException
from fastapi.responses import JSONResponse

from src.schemas.base import Result

def raise_http_exception(status_code: int, message: str, headers: dict = None):
    result = Result.model_validate({
        "success": False,
        "error_code": status_code,
        "message": message,
    })

    headers = headers or {}

    raise HTTPException(
        status_code=status_code,
        detail=result.model_dump(),
        headers=headers,
    )

def error_response(status_code: int, message: str):
    result = Result.model_validate({
        "success": False,
        "error_code": status_code,
        "message": message,
    })

    headers = { "X-Status-Code": str(status_code) }

    return JSONResponse(content=result.model_dump(), headers=headers, status_code=status_code)