from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.auth import create_access_token
from datetime import timedelta
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

def test_create_comment():
    token = create_access_token(data={"sub": "testuser"}, expires_delta=timedelta(minutes=30))
    response = client.post(
        "/movies/1/comments/",
        json={"text": "Test Comment"},
        headers={"Authorization": f"Bearer {token}"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["text"] == "Test Comment"
    assert "id" in data
    assert "movie_id" in data
    assert "user_id" in data

def test_read_comments():
    response = client.get("/movies/1/comments/")
    assert response.status_code == 200, response.text
    data = response.json()
    assert isinstance(data, list)
