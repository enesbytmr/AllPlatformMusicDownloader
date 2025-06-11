from fastapi.testclient import TestClient
import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

os.environ["CELERY_BROKER_URL"] = "memory://"
os.environ["CELERY_RESULT_BACKEND"] = "cache+memory://"
os.environ["CELERY_TASK_ALWAYS_EAGER"] = "false"
os.environ["STRIPE_API_KEY"] = "sk_test"

from backend.main import app
import backend.billing as billing

client = TestClient(app)


def _register(email="bill@example.com"):
    data = {"email": email, "password": "secret"}
    resp = client.post("/auth/register", json=data)
    assert resp.status_code == 200
    return resp.json()["access_token"]


def test_list_plans():
    resp = client.get("/billing/plans")
    assert resp.status_code == 200
    assert "free" in resp.json()


def test_quota_enforcement(monkeypatch):
    token = _register("bill1@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    monkeypatch.setattr(billing, "create_checkout_session", lambda plan, user: "url")

    for _ in range(10):
        files = {"file": ("tracks.txt", b"song")}
        resp = client.post("/download/text", files=files, headers=headers)
        assert resp.status_code == 200

    files = {"file": ("tracks.txt", b"song")}
    resp = client.post("/download/text", files=files, headers=headers)
    assert resp.status_code == 402


def test_upgrade_plan(monkeypatch):
    token = _register("bill2@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    monkeypatch.setattr(billing, "create_checkout_session", lambda plan, user: "checkout")
    resp = client.post("/billing/upgrade", headers=headers, params={"plan": "pro"})
    assert resp.status_code == 200
    assert resp.json()["checkout_url"] == "checkout"
