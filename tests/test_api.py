"""HTTP-level tests against the FastAPI app with an in-memory SQLite."""

import os
import tempfile

import pytest
from fastapi.testclient import TestClient


@pytest.fixture(autouse=True)
def temp_db(monkeypatch):
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{path}")
    monkeypatch.setenv("ENVIRONMENT", "test")

    # Re-import module-level state so settings pick up the env.
    import importlib

    import app.main

    importlib.reload(app.main)
    yield
    os.remove(path)


@pytest.fixture
def client():
    from app.main import app

    return TestClient(app)


def test_count_starts_at_zero(client):
    r = client.get("/count")
    assert r.status_code == 200
    assert r.json() == {"value": 0}


def test_increment_returns_new_value(client):
    r = client.post("/increment")
    assert r.status_code == 200
    body = r.json()
    assert body["value"] == 1
    assert "updated_at" in body


def test_two_increments_differ_by_one(client):
    assert client.post("/increment").json()["value"] == 1
    assert client.post("/increment").json()["value"] == 2


def test_health_returns_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"