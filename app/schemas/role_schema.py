from pydantic import Field
from app.schemas.base import BaseSchema

class RoleSchema(BaseSchema):
    name: str = Field(..., min_length=3, max_length=50)
    description: str = ''