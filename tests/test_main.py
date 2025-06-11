from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["CELERY_BROKER_URL"] = "memory://"
os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"
os.environ["CELERY_TASK_ALWAYS_EAGER"] = "false"
from backend.main import app

client = TestClient(app)


def test_root_endpoint():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello, World"}


def test_download_task_creation():
    data = {"email": "task@example.com", "password": "secret"}
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    files = {"file": ("tracks.txt", b"song1")}
    resp = client.post("/download/text", files=files, headers=headers)
    assert resp.status_code == 200
    assert "task_id" in resp.json()
