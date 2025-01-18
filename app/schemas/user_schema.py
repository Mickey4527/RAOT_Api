import random
import string
from pydantic import Field, EmailStr, field_validator, model_validator
from app.schemas.base import BaseSchema

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
    first_name: str
    last_name: str = ''
    email_primary: EmailStr
    email_secondary: EmailStr = None
    telephone: str

class UserCreateSchema(UserLoginSchema, UserDetailSchema):
    is_auto_generate_password: bool = False
    is_change_password_first_login: bool = False

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
        if email:
            values["username"] = email.split('@')[0]
        return values

class UserRegisterSchema(UserCreateSchema):
    pass
class UserTokenSchema(UserDetailSchema):
    pass
