import pytest

from tests.conftest import auth_header, make_user


@pytest.fixture
def manager(client):
    make_user("mgr", role="manager")
    return auth_header(client, "mgr")


def test_product_crud_as_manager(client, staff, manager):
    r = client.post("/products/", json={"name": "Pallet", "quantity": 10}, headers=manager)
    assert r.status_code == 201
    pid = r.json()["id"]

    # staff can read
    assert client.get("/products/", headers=staff).json() == [{"id": pid, "name": "Pallet", "quantity": 10}]
    assert client.get(f"/products/{pid}", headers=staff).json()["name"] == "Pallet"

    r = client.patch(f"/products/{pid}", json={"quantity": 4}, headers=manager)
    assert r.status_code == 200
    assert r.json() == {"id": pid, "name": "Pallet", "quantity": 4}

    assert client.delete(f"/products/{pid}", headers=manager).status_code == 204
    assert client.get(f"/products/{pid}", headers=staff).status_code == 404


def test_staff_is_read_only(client, staff, manager):
    pid = client.post("/products/", json={"name": "Crate", "quantity": 1}, headers=manager).json()["id"]
    assert client.post("/products/", json={"name": "Box", "quantity": 1}, headers=staff).status_code == 403
    assert client.patch(f"/products/{pid}", json={"quantity": 9}, headers=staff).status_code == 403
    assert client.delete(f"/products/{pid}", headers=staff).status_code == 403
    assert client.get(f"/products/{pid}", headers=staff).json()["quantity"] == 1


def test_admin_can_manage_products(client, admin):
    pid = client.post("/products/", json={"name": "Bin", "quantity": 2}, headers=admin).json()["id"]
    assert client.patch(f"/products/{pid}", json={"name": "Big bin"}, headers=admin).json()["name"] == "Big bin"
    assert client.delete(f"/products/{pid}", headers=admin).status_code == 204


def test_product_validation(client, manager):
    assert client.post("/products/", json={"name": "", "quantity": 1}, headers=manager).status_code == 422
    assert client.post("/products/", json={"name": "Box", "quantity": -1}, headers=manager).status_code == 422
    assert client.patch("/products/999", json={"quantity": 1}, headers=manager).status_code == 404


def test_user_list_admin_only(client, staff, admin):
    assert client.get("/users/", headers=staff).status_code == 403
    r = client.get("/users/", headers=admin)
    assert r.status_code == 200
    assert {u["username"] for u in r.json()} == {"staff1", "admin1"}


def test_admin_sets_role(client, staff, admin):
    staff_id = next(u["id"] for u in client.get("/users/", headers=admin).json() if u["username"] == "staff1")
    assert client.patch(f"/users/{staff_id}/role", json={"role": "manager"}, headers=staff).status_code == 403
    assert client.patch(f"/users/{staff_id}/role", json={"role": "boss"}, headers=admin).status_code == 422
    r = client.patch(f"/users/{staff_id}/role", json={"role": "manager"}, headers=admin)
    assert r.status_code == 200 and r.json()["role"] == "manager"


def test_cors_allows_frontend_origin(client):
    r = client.options(
        "/products/",
        headers={"Origin": "http://localhost:3000", "Access-Control-Request-Method": "GET"},
    )
    assert r.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert "access-control-allow-credentials" not in r.headers
