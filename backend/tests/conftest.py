import os
import tempfile

_db_dir = tempfile.mkdtemp()
os.environ["DATABASE_URL"] = f"sqlite:///{_db_dir}/test.db"
os.environ["JWT_SECRET"] = "test-secret-" + "x" * 32

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from auth.security import hash_password  # noqa: E402
from database import Base, SessionLocal, engine  # noqa: E402
from main import app  # noqa: E402
from models import User  # noqa: E402


@pytest.fixture(autouse=True)
def fresh_db():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield


@pytest.fixture
def client():
    return TestClient(app)


def make_user(username: str, password: str = "password123", role: str = "staff") -> None:
    with SessionLocal() as db:
        db.add(User(username=username, password=hash_password(password), role=role))
        db.commit()


def auth_header(client: TestClient, username: str, password: str = "password123") -> dict:
    r = client.post("/auth/login", data={"username": username, "password": password})
    assert r.status_code == 200, r.text
    return {"Authorization": f"Bearer {r.json()['access_token']}"}


@pytest.fixture
def staff(client):
    make_user("staff1")
    return auth_header(client, "staff1")


@pytest.fixture
def admin(client):
    make_user("admin1", role="admin")
    return auth_header(client, "admin1")
