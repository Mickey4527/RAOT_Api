from typing import Annotated

from sqlmodel import Field, SQLModel, Column, Field, SQLModel, create_engine, Session
import sqlalchemy.dialects.postgresql as pg
from uuid import UUID, uuid4
from datetime import datetime

class UserAccount(SQLModel, table=True):
    id: UUID = Field(default=uuid4(), primary_key=True, unique=True)
    email: str = Field(max_length=255)
    password_hash: str = Field(max_length=255)
    telephone: str = Field(max_length=10)
    user_type: str = Field(max_length=255)
    created_at: datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    updated_at:datetime = Field(sa_column=Column(pg.TIMESTAMP, default=datetime.now))
    last_login: str = Field(max_length=255)

    def __str__(self) -> str:
        return self.email
