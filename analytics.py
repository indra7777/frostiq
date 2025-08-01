from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from collections import defaultdict
from typing import List, Dict
from database import get_db
from models import Favorite, Item
from schemas import ItemAnalyticsResponse

router = APIRouter()

@router.get("/analytics/most-favorited", response_model=List[Dict])
def get_most_favorited_items(db: Session = Depends(get_db)):
    results = (
        db.query(Favorite.item_id, Item.name, func.count(Favorite.id).label("count"))
        .join(Item, Item.id == Favorite.item_id)
        .group_by(Favorite.item_id, Item.name)
        .order_by(func.count(Favorite.id).desc())
        .limit(5)
        .all()
    )
    return [{"item_id": r[0], "item_name": r[1], "favorites": r[2]} for r in results]


@router.get("/analytics/active-hours", response_model=Dict[str, int])
def get_active_hours(db: Session = Depends(get_db)):
    hour_counts = defaultdict(int)
    all_favorites = db.query(Favorite).all()
    for fav in all_favorites:
        hour = fav.created_at.strftime("%H:00")
        hour_counts[hour] += 1
    return dict(sorted(hour_counts.items()))


@router.get("/analytics/trending-items", response_model=Dict[str, int])
def get_trending_items(db: Session = Depends(get_db)):
    item_counts = defaultdict(int)
    for fav in db.query(Favorite).all():
        day = fav.created_at.strftime("%Y-%m-%d")
        item_counts[day] += 1
    return dict(sorted(item_counts.items()))
