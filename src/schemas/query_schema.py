from typing import Optional
from .base import BaseSchema

class QuerySchema(BaseSchema):
    limit: Optional[int] = None
    offset: Optional[int] = None
    search: Optional[str] = None
    order_by: Optional[str] = None
