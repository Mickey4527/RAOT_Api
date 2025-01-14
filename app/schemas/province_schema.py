from typing import Optional, List

from app.schemas.base import BaseSchema
from app.schemas.query_schema import QuerySchema

class BaseGeographySchema(BaseSchema):
    code: int
    name_th: str
    name_en: Optional[str] = None

class ProvinceSchema(BaseGeographySchema):
    geography_id: int

class SubDistrictSchema(BaseGeographySchema):
    zip_code: int
    
class DistrictSchema(BaseGeographySchema):
    sub_districts: Optional[List[SubDistrictSchema]] = None

class ProvinceDetailSchema(ProvinceSchema):
    districts: Optional[List[DistrictSchema]] = None

class DistrictCreateSchema(DistrictSchema):
    province_id: int
class SubDistrictCreateSchema(SubDistrictSchema):
    district_id: int

class QueryGeographySchema(QuerySchema):
    code: Optional[int] = None
    detail: Optional[bool] = False