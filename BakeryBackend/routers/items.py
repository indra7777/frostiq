from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from BakeryBackend.database import get_db
from BakeryBackend.models import Item as ItemModel, Category as CategoryModel
from BakeryBackend.schemas import Item, ItemCreate, ItemUpdate

router = APIRouter(prefix="/items", tags=["Items"])

@router.post("/", response_model=Item)
def create_item(item: ItemCreate, db: Session = Depends(get_db)):
    # Check if category exists
    category = db.query(CategoryModel).filter(CategoryModel.id == item.category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    db_item = ItemModel(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.get("/", response_model=List[Item])
def get_items(
    skip: int = 0, 
    limit: int = 100, 
    category_id: Optional[int] = None,
    available_only: bool = True,
    min_price: Optional[float] = None,
    max_price: Optional[float] = None,
    db: Session = Depends(get_db)
):
    query = db.query(ItemModel)
    
    if available_only:
        query = query.filter(ItemModel.is_available == True)
    if category_id:
        query = query.filter(ItemModel.category_id == category_id)
    if min_price is not None:
        query = query.filter(ItemModel.price >= min_price)
    if max_price is not None:
        query = query.filter(ItemModel.price <= max_price)
    
    return query.offset(skip).limit(limit).all()

@router.get("/{item_id}", response_model=Item)
def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}", response_model=Item)
def update_item(item_id: int, item_update: ItemUpdate, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    update_data = item_update.dict(exclude_unset=True)
    
    # Check if category exists when updating category_id
    if 'category_id' in update_data:
        category = db.query(CategoryModel).filter(CategoryModel.id == update_data['category_id']).first()
        if not category:
            raise HTTPException(status_code=404, detail="Category not found")
    
    if update_data:
        for field, value in update_data.items():
            setattr(item, field, value)
        db.commit()
        db.refresh(item)
    
    return item

@router.delete("/{item_id}")
def delete_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    db.delete(item)
    db.commit()
    return {"message": "Item deleted successfully"}

@router.patch("/{item_id}/availability")
def toggle_availability(item_id: int, available: bool, db: Session = Depends(get_db)):
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.is_available = available
    db.commit()
    db.refresh(item)
    return {"message": f"Item availability updated to {available}"}

@router.patch("/{item_id}/stock")
def update_stock(item_id: int, quantity: int, db: Session = Depends(get_db)):
    if quantity < 0:
        raise HTTPException(status_code=400, detail="Stock quantity cannot be negative")
    
    item = db.query(ItemModel).filter(ItemModel.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    
    item.stock_quantity = quantity
    db.commit()
    db.refresh(item)
    return {"message": f"Stock updated to {quantity}"}