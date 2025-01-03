from typing import Optional
from .base import BaseSchema

class BaseGeographySchema(BaseSchema):
    id: int = 0
    name_th: str
    name_en: Optional[str]

class BaseCitySchema(BaseGeographySchema):
    code: int

class ProvinceSchema(BaseCitySchema):
    geography_id: int

class DistrictSchema(BaseCitySchema):
    province_id: int

class DistrictOfProvinceSchema(BaseCitySchema):
    districts: list[DistrictSchema]
