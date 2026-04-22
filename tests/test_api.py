import pytest

from app.main import app


@pytest.fixture
def client():
    with app.test_client() as client:
        yield client


def test_count_starts_at_zero(client):
    r = client.get("/count")
    assert r.status_code == 200
    assert r.get_json() == {"value": 0}


def test_increment_returns_new_value(client):
    r = client.post("/increment")
    assert r.status_code == 200
    body = r.get_json()
    assert body["value"] == 1
    assert "updated_at" in body


def test_two_increments_differ_by_one(client):
    assert client.post("/increment").get_json()["value"] == 1
    assert client.post("/increment").get_json()["value"] == 2


def test_health_returns_ok(client):
    r = client.get("/health")
    assert r.status_code == 200
    assert r.get_json()["status"] == "ok"