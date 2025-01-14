import uuid
from sqlalchemy import String, Boolean
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class Permission(SQLModel):
    __tablename__ = "permission"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    permission_type: Mapped[str] = mapped_column(String(255), nullable=False)

    role_permission: Mapped["RolePermission"] = relationship("RolePermission", back_populates="permission") # type: ignore