from typing import Any
from app.schemas.base import Base

class Result(Base):

    success: bool = False
    trace_id: str | None = None
    message: str | None = None
    data: Any | None = None

    @classmethod
    def model_validate(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()
    