from enum import IntEnum
from app.schemas.base import Base

from typing import Optional, Literal
from pydantic import Field

class PredictBaseSchema(Base):
    pass

class SuitablePredictSchema(PredictBaseSchema):
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
    province: int
    district: int
    subdistrict: int
    rubber_type: str
    rubber_tree_count: int
    rubber_area: float
    rubber_tree_age: int
    fer_top: str
    soil_group: str
    ph_top: str
    ph_low: str
    rainfall: float
    temperature: float
    rainfall_days: int
    humidity: float

class PredictResultSchema(Base):
    pass

class SuitabilityPredictResultSchema(Base):
    suitability: int
    probabilities: list