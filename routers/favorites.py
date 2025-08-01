from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional

from BakeryBackend import models, schemas
from BakeryBackend.database import get_db

router = APIRouter(prefix="/favorites", tags=["Favorites"])

@router.get("/{user_id}", response_model=List[schemas.Favorite])
def get_user_favorites(
    user_id: int,
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    category: Optional[str] = None,
    is_public: Optional[bool] = None,
    db: Session = Depends(get_db)
):
    query = db.query(models.Favorite).filter(models.Favorite.user_id == user_id)

    if category:
        query = query.filter(models.Favorite.category == category)
    if is_public is not None:
        query = query.filter(models.Favorite.is_public == is_public)

    favorites = query.order_by(models.Favorite.created_at.desc()).offset(offset).limit(limit).all()
    return favorites

@router.post("/", response_model=schemas.Favorite)
def add_favorite(fav: schemas.Favorite, db: Session = Depends(get_db)):
    # Optional: Check for duplicates
    new_fav = models.Favorite(**fav.dict(exclude_unset=True))
    db.add(new_fav)
    db.commit()
    db.refresh(new_fav)
    return new_fav
