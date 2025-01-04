from typing import Optional, List
from .base import BaseSchema
from .query_schema import QuerySchema

class BaseGeographySchema(BaseSchema):
    id: Optional[int] = None
    name_th: str
    name_en: Optional[str] = None

class QueryGeographySchema(QuerySchema):
    code: Optional[int] = None
    detail: Optional[bool] = False

class BaseCitySchema(BaseGeographySchema):
    code: int

class ProvinceSchema(BaseCitySchema):
    geography_id: int

class SubDistrictSchema(BaseCitySchema):
    zipCode: int
    
class DistrictSchema(BaseCitySchema):
    sub_districts: Optional[List[SubDistrictSchema]] = None

class ProvinceDetailSchema(ProvinceSchema):
    districts: Optional[List[DistrictSchema]] = None

class SubDistrictCreateSchema(SubDistrictSchema):
    province_id: int

