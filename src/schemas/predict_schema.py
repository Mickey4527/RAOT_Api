from .base import BaseSchema

class PredictSchema(BaseSchema):
    province: int
    district: int
    sub_district: int
    rubber_area: float
    rubber_tree_count: int
    rubber_type: str
    rubber_tree_age: int
    fer_top: str
    soil_group: str
    pH_top: str
    pH_low: str