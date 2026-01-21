import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.main import app
from app.core.database import Base, get_db
from app.core.security import get_password_hash

# Setup in-memory SQLite database for testing
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "Retro Tech Blog" in response.text

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_create_user():
    response = client.post(
        "/api/v1/users/",
        json={"email": "test@example.com", "password": "testpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "test@example.com"
    assert "id" in data

def test_login():
    # Create a user first
    client.post(
        "/api/v1/users/",
        json={"email": "login@example.com", "password": "loginpassword"},
    )

    # Try to login
    response = client.post(
        "/api/v1/auth/login",
        data={"username": "login@example.com", "password": "loginpassword"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_get_posts_empty():
    response = client.get("/api/v1/posts/")
    assert response.status_code == 200
    assert response.json() == []

def test_create_post_unauthorized():
    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post Title", "content": "Test Post Content with enough length"},
    )
    assert response.status_code == 401 # Should be 401 because not authenticated

def test_create_post_admin():
    # 1. Create admin user manually in DB because we don't have an endpoint for it (it's internal/fixed)
    # Or we can just create a user and update role.
    db = TestingSessionLocal()
    from app.models.user import User
    admin_user = User(
        email="admin@example.com",
        hashed_password=get_password_hash("adminpassword"),
        role="admin"
    )
    db.add(admin_user)
    db.commit()
    db.close()

    # 2. Login as admin
    login_response = client.post(
        "/api/v1/auth/login",
        data={"username": "admin@example.com", "password": "adminpassword"},
    )
    token = login_response.json()["access_token"]

    # 3. Create post
    response = client.post(
        "/api/v1/posts/",
        json={"title": "Test Post Title", "content": "Test Post Content with enough length"},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Test Post Title"
    assert data["published"] is False
