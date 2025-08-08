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
