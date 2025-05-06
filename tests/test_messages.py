# tests/test_messages.py

import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

@pytest.fixture
def setup_chat():
    # register + login
    email = "msg_user@example.com"
    client.post("/auth/register", json={"email": email, "password": "Pwd123!"})
    login = client.post("/auth/login", json={"email": email, "password": "Pwd123!"})
    token = login.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    user_id = login.json()["user_id"]
    # create conversation
    conv = client.post("/conversations/", json={"user_id": user_id, "title": "Chat"}, headers=headers)
    cid = conv.json()["conversation_id"]
    return headers, cid

def test_create_message_success(setup_chat):
    headers, cid = setup_chat
    payload = {
        "conversation_id": cid,
        "sender_type": "user",
        "content": "Hello!",
        "order_index": 1
    }
    r = client.post("/messages/", json=payload, headers=headers)
    assert r.status_code == 201
    data = r.json()
    assert data["content"] == "Hello!"
    assert data["order_index"] == 1

def test_create_message_duplicate(setup_chat):
    headers, cid = setup_chat
    payload = {
        "conversation_id": cid,
        "sender_type": "user",
        "content": "Dup",
        "order_index": 1
    }
    client.post("/messages/", json=payload, headers=headers)
    r2 = client.post("/messages/", json=payload, headers=headers)
    assert r2.status_code == 400

def test_get_messages(setup_chat):
    headers, cid = setup_chat
    # post two messages
    client.post("/messages/", json={"conversation_id": cid, "sender_type": "user", "content": "A", "order_index": 1}, headers=headers)
    client.post("/messages/", json={"conversation_id": cid, "sender_type": "chatbot", "content": "B", "order_index": 2}, headers=headers)
    r = client.get(f"/messages/conversations/{cid}/messages", headers=headers)
    assert r.status_code == 200
    arr = r.json()
    assert isinstance(arr, list)
    assert len(arr) == 2
    assert arr[0]["order_index"] == 1
    assert arr[1]["order_index"] == 2
