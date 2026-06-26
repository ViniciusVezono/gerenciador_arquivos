import pytest
import io

def test_health_check(client):
    response = client.get("/health/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "ok"
    assert data["database"] == "ok"

def test_upload_image(client):
    file_content = b"fake image content"
    files = {
        "file": ("test.png", io.BytesIO(file_content), "image/png")
    }
    
    response = client.post("/images/", files=files)
    assert response.status_code == 201
    data = response.json()
    assert data["filename"] == "test.png"
    assert data["mime_type"] == "image/png"
    assert "url" in data
    assert data["user_id"] == "test_user_123"

def test_get_images_empty(client):
    response = client.get("/images/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 0

def test_upload_and_get_images(client):
    file_content = b"fake image content"
    files = {
        "file": ("test2.png", io.BytesIO(file_content), "image/png")
    }
    
    client.post("/images/", files=files)
    
    response = client.get("/images/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["filename"] == "test2.png"
