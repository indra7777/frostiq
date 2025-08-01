from pydantic import BaseModel, constr, Field
from typing import Optional
from datetime import datetime

class Favorite(BaseModel):
    id: Optional[int] = None
    user_id: int
    item_id: int
    item_name: constr(min_length=1, strip_whitespace=True)
    category: Optional[str] = None
    rating: Optional[float] = Field(None, ge=1, le=5)
    experience: Optional[str] = None
    is_public: Optional[bool] = True
    created_at: Optional[datetime] = None

    class Config:
        orm_mode = True
