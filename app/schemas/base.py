from typing import Optional
from pydantic import BaseModel, ConfigDict, Field


class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class QuerySchema(Base):
    limit: Optional[int] = Field(100, ge=1, le=1000)
    offset: Optional[int] = Field(0, ge=0)
    search: Optional[str] = None
    order_by_desc: bool = False