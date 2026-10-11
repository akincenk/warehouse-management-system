import pytest

import create_admin
from tests.conftest import auth_header, make_user


def run(monkeypatch, username, password):
    monkeypatch.setattr("sys.argv", ["create_admin.py", username])
    monkeypatch.setattr("getpass.getpass", lambda prompt="": password)
    create_admin.main()


def test_creates_admin(monkeypatch, client):
    run(monkeypatch, "root", "adminpass1")
    headers = auth_header(client, "root", "adminpass1")
    assert client.get("/users/", headers=headers).status_code == 200


def test_promotes_existing_user(monkeypatch, client):
    make_user("staffer")
    run(monkeypatch, "staffer", "newpass123")
    assert client.get("/auth/me", headers=auth_header(client, "staffer", "newpass123")).json()["role"] == "admin"


def test_rejects_weak_password(monkeypatch):
    with pytest.raises(SystemExit):
        run(monkeypatch, "root", "short")
