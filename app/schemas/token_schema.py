from app.schemas.base import Base

class TokenSchema(Base):
    access_token: str
    token_type: str
    expires_in: int

class TokenData(Base):
    username: str | None = None
