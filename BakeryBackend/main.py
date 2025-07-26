from fastapi import FastAPI
from database import Base, engine
from routers import favorites

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Bakery Backend with Favorites")
@app.get("/")
async def root():
    return {"message": "Welcome to the Bakery Backend API!"}

app.include_router(favorites.router)


