import hashlib
import uuid
from sqlalchemy import Boolean, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import SQLModel

def generate_username_from_email(context):

    email = context.get_current_parameters()["email"]
    return hashlib.sha256(email.encode()).hexdigest()

class UserAccount(SQLModel):
    __tablename__ = "user_account"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True, nullable=False)
    username: Mapped[str] = mapped_column(String(255), nullable=False, unique=True, default=generate_username_from_email)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    telephone: Mapped[str] = mapped_column(String(10), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    profile: Mapped["UserProfile"] = relationship("UserProfile", back_populates="user_account", uselist=False)
    user_roles: Mapped["UserRole"] = relationship("UserRole", back_populates="user", uselist=True)