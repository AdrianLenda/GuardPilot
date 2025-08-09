import os
import sys
import tempfile
from pathlib import Path

# Ensure the application package is on the import path
sys.path.append(str(Path(__file__).resolve().parents[1]))

# Set environment variables before importing application
os.environ.setdefault("DATABASE_URL", "sqlite:///./test.db")
os.environ.setdefault("LOGS_DIR", tempfile.mkdtemp())

from fastapi.testclient import TestClient
from app.main import app


def test_health_endpoint():
    with TestClient(app) as client:
        response = client.get("/health")
        assert response.status_code == 200
        assert response.json() == {"status": "ok"}


def test_proxy_and_logs():
    with TestClient(app) as client:
        payload = {"messages": [{"role": "user", "content": "hello"}]}
        response = client.post("/proxy", json=payload)
        assert response.status_code == 200
        data = response.json()
        assert "conversation_id" in data
        assert data["reply"].startswith("Echo")

        logs_response = client.get("/logs")
        assert logs_response.status_code == 200
        logs = logs_response.json()
        assert isinstance(logs, list)
        assert any(log["prompt"] == "hello" for log in logs)


def test_conversation_history():
    with TestClient(app) as client:
        conv_id = "conv-hist"
        first = {"conversation_id": conv_id, "messages": [{"role": "user", "content": "hello"}]}
        first_resp = client.post("/proxy", json=first)
        assert first_resp.status_code == 200
        first_reply = first_resp.json()["reply"]

        second = {
            "conversation_id": conv_id,
            "messages": [
                {"role": "user", "content": "hello"},
                {"role": "assistant", "content": first_reply},
                {"role": "user", "content": "who are you?"},
            ],
        }
        second_resp = client.post("/proxy", json=second)
        assert second_resp.status_code == 200
        data = second_resp.json()
        assert data["conversation_id"] == conv_id
        assert "hello" in data["reply"]
        assert "who are you?" in data["reply"]

        logs = client.get("/logs", params={"conversation_id": conv_id}).json()
        assert len(logs) == 2

def test_logs_filter_by_conversation_id():
    with TestClient(app) as client:
        payload1 = {
            "conversation_id": "conv-1",
            "messages": [{"role": "user", "content": "hello"}],
        }
        payload2 = {
            "conversation_id": "conv-2",
            "messages": [{"role": "user", "content": "hi"}],
        }
        client.post("/proxy", json=payload1)
        client.post("/proxy", json=payload2)
        response = client.get("/logs", params={"conversation_id": "conv-1"})
        assert response.status_code == 200
        logs = response.json()
        assert len(logs) == 1
        assert logs[0]["conversation_id"] == "conv-1"


def test_logs_filter_with_unknown_conversation_id():
    with TestClient(app) as client:
        payload = {
            "conversation_id": "conv-x",
            "messages": [{"role": "user", "content": "hey"}],
        }
        client.post("/proxy", json=payload)
        response = client.get("/logs", params={"conversation_id": "missing"})
        assert response.status_code == 200
        assert response.json() == []
