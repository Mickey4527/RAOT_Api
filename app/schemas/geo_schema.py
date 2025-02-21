from typing import Optional, List

from app.schemas.base import Base, QuerySchema


class BaseGeoSchema(Base):
    code: int
    name: str

class ProvinceSchema(BaseGeoSchema):
    geography_id: int

class SubDistrictSchema(BaseGeoSchema):
    zip_code: int

class DistrictSchema(BaseGeoSchema):
    sub_districts: Optional[List[SubDistrictSchema]] = None

class ProvinceDetailSchema(ProvinceSchema):
    districts: Optional[List[DistrictSchema]] = None

class BaseCreateSchema(Base):
    name_th: str
    name_en: str
    code: int

class ProvinceCreateSchema(BaseCreateSchema):
    geography_id: int

class DistrictCreateSchema(BaseCreateSchema):
    province_id: int

class SubDistrictCreateSchema(BaseCreateSchema):
    district_id: int
    zip_code: int

class QueryGeoSchema(QuerySchema):
    code: Optional[int] = None
    type: Optional[str] = None
    detail: Optional[bool] = False
    order_by: Optional[str] = None
