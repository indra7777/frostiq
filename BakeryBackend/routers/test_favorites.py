import pytest
from fastapi.testclient import TestClient
from BakeryBackend.main import app
from BakeryBackend.database import Base, engine, get_db
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from BakeryBackend.models import Favorite as FavoriteModel

# Use an in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"
test_engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

Base.metadata.create_all(bind=test_engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db
client = TestClient(app)

def test_add_favorite():
    # Add a favorite
    response = client.post("/favorites/", json={"user_id": 1, "item_id": 101, "item_name": "Cake"})
    assert response.status_code == 200
    data = response.json()
    assert data["user_id"] == 1
    assert data["item_id"] == 101
    assert data["item_name"] == "Cake"

    # Try to add duplicate
    response = client.post("/favorites/", json={"user_id": 1, "item_id": 101, "item_name": "Cake"})
    assert response.status_code == 409
    assert "already exists" in response.json()["detail"]

def test_delete_favorite():
    # Add a favorite to delete
    response = client.post("/favorites/", json={"user_id": 2, "item_id": 202, "item_name": "Pie"})
    fav_id = response.json()["id"]
    # Unauthorized delete (wrong user)
    response = client.delete(f"/favorites/{fav_id}?user_id=999")
    assert response.status_code == 403
    # Authorized delete
    response = client.delete(f"/favorites/{fav_id}?user_id=2")
    assert response.status_code == 200
    assert response.json()["message"] == "Favorite deleted successfully" 