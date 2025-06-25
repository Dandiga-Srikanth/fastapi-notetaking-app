from app.db.session import Base
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from app.models.mixins import AuditMixin
from sqlalchemy.orm import relationship

class User(Base, AuditMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)

    role_id = Column(Integer, ForeignKey("roles.id", ondelete="SET NULL"), nullable=True)
    
    role = relationship("Role", back_populates="users", foreign_keys=[role_id])
    notes = relationship("Note", back_populates="owner", foreign_keys="[Note.user_id]", cascade="all, delete-orphan")