import random
import string
import uuid
from pydantic import Field, EmailStr, field_validator, model_validator
from app.schemas.base import Base

class UserSchema(Base):
    username: str = Field(..., min_length=3, max_length=50)

    @field_validator('username')
    def validate_username(cls, value):
        if '@' in value and not EmailStr.validate(value):
            raise ValueError('Invalid email format')
        return value
    
class UserLoginSchema(UserSchema):
    password: str = Field(..., min_length=5)

class UserDetailSchema(UserSchema):
    firstname: str | None = None
    lastname: str | None = None
    email_primary: EmailStr
    telephone: str
    user_roles: list[str] = []

class UserViewSchema(UserDetailSchema):
    id: uuid.UUID
    is_active: bool

class UserCreateSchema(UserLoginSchema, UserDetailSchema):
    is_auto_generate_password: bool = False
    is_change_password_first_login: bool = False
    email_secondary: EmailStr = None

    @model_validator(mode='before')
    @classmethod
    def generate_auto_password(cls, values):
        if values.get('is_auto_generate_password', False):
            values['password'] = ''.join(random.choices(string.ascii_letters + string.digits, k=5))
        return values
    
    @model_validator(mode='before')
    @classmethod
    def generate_username(cls, values):
        email = values.get("email_primary")
        username = values.get("username")
        if email and not username:
            values["username"] = email.split('@')[0]
        return values

class UserRegisterSchema(UserCreateSchema):
    pass
class UserTokenSchema(UserDetailSchema):
    pass