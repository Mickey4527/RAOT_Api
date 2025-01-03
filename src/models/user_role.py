import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import SQLModel

class UserRole(SQLModel):
    __tablename__ = "user_role"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    role_name: Mapped[str] = mapped_column(String(255), nullable=False)
    role_description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role_permission: Mapped["RolePermission"] = relationship("RolePermission", back_populates="role")
    user_account: Mapped["UserAccount"] = relationship("UserAccount", back_populates="user_role")