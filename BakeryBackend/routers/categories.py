from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from typing import List
from BakeryBackend.database import get_db
from BakeryBackend.models import Category as CategoryModel
from BakeryBackend.schemas import Category, CategoryCreate, CategoryUpdate

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", response_model=Category)
def create_category(category: CategoryCreate, db: Session = Depends(get_db)):
    try:
        db_category = CategoryModel(**category.dict())
        db.add(db_category)
        db.commit()
        db.refresh(db_category)
        return db_category
    except IntegrityError:
        raise HTTPException(status_code=409, detail="Category with this name already exists")

@router.get("/", response_model=List[Category])
def get_categories(skip: int = 0, limit: int = 100, active_only: bool = True, db: Session = Depends(get_db)):
    query = db.query(CategoryModel)
    if active_only:
        query = query.filter(CategoryModel.is_active == True)
    return query.offset(skip).limit(limit).all()

@router.get("/{category_id}", response_model=Category)
def get_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category

@router.put("/{category_id}", response_model=Category)
def update_category(category_id: int, category_update: CategoryUpdate, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    update_data = category_update.dict(exclude_unset=True)
    if update_data:
        for field, value in update_data.items():
            setattr(category, field, value)
        
        try:
            db.commit()
            db.refresh(category)
        except IntegrityError:
            raise HTTPException(status_code=409, detail="Category with this name already exists")
    
    return category

@router.delete("/{category_id}")
def delete_category(category_id: int, db: Session = Depends(get_db)):
    category = db.query(CategoryModel).filter(CategoryModel.id == category_id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    
    # Check if category has items
    if category.items:
        raise HTTPException(status_code=409, detail="Cannot delete category with existing items")
    
    db.delete(category)
    db.commit()
    return {"message": "Category deleted successfully"}