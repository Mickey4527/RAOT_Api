import uuid
from sqlalchemy import ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.models.base import SQLModel

class RolePermission(SQLModel):
    __tablename__ = "role_permission"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("resource.id"), nullable=False)
    role_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("user_role.id"), nullable=False)
    permission_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("permission.id"), nullable=False)
    

    role: Mapped["UserRole"] = relationship("UserRole", back_populates="role_permission")
    permission: Mapped["Permission"] = relationship("Permission", back_populates="role_permission")
    resource: Mapped["Resource"] = relationship("Resource", back_populates="role_permission")