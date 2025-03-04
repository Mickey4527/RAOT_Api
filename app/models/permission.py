import uuid
from sqlalchemy import ForeignKey, Integer, String, Boolean
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class Permission(SQLModel):
    __tablename__ = "Permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    url_action: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)
    module_id: Mapped[int] = mapped_column(Integer, ForeignKey("Module.id"), nullable=False)

    module = relationship("Module", back_populates="permissions")  # type: ignore
    role_permissions = relationship("RolePermission", back_populates="permission")
    roles = relationship("Role", secondary="RolePermission", back_populates="permissions")
