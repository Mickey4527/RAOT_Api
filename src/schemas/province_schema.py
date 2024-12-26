
from uuid import UUID
from .base import BaseSchema


class ProvinceBaseSchema(BaseSchema):
    name_th: str
    name_en: str


class ProvinceSchema(ProvinceBaseSchema):
    id: UUID

class DistrictSchema(ProvinceBaseSchema):
    id: UUID
    province_id: UUID

class SubDistrictSchema(ProvinceBaseSchema):
    id: UUID
    district_id: UUID
    


