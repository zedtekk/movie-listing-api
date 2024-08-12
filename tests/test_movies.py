from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.auth import create_access_token
from datetime import timedelta, timezone, datetime
import os

DATABASE_URL = os.environ.get('DB_URL')
engine = create_engine(DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

def create_test_user():
    response = client.post(
        "/register",
        json={"username": "testuser", "password": "testpassword"},
    )
    if response.status_code != 200:
        response = client.post(
            "/token",
            data={"username": "testuser", "password": "testpassword"},
        )
    return response.json()

user_data = create_test_user()
token = user_data.get("access_token", "")

def create_test_movie(token):
    response = client.post(
        "/movies/",
        json={"title": "Test Movie", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    return data["id"]

def test_create_movie():
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.post(
        "/movies/",
        json={"title": "Test Movie", "description": "Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Movie"
    assert data["description"] == "Test Description"
    assert "id" in data
    assert "owner_id" in data

def test_read_movies():
    response = client.get("/movies/", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)

def test_update_movie():
    movie_id = create_test_movie(token)
    response = client.put(
        f"/movies/{movie_id}",
        json={"title": "Updated Test Movie", "description": "Updated Test Description"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Updated Test Movie"
    assert data["description"] == "Updated Test Description"

def test_delete_movie():
    movie_id = create_test_movie(token)
    response = client.delete(
        f"/movies/{movie_id}",
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["title"] == "Test Movie"
