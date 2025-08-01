from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from BakeryBackend import models, schemas
from BakeryBackend.database import get_db

router = APIRouter(prefix="/search", tags=["Search"])

@router.get("/favorites/", response_model=List[schemas.Favorite])
def search_favorites(
    item_name: str = Query(..., min_length=1),
    limit: int = Query(10, ge=1),
    offset: int = Query(0, ge=0),
    db: Session = Depends(get_db),
):
    search_pattern = f"%{item_name.lower()}%"
    favorites = (
        db.query(models.Favorite)
        .filter(func.lower(models.Favorite.item_name).like(search_pattern))
        .order_by(models.Favorite.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
    # Track search counts
    search_stat = db.query(models.SearchStat).filter_by(item_name=item_name.lower()).first()
    if search_stat:
        search_stat.search_count += 1
    else:
        search_stat = models.SearchStat(item_name=item_name.lower(), search_count=1)
        db.add(search_stat)
    db.commit()
    return favorites

@router.get("/most-searched/", response_model=List[str])
def most_searched_items(
    limit: int = Query(10, ge=1),
    db: Session = Depends(get_db),
):
    stats = (
        db.query(models.SearchStat.item_name)
        .order_by(models.SearchStat.search_count.desc())
        .limit(limit)
        .all()
    )
    return [item[0] for item in stats]
