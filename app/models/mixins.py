from sqlalchemy import Column, Integer, DateTime, ForeignKey, func
from sqlalchemy.orm import declared_attr


class AuditMixin:
    @declared_attr
    def created_by(cls):
        return Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    @declared_attr
    def updated_by(cls):
        return Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True)

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), onupdate=func.now(), nullable=True)
