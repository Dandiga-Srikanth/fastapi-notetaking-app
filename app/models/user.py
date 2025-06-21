from app.db.session import Base
from sqlalchemy import Column, Integer, String

class User(Base):
    __tablename__ = "users"
    __versioned__ = {}

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=True)
    last_name = Column(String, nullable=True)