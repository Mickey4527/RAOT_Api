from .base import BaseSchema

class UserSchema(BaseSchema):
    username: str = ""
    
class UserLoginSchema(UserSchema):
    password: str

class UserDetailSchema(UserSchema):
    email: str
    telephone: str
    user_type: str

class UserCreateSchema(UserLoginSchema, UserDetailSchema):
    pass
