from typing import Optional
from pydantic import Field

from app.schemas.base import BaseSchema

class QuerySchema(BaseSchema):
    limit: Optional[int] = Field(100, ge=1, le=1000)
    offset: Optional[int] = Field(0, ge=0)
    search: Optional[str] = None
    order_by: Optional[str] = None
