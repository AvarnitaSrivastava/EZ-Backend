import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.database import SessionLocal
from app.models import User
from app.auth import get_password_hash
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


client = TestClient(app)

@pytest.fixture(scope="module", autouse=True)
def create_ops_user():
    db = SessionLocal()
    if not db.query(User).filter_by(email="ops@example.com").first():
        user = User(
            email="ops@example.com",
            password_hash=get_password_hash("opspassword"),
            role="ops",
            is_verified=True
        )
        db.add(user)
        db.commit()
    db.close()

def test_ops_login(create_ops_user):
    response = client.post("/ops/login", json={
        "email": "ops@example.com",
        "password": "opspassword"
    })
    assert response.status_code == 200
    assert "access_token" in response.json()

def test_ops_upload_file(create_ops_user):
    
    login = client.post("/ops/login", json={
        "email": "ops@example.com",
        "password": "opspassword"
    })
    token = login.json()["access_token"]
    
    file_content = b"test file content"
    response = client.post(
        "/ops/upload-file",
        files={"file": ("test.docx", file_content, "application/vnd.openxmlformats-officedocument.wordprocessingml.document")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 201
    assert "file_id" in response.json()
    
    response = client.post(
        "/ops/upload-file",
        files={"file": ("test.txt", file_content, "text/plain")},
        headers={"Authorization": f"Bearer {token}"}
    )
    assert response.status_code == 400



