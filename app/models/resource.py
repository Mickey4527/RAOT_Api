import uuid
from sqlalchemy import Boolean, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import SQLModel

class Resource(SQLModel):
    __tablename__ = "resource"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    resource_name: Mapped[str] = mapped_column(String(255), nullable=False)
    resource_description: Mapped[str] = mapped_column(String(255), nullable=False)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)

    role_permission: Mapped["RolePermission"] = relationship("RolePermission", back_populates="resource") # type: ignore
    