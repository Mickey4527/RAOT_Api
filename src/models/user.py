from sqlalchemy import String, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

import uuid
from datetime import datetime
from src.models.base import SQLModel

class UserAccount(SQLModel):
    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telephone: Mapped[str] = mapped_column(String(10), nullable=False)
    user_type: Mapped[str] = mapped_column(String(255), nullable=False)
    last_login: Mapped[str] = mapped_column(String(255), nullable=True)

