from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from BakeryBackend.database import get_db
from BakeryBackend.models import Favorite as FavoriteModel
from BakeryBackend.schemas import Favorite

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/", response_model=Favorite)
def add_favorite(favorite: Favorite, db: Session = Depends(get_db)):
    # Duplicate detection
    existing = db.query(FavoriteModel).filter(
        FavoriteModel.user_id == favorite.user_id,
        FavoriteModel.item_id == favorite.item_id
    ).first()
    if existing:
        raise HTTPException(status_code=409, detail="Favorite already exists for this user and item.")
    db_fav = FavoriteModel(
        user_id=favorite.user_id,
        item_id=favorite.item_id,
        item_name=favorite.item_name
    )
    db.add(db_fav)
    db.commit()
    db.refresh(db_fav)
    return db_fav

@router.get("/{user_id}", response_model=List[Favorite])
def get_favorites(user_id: int, db: Session = Depends(get_db)):
    favorites = db.query(FavoriteModel).filter(FavoriteModel.user_id == user_id).all()
    return favorites

@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, user_id: int, db: Session = Depends(get_db)):
    fav = db.query(FavoriteModel).filter(FavoriteModel.id == favorite_id).first()
    if not fav:
        raise HTTPException(status_code=404, detail="Favorite not found")
    if fav.user_id != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this favorite.")
    db.delete(fav)
    db.commit()
    return {"message": "Favorite deleted successfully"}