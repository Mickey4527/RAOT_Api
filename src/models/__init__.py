from .province import Province
from .district import District
from .subdistrict import SubDistrict
from .user_account import UserAccount
from .base import Base, SQLModel
from .user_profile import UserProfile
from .user_role import UserRole
from .permission import Permission
from .role_permission import RolePermission
from .geography import Geography
from .resource import Resource
from .role import Role
from .private_model.number import NumberTest
from .rubber_farm import RubberFarm
from .soil_geography import SoilGeography
from .weather_geography import WeatherGeography
from .rubber_type import RubberType
from .soil_type import SoilType

from src.config import settings

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
    "Resource",
    "Role"
]

if settings.ENVIRONMENT == "local":
    __all__.append("NumberTest")