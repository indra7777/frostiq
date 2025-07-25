from sqlalchemy import Column, Integer, String
from BakeryBackend.database import Base

class Favorite(Base):
    __tablename__ = "favorites"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, index=True)
    item_id = Column(Integer, index=True)
    item_name = Column(String, nullable=False)
