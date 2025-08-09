from pydantic import BaseModel, constr, Field
from typing import Optional, List
from datetime import datetime

# Category Schemas
class CategoryBase(BaseModel):
    name: constr(min_length=1, max_length=100, strip_whitespace=True)
    description: Optional[str] = None
    is_active: bool = True

class CategoryCreate(CategoryBase):
    pass

class CategoryUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=100, strip_whitespace=True)] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class Category(CategoryBase):
    id: int
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# Item Schemas
class ItemBase(BaseModel):
    name: constr(min_length=1, max_length=200, strip_whitespace=True)
    description: Optional[str] = None
    price: float = Field(..., gt=0)
    category_id: int
    image_url: Optional[str] = None
    is_available: bool = True
    stock_quantity: int = Field(default=0, ge=0)
    ingredients: Optional[str] = None
    allergens: Optional[str] = None
    preparation_time: Optional[int] = Field(None, gt=0)

class ItemCreate(ItemBase):
    pass

class ItemUpdate(BaseModel):
    name: Optional[constr(min_length=1, max_length=200, strip_whitespace=True)] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    category_id: Optional[int] = None
    image_url: Optional[str] = None
    is_available: Optional[bool] = None
    stock_quantity: Optional[int] = Field(None, ge=0)
    ingredients: Optional[str] = None
    allergens: Optional[str] = None
    preparation_time: Optional[int] = Field(None, gt=0)

class Item(ItemBase):
    id: int
    created_at: datetime
    updated_at: datetime
    category: Category
    
    class Config:
        from_attributes = True

# Favorite Schemas  
class FavoriteBase(BaseModel):
    user_id: int
    item_id: int

class FavoriteCreate(FavoriteBase):
    pass

class Favorite(FavoriteBase):
    id: int
    created_at: datetime
    item: Item
    
    class Config:
        from_attributes = True