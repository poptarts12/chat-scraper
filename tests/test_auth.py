# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from app.main import app  # adjust import path if needed

client = TestClient(app)

@pytest.fixture(autouse=True)
def setup_db():
    """
    (Optional) Reset or re-create your test DB here.
    If using SQLite in-memory, ensure your app uses it for tests.
    """
    yield
    # teardown logic if needed

def test_register_user_success():
    payload = {"email": "unit1@example.com", "password": "TestPass123!"}
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert "user_id" in data
    assert data["email"] == payload["email"]

def test_register_user_duplicate():
    payload = {"email": "unit2@example.com", "password": "TestPass123!"}
    # first time
    r1 = client.post("/auth/register", json=payload)
    assert r1.status_code == 201
    # duplicate
    r2 = client.post("/auth/register", json=payload)
    assert r2.status_code == 400
    assert "already exists" in r2.json()["detail"].lower()

def test_login_user_success():
    reg = client.post("/auth/register", json={"email": "unit3@example.com", "password": "Secret!"})
    assert reg.status_code == 201
    resp = client.post("/auth/login", json={"email": "unit3@example.com", "password": "Secret!"})
    assert resp.status_code == 200
    data = resp.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_login_user_failure():
    resp = client.post("/auth/login", json={"email": "noone@example.com", "password": "bad"})
    assert resp.status_code == 401
