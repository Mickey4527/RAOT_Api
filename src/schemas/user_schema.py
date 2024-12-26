from .base import BaseSchema

class UserSchema(BaseSchema):
    pass

class UserLoginSchema(UserSchema):
    email: str
    password: str