from pydantic import Field, EmailStr, field_validator
from .base import BaseSchema

class UserSchema(BaseSchema):
    username: str = Field(..., min_length=3, max_length=50)

    @field_validator('username')
    def validate_username(cls, value):
        if '@' in value and not EmailStr.validate(value):
            raise ValueError('Invalid email format')
        return value
    
class UserLoginSchema(UserSchema):
    password: str = Field(..., min_length=5)

class UserDetailSchema(UserSchema):
    email: str
    telephone: str

class UserCreateSchema(UserLoginSchema, UserDetailSchema):
    pass

class UserTokenSchema(UserDetailSchema):
    pass
