from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.database import Base, get_db
from app.models import User  # Import the User model
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

def delete_test_user(username):
    db = TestingSessionLocal()
    user = db.query(User).filter(User.username == username).first()
    if user:
        db.delete(user)
        db.commit()
    db.close()

def test_create_user():
    delete_test_user("testuser2")
    response = client.post(
        "/register",
        json={"username": "testuser2", "password": "testpassword"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert data["username"] == "testuser2"
    assert "id" in data

def test_login_user():
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
    )
    assert response.status_code == 200, response.text
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"
