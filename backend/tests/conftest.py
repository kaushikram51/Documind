import pytest
import os

# Disable rate limiting before importing app
os.environ["TESTING"] = "true"

from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.core.database import get_db, Base

TEST_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    TEST_DATABASE_URL,
    connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(
    autocommit=False, autoflush=False, bind=engine
)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(autouse=True)
def setup_database():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

@pytest.fixture
def client():
    return TestClient(app)

@pytest.fixture
def registered_user(client):
    client.post("/auth/register", json={
        "email": "test@example.com",
        "password": "password123"
    })
    return {"email": "test@example.com", "password": "password123"}

@pytest.fixture
def auth_headers(client, registered_user):
    response = client.post("/auth/login", json={
        "email": registered_user["email"],
        "password": registered_user["password"]
    })
    data = response.json()
    assert "access_token" in data, f"Login failed: {data}"
    token = data["access_token"]
    return {"Authorization": f"Bearer {token}"}