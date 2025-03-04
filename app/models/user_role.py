import uuid
from sqlalchemy import Integer, String, Boolean, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class UserRole(SQLModel):
    __tablename__ = "UserRole"

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("UserAccount.id", ondelete="CASCADE"), primary_key=True)
    role_id = mapped_column(Integer, ForeignKey("Role.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("user_id", "role_id", name="uq_user_role"),
    )