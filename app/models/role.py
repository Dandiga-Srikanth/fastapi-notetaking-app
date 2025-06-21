from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base
from app.models.mixins import AuditMixin


class Role(Base, AuditMixin):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)

    users = relationship("User", back_populates="role", cascade="all, delete")
    permissions = relationship("Permission", secondary="role_permissions", back_populates="roles")
