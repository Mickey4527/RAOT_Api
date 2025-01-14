import uuid
from sqlalchemy import String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class UserRole(SQLModel):
    __tablename__ = "user_role"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("role.id"), nullable=False)
    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user_account.id"), nullable=False)

    # Relationships
    role: Mapped["Role"] = relationship("Role", back_populates="user_roles")
    user: Mapped["UserAccount"] = relationship("UserAccount", back_populates="user_roles")
    