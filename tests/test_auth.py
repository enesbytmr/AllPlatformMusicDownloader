from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.main import app

client = TestClient(app)


def test_register_and_login():
    data = {"email": "user@example.com", "password": "secret"}
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 200
    token = resp.json()["access_token"]
    assert token

    resp = client.post("/auth/login", json=data)
    assert resp.status_code == 200
    assert resp.json()["access_token"]


def test_download_requires_auth():
    files = {"file": ("tracks.txt", b"song1")}
    resp = client.post("/download/text", files=files)
    assert resp.status_code == 401
