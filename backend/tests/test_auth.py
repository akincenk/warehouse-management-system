from datetime import UTC, datetime, timedelta

import jwt

from auth import security
from database import SessionLocal
from models import User


def test_register_creates_staff_and_hashes_password(client):
    r = client.post("/auth/register", json={"username": "alice", "password": "s3cretpass", "role": "admin"})
    assert r.status_code == 201
    body = r.json()
    assert body["role"] == "staff"  # client cannot self-assign admin
    assert "password" not in body
    with SessionLocal() as db:
        stored = db.query(User).filter_by(username="alice").one().password
    assert stored != "s3cretpass" and stored.startswith("$2")


def test_duplicate_username_returns_409(client):
    payload = {"username": "bob", "password": "password123"}
    assert client.post("/auth/register", json=payload).status_code == 201
    assert client.post("/auth/register", json=payload).status_code == 409


def test_register_validation(client):
    assert client.post("/auth/register", json={"username": "ab", "password": "password123"}).status_code == 422
    assert client.post("/auth/register", json={"username": "carol", "password": "short"}).status_code == 422
    assert client.post("/auth/register", json={"username": "carol", "password": "x" * 73}).status_code == 422


def test_login_and_me(client):
    client.post("/auth/register", json={"username": "dave", "password": "password123"})
    r = client.post("/auth/login", data={"username": "dave", "password": "password123"})
    assert r.status_code == 200
    token = r.json()["access_token"]
    me = client.get("/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert me.status_code == 200
    assert me.json()["username"] == "dave"


def test_login_wrong_password(client):
    client.post("/auth/register", json={"username": "erin", "password": "password123"})
    assert client.post("/auth/login", data={"username": "erin", "password": "nope-nope"}).status_code == 401
    assert client.post("/auth/login", data={"username": "ghost", "password": "password123"}).status_code == 401


def test_protected_routes_require_token(client):
    assert client.get("/auth/me").status_code == 401
    assert client.get("/products/").status_code == 401
    assert client.get("/products/", headers={"Authorization": "Bearer garbage"}).status_code == 401


def test_expired_token_rejected(client, staff):
    expired = jwt.encode(
        {"sub": "staff1", "exp": datetime.now(UTC) - timedelta(minutes=1)},
        security.SECRET_KEY,
        algorithm=security.ALGORITHM,
    )
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {expired}"}).status_code == 401


def test_token_signed_with_other_key_rejected(client, staff):
    forged = jwt.encode({"sub": "staff1"}, "another-secret-" + "y" * 32, algorithm="HS256")
    assert client.get("/auth/me", headers={"Authorization": f"Bearer {forged}"}).status_code == 401
