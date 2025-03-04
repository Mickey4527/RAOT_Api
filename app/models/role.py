import uuid
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class Role(SQLModel):
    __tablename__ = "Role"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)

    users = relationship("UserAccount", secondary="UserRole", back_populates="roles")
    role_permissions = relationship("RolePermission", back_populates="role")
    permissions = relationship("Permission", secondary="RolePermission", back_populates="roles")
