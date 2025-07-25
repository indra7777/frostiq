from fastapi import FastAPI
from BakeryBackend.routers import favorites
from BakeryBackend.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bakery Backend with Favorites")

app.include_router(favorites.router)


