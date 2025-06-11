from fastapi.testclient import TestClient
import os
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["CELERY_BROKER_URL"] = "memory://"
os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"
os.environ["CELERY_TASK_ALWAYS_EAGER"] = "false"
from backend.main import app

client = TestClient(app)


def _register():
    data = {"email": "oauth@example.com", "password": "secret"}
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_spotify_flow():
    token = _register()
    headers = {"Authorization": f"Bearer {token}"}
    resp = client.get("/connect/spotify", headers=headers, allow_redirects=False)
    assert resp.status_code in (302, 307)
    resp = client.get("/callback/spotify?code=testcode", headers=headers)
    assert resp.status_code == 200
    assert resp.json()["access_token"] == "spotify_token_testcode"
