from .base import BaseSchema

class Token(BaseSchema):
    access_token: str
    token_type: str


class TokenData(BaseSchema):
    username: str | None = None
