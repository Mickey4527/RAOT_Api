
from uuid import UUID
from .base import BaseSchema


from uuid import UUID
from .base import BaseSchema


class BaseCitySchema(BaseSchema):
    name_th: str
    name_en: str


class CityWithIdSchema(BaseCitySchema):
    id: UUID


class ProvinceSchema(CityWithIdSchema):
    geography_id: int


class DistrictCreateSchema(BaseCitySchema):
    province_id: UUID


class DistrictSchema(CityWithIdSchema):
    pass
