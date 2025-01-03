from typing import Optional
from .base import BaseSchema

class QuerySchema(BaseSchema):
    limit: int = 10
    offset: int = 0
    search: Optional[str] = None
    order_by: Optional[str] = None
