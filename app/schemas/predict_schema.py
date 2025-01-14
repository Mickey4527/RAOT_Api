from app.schemas.base import BaseSchema

from typing import Optional, Literal
from pydantic import Field, BaseModel

class PredictBaseSchema(BaseSchema):
    pass

class SuitabilityPredictSchema(PredictBaseSchema):
    rain_fall: float = Field()
    temperature: float = Field()
    humidity: float = Field()
    rain_fall_days: int = Field()
    pH_top: Optional[Literal[
        '< 4.5', 
        '4.5 - 5.0', 
        '4.5 - 5.5',
        '4.5 - 6.0',
        '5.0 - 5.5',
        '5.0 - 6.0',
        '5.0 - 6.5',
        '5.5 - 6.5',
        '5.5 - 7.0',
        '5.5 - 8.0',
        '6.0 - 7.0',
        '6.0 - 8.0']] = Field(None, title="pH ดิน (ด้านบน)")
    
class ProductPredictSchema(PredictBaseSchema):
   pass

class PredictResultSchema(BaseModel):
    pass