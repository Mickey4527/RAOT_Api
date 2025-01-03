import uuid

from pydantic import Field
from .base import BaseSchema

class UserSchema(BaseSchema):
    username: str = ""
    
class UserLoginSchema(UserSchema):
    password: str = Field(..., min_length=5)

class UserDetailSchema(UserSchema):
    email: str
    telephone: str

class UserCreateSchema(UserLoginSchema, UserDetailSchema):
    user_role_id: uuid.UUID

class UserTokenSchema(UserDetailSchema):
    pass
