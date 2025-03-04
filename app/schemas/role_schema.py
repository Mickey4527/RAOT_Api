from app.schemas.base import Base

class RoleSchema(Base):
    id: int
    name: str
    description: str
