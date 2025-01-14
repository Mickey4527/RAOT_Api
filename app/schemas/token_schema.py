from app.schemas.base import BaseSchema

class Token(BaseSchema):
    access_token: str
    refresh_token: str | None = None
    token_type: str
    expires_in: int
    refresh_expires_in: int | None = None


class TokenData(BaseSchema):
    username: str | None = None
