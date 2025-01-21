from app.models.province import Province
from app.models.district import District
from app.models.subdistrict import SubDistrict
from app.models.user_account import UserAccount
from app.models.base import Base, SQLModel
from app.models.user_profile import UserProfile
from app.models.user_role import UserRole
from app.models.permission import Permission
from app.models.role_permission import RolePermission
from app.models.geography import Geography
from app.models.role import Role
from app.models.private_model.number import NumberTest
from app.models.rubber_farm import RubberFarm
from app.models.soil_geography import SoilGeography
from app.models.weather_geography import WeatherGeography
from app.models.rubber_type import RubberType
from app.models.soil_type import SoilType
from app.models.casbin_rule import CasbinRule

from app.config import settings

__all__ = [
    "Province",
    "District",
    "SubDistrict",
    "UserAccount",
    "Base",
    "SQLModel",
    "UserProfile",
    "UserRole",
    "Permission",
    "RolePermission",
    "Geography",
    "Role",
    "RubberFarm",
    "SoilGeography",
    "WeatherGeography",
    "RubberType",
    "SoilType",
    "CasbinRule"
]

if settings.ENVIRONMENT == "local":
    __all__.append("NumberTest")