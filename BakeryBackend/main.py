from fastapi import FastAPI
from BakeryBackend.routers import favorites, categories, items
from BakeryBackend.database import Base, engine

# Create all tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Enhanced Bakery Backend API",
    description="Complete bakery management system with categories, items, and favorites",
    version="2.0.0"
)

# Include all routers
app.include_router(categories.router)
app.include_router(items.router)
app.include_router(favorites.router)

@app.get("/")
def root():
    return {
        "message": "Enhanced Bakery Backend API", 
        "version": "2.0.0",
        "endpoints": {
            "categories": "/categories",
            "items": "/items", 
            "favorites": "/favorites"
        }
    }