import uuid
from sqlalchemy import Boolean, ForeignKey, Integer, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class RolePermission(SQLModel):
    __tablename__ = "RolePermission"

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("Role.id", ondelete="CASCADE"), primary_key=True)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey("Module.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("Permission.id", ondelete="CASCADE"), primary_key=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    __table_args__ = (
        UniqueConstraint("role_id", "module_id", "permission_id", name="role_module_permission_uc"),
    )

    # Relationships
    role = relationship("Role", back_populates="role_permissions")
    module = relationship("Module", back_populates="role_permissions")
    permission = relationship("Permission", back_populates="role_permissions")
