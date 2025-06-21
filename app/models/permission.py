from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.mixins import AuditMixin


class Permission(Base, AuditMixin):
    __tablename__ = "permissions"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, nullable=False)

    roles = relationship("Role", secondary="role_permissions", back_populates="permissions")