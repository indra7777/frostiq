from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import favorites
from database import Base, engine

app = FastAPI(title="Bakery Backend with Favorites")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to the frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creating tables on startup
@app.on_event("startup")
def on_startup():
    Base.metadata.create_all(bind=engine)

app.include_router(favorites.router, tags=["Favorites"])
