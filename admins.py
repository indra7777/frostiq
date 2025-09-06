@router.post("/items/{item_id}/stock")
def update_stock(item_id: int, stock: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    item.stock = stock
    db.commit()
    return {"message": "Stock updated", "new_stock": stock}
