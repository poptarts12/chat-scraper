# tests/test_conversations.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def auth_header():
    # register + login to get a token
    email = "conv_user@example.com"
    client.post("/auth/register", json={"email": email, "password": "Pwd123!"})
    login = client.post("/auth/login", json={"email": email, "password": "Pwd123!"})
    token = login.json()["access_token"]
    return {"Authorization": f"Bearer {token}"}

def test_create_conversation(auth_header):
    payload = {"user_id": login_id := None, "title": "My First Chat"}
    # fetch user_id from /auth/login response
    login = client.post("/auth/login", json={"email": "conv_user@example.com", "password": "Pwd123!"})
    payload["user_id"] = login.json()["user_id"]
    r = client.post("/conversations/", json=payload, headers=auth_header)
    assert r.status_code == 201
    data = r.json()
    assert "conversation_id" in data
    assert data["title"] == payload["title"]

def test_update_conversation_success(auth_header):
    # create
    login = client.post("/auth/login", json={"email": "conv_user@example.com", "password": "Pwd123!"})
    user_id = login.json()["user_id"]
    create = client.post("/conversations/", json={"user_id": user_id, "title": "Old"}, headers=auth_header)
    cid = create.json()["conversation_id"]
    # update
    upd = client.put(f"/conversations/{cid}", json={"title": "New Title"}, headers=auth_header)
    assert upd.status_code == 200
    assert upd.json()["title"] == "New Title"

def test_update_conversation_not_found(auth_header):
    r = client.put("/conversations/00000000-0000-0000-0000-000000000000", json={"title": "X"}, headers=auth_header)
    assert r.status_code == 404
