from pydantic import BaseModel, ConfigDict
from typing import Any, Optional, Union
from datetime import datetime

class Base(BaseModel):
    model_config = ConfigDict(from_attributes=True)

class Result(BaseModel):
    success: bool = False
    message: str
    data: Optional[Any] = None

    @classmethod
    def model_validate(cls, data: dict):
        return cls(**data)

    def to_dict(self):
        return self.model_dump()

class BaseSchema(Base):
    pass
