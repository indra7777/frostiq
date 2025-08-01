from sqlalchemy import Column, Integer, String, Boolean, DateTime, Float
from sqlalchemy.sql import func
from BakeryBackend.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    item_id = Column(Integer, index=True)
    item_name = Column(String, nullable=False)
    category = Column(String, nullable=True)  # New
    rating = Column(Float, nullable=True)     # New: 1-5
    experience = Column(String, nullable=True)  # Optional user comment
    is_public = Column(Boolean, default=True)   # New
    created_at = Column(DateTime(timezone=True), server_default=func.now())  # New
