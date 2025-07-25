from pydantic import BaseModel, constr
from typing import Optional

class Favorite(BaseModel):
    id: Optional[int] = None  # Optional, will be filled when returning data
    user_id: int
    item_id: int
    item_name: constr(min_length=1, strip_whitespace=True)
