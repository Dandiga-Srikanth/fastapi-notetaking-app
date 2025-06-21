from app.db.session import Base
from sqlalchemy import Column, Integer, String
from app.models.mixins import AuditMixin
from sqlalchemy.orm import relationship

class User(Base, AuditMixin):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)

    notes = relationship("Note", back_populates="owner", cascade="all, delete-orphan")