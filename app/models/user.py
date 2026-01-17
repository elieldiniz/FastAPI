from sqlalchemy import Column, Integer, String, Boolean, DateTime, func
from sqlalchemy.orm import relationship
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    full_name = Column(String, nullable=True)
    hashed_password = Column(String, nullable=False)
    role = Column(String, default="user") # "admin" or "user"
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())

    posts = relationship("Post", back_populates="author", cascade="all, delete-orphan")
