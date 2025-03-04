import uuid
from sqlalchemy import Integer, String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class Permission(SQLModel):
    __tablename__ = "Permission"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    description: Mapped[str] = mapped_column(String(255), nullable=True)
    api_endpoint: Mapped[str] = mapped_column(String(255), nullable=False)

    roles = relationship("Role", secondary="RolePermission", back_populates="permissions")
