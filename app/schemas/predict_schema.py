from enum import IntEnum
from app.schemas.base import BaseSchema

from typing import Optional, Literal
from pydantic import Field

class PredictBaseSchema(BaseSchema):
    pass

class SuitabilityPredictSchema(PredictBaseSchema):
    rainfall: float = Field()
    temperature: float = Field()
    humidity: float = Field()
    rainfall_days: int = Field()
    ph_top: Optional[Literal[
        '<4.5', 
        '4.5-5.0', 
        '4.5-5.5',
        '4.5-6.0',
        '5.0-5.5',
        '5.0-6.0',
        '5.0-6.5',
        '5.5-6.5',
        '5.5-7.0',
        '5.5-8.0',
        '6.0-7.0',
        '6.0-8.0']] = Field(None, title="pH ดิน (ด้านบน)")
    
class ProductPredictSchema(PredictBaseSchema):
    province: str 
    district: str
    subdistrict: str
    rubbertype: str
    rubbertreecount: int
    rubberarea: float
    rubbertreeage: int
    fer_top: str
    soilgroup: str
    pH_top: str
    pH_low: str
    rainfall: float
    avg_temperature: float
    rainy_days: int
    avg_humidity: float

class PredictResultSchema(BaseSchema):
    pass

class SuitabilityPredictResultSchema(BaseSchema):
    suitability: int
    probabilities: list