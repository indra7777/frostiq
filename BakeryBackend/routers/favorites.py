from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from typing import List
from BakeryBackend.database import get_db
from BakeryBackend.models import Favorite as FavoriteModel
from BakeryBackend.schemas import Favorite
from BakeryBackend.exceptions import (
    ValidationError,
    NotFoundError,
    ConflictError,
    UnauthorizedError,
    DatabaseError
)

router = APIRouter(prefix="/favorites", tags=["Favorites"])


@router.post("/", response_model=Favorite)
def add_favorite(favorite: Favorite, db: Session = Depends(get_db)):
    """Add a new favorite item for a user"""
    try:
        # Input validation
        if favorite.user_id <= 0:
            raise ValidationError(
                message="Invalid user ID provided",
                details={"user_id": favorite.user_id, "requirement": "must be positive integer"}
            )
        
        if favorite.item_id <= 0:
            raise ValidationError(
                message="Invalid item ID provided", 
                details={"item_id": favorite.item_id, "requirement": "must be positive integer"}
            )
        
        if not favorite.item_name or len(favorite.item_name.strip()) == 0:
            raise ValidationError(
                message="Item name cannot be empty",
                details={"item_name": favorite.item_name}
            )

        # Duplicate detection
        existing = db.query(FavoriteModel).filter(
            FavoriteModel.user_id == favorite.user_id,
            FavoriteModel.item_id == favorite.item_id
        ).first()
        
        if existing:
            raise ConflictError(
                message="Favorite already exists for this user and item",
                details={
                    "user_id": favorite.user_id,
                    "item_id": favorite.item_id,
                    "existing_favorite_id": existing.id
                }
            )
        
        # Create new favorite
        db_fav = FavoriteModel(
            user_id=favorite.user_id,
            item_id=favorite.item_id,
            item_name=favorite.item_name.strip()
        )
        db.add(db_fav)
        db.commit()
        db.refresh(db_fav)
        return db_fav
        
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            message="Failed to add favorite item to database",
            details={
                "user_id": favorite.user_id,
                "item_id": favorite.item_id,
                "db_error": str(e)
            }
        )


@router.get("/{user_id}", response_model=List[Favorite])
def get_favorites(user_id: int, db: Session = Depends(get_db)):
    """Get all favorite items for a specific user"""
    try:
        # Input validation
        if user_id <= 0:
            raise ValidationError(
                message="Invalid user ID provided",
                details={"user_id": user_id, "requirement": "must be positive integer"}
            )
        
        # Get favorites from database
        favorites = db.query(FavoriteModel).filter(FavoriteModel.user_id == user_id).all()
        
        # Note: Empty list is valid response, not an error
        return favorites
        
    except SQLAlchemyError as e:
        raise DatabaseError(
            message="Failed to retrieve favorites from database",
            details={
                "user_id": user_id,
                "db_error": str(e)
            }
        )


@router.delete("/{favorite_id}")
def delete_favorite(favorite_id: int, user_id: int, db: Session = Depends(get_db)):
    """Delete a specific favorite item"""
    try:
        # Input validation
        if favorite_id <= 0:
            raise ValidationError(
                message="Invalid favorite ID provided",
                details={"favorite_id": favorite_id, "requirement": "must be positive integer"}
            )
        
        if user_id <= 0:
            raise ValidationError(
                message="Invalid user ID provided",
                details={"user_id": user_id, "requirement": "must be positive integer"}
            )
        
        # Find the favorite
        fav = db.query(FavoriteModel).filter(FavoriteModel.id == favorite_id).first()
        
        if not fav:
            raise NotFoundError(
                message="Favorite not found",
                details={"favorite_id": favorite_id}
            )
        
        # Authorization check
        if fav.user_id != user_id:
            raise UnauthorizedError(
                message="Not authorized to delete this favorite",
                details={
                    "favorite_id": favorite_id,
                    "requested_by_user": user_id,
                    "favorite_belongs_to_user": fav.user_id
                }
            )
        
        # Delete the favorite
        db.delete(fav)
        db.commit()
        
        return {
            "message": "Favorite deleted successfully",
            "deleted_favorite": {
                "id": favorite_id,
                "user_id": user_id,
                "item_name": fav.item_name
            }
        }
        
    except SQLAlchemyError as e:
        db.rollback()
        raise DatabaseError(
            message="Failed to delete favorite from database",
            details={
                "favorite_id": favorite_id,
                "user_id": user_id,
                "db_error": str(e)
            }
        )


@router.get("/item/{item_id}/users", response_model=List[Favorite])
def get_users_who_favorited_item(item_id: int, db: Session = Depends(get_db)):
    """Get all users who have favorited a specific item"""
    try:
        # Input validation
        if item_id <= 0:
            raise ValidationError(
                message="Invalid item ID provided",
                details={"item_id": item_id, "requirement": "must be positive integer"}
            )
        
        # Get all favorites for this item
        favorites = db.query(FavoriteModel).filter(FavoriteModel.item_id == item_id).all()
        
        return favorites
        
    except SQLAlchemyError as e:
        raise DatabaseError(
            message="Failed to retrieve item favorites from database",
            details={
                "item_id": item_id,
                "db_error": str(e)
            }
        )


@router.get("/user/{user_id}/item/{item_id}")
def check_if_favorited(user_id: int, item_id: int, db: Session = Depends(get_db)):
    """Check if a specific item is favorited by a specific user"""
    try:
        # Input validation
        if user_id <= 0:
            raise ValidationError(
                message="Invalid user ID provided",
                details={"user_id": user_id, "requirement": "must be positive integer"}
            )
        
        if item_id <= 0:
            raise ValidationError(
                message="Invalid item ID provided",
                details={"item_id": item_id, "requirement": "must be positive integer"}
            )
        
        # Check if favorite exists
        favorite = db.query(FavoriteModel).filter(
            FavoriteModel.user_id == user_id,
            FavoriteModel.item_id == item_id
        ).first()
        
        return {
            "user_id": user_id,
            "item_id": item_id,
            "is_favorited": favorite is not None,
            "favorite_id": favorite.id if favorite else None,
            "favorite_details": {
                "item_name": favorite.item_name,
                "created_at": favorite.id  # Assuming you have timestamp in model
            } if favorite else None
        }
        
    except SQLAlchemyError as e:
        raise DatabaseError(
            message="Failed to check favorite status",
            details={
                "user_id": user_id,
                "item_id": item_id,
                "db_error": str(e)
            }
        )