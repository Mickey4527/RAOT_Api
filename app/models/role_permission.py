import uuid
from sqlalchemy import ForeignKey, Integer, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class RolePermission(SQLModel):
    __tablename__ = "RolePermission"

    role_id: Mapped[int] = mapped_column(Integer, ForeignKey("Role.id", ondelete="CASCADE"), primary_key=True)
    permission_id: Mapped[int] = mapped_column(Integer, ForeignKey("Permission.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        UniqueConstraint("role_id", "permission_id", name="uq_role_permission"),
    )