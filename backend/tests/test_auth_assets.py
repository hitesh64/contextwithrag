from datetime import timedelta

from backend.app.core import database
from backend.app.core.utils import now

from .conftest import API, PASSWORD, Factory


def test_health_is_public(client):
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"
    assert response.headers["x-request-id"]


def test_protected_apis_need_a_login(client):
    for path in ("assets", "documents", "breakdowns", "work-orders", "audit", "dashboard", "users", "auth/me"):
        assert client.get(f"{API}/{path}").status_code == 401, path
    assert client.post(f"{API}/chat", json={"question": "anything"}).status_code == 401
    assert client.get(f"{API}/assets", headers={"Authorization": "Bearer made-up"}).status_code == 401


def test_register_login_and_me(client, factory):
    me = client.get(f"{API}/auth/me", headers=factory.admin).json()
    assert me["role"] == "admin"
    assert me["organization_name"] == "alpha"
    assert "password_hash" not in me
    stored = database.users.find_one({"email": "admin@alpha.example.com"})
    assert stored["password_hash"] != PASSWORD and stored["password_hash"].startswith("$2")


def test_wrong_password_and_duplicate_email(client, factory):
    wrong = client.post(f"{API}/auth/login", json={"email": "admin@alpha.example.com", "password": "wrong-password"})
    assert wrong.status_code == 401
    unknown = client.post(f"{API}/auth/login", json={"email": "nobody@alpha.example.com", "password": PASSWORD})
    assert unknown.status_code == 401
    again = client.post(f"{API}/auth/register", json={
        "organization_name": "copy", "name": "Someone", "email": "admin@alpha.example.com", "password": PASSWORD,
    })
    assert again.status_code == 409
    assert database.organizations.count_documents({}) == 1


def test_login_attempts_are_rate_limited(client, factory):
    from backend.app.api import auth

    auth.login_limiter.reset()
    auth.login_limiter.limit = 3
    try:
        codes = [
            client.post(f"{API}/auth/login", json={"email": "admin@alpha.example.com", "password": "wrong-password"}).status_code
            for _ in range(4)
        ]
    finally:
        auth.login_limiter.limit = 1000
    assert codes == [401, 401, 401, 429]


def test_expired_and_logged_out_tokens_stop_working(client, factory):
    database.login_sessions.update_many({}, {"$set": {"expires_at": now() - timedelta(seconds=1)}})
    assert client.get(f"{API}/auth/me", headers=factory.admin).status_code == 401

    headers = factory.login("admin@alpha.example.com")
    assert client.post(f"{API}/auth/logout", headers=headers).status_code == 204
    assert client.get(f"{API}/auth/me", headers=headers).status_code == 401


def test_deactivated_user_is_locked_out_at_once(client, factory):
    technician = factory.user("technician")
    user_id = client.get(f"{API}/auth/me", headers=technician).json()["id"]
    assert client.patch(f"{API}/users/{user_id}", headers=factory.admin, json={"is_active": False}).status_code == 200
    assert client.get(f"{API}/assets", headers=technician).status_code == 401
    login = client.post(f"{API}/auth/login", json={"email": database.users.find_one({"role": "technician"})["email"], "password": PASSWORD})
    assert login.status_code == 403


def test_admin_cannot_lock_themselves_out(client, factory):
    me = client.get(f"{API}/auth/me", headers=factory.admin).json()
    assert client.patch(f"{API}/users/{me['id']}", headers=factory.admin, json={"is_active": False}).status_code == 409
    assert client.patch(f"{API}/users/{me['id']}", headers=factory.admin, json={"role": "viewer"}).status_code == 409


def test_roles_limit_what_a_user_can_do(client, factory):
    viewer, technician, manager = factory.user("viewer"), factory.user("technician"), factory.user("maintenance_manager")
    body = {"asset_code": "P-1", "name": "Press"}
    assert client.post(f"{API}/assets", headers=viewer, json=body).status_code == 403
    assert client.post(f"{API}/assets", headers=technician, json=body).status_code == 403
    assert client.post(f"{API}/assets", headers=manager, json=body).status_code == 201
    assert client.get(f"{API}/assets", headers=viewer).status_code == 200
    # Only an administrator manages users; only managers and above read the audit trail
    assert client.get(f"{API}/users", headers=manager).status_code == 403
    assert client.get(f"{API}/audit", headers=technician).status_code == 403
    assert client.get(f"{API}/audit", headers=manager).status_code == 200


def test_users_of_another_organization_cannot_be_managed(client, factory, other_factory):
    outsider = client.get(f"{API}/auth/me", headers=other_factory.admin).json()
    assert client.patch(f"{API}/users/{outsider['id']}", headers=factory.admin, json={"role": "viewer"}).status_code == 404
    listed = client.get(f"{API}/users", headers=factory.admin).json()
    assert [u["email"] for u in listed["items"]] == ["admin@alpha.example.com"]


def test_asset_lifecycle(client, factory):
    asset = factory.asset("cnc-01", name="CNC Lathe", location="Bay 2")
    assert asset["asset_code"] == "CNC-01"
    factory.asset("PRESS-07", name="Hydraulic Press", location="Bay 5")

    assert client.get(f"{API}/assets", headers=factory.admin, params={"q": "lathe"}).json()["total"] == 1
    assert client.get(f"{API}/assets", headers=factory.admin, params={"q": "bay"}).json()["total"] == 2

    updated = client.patch(f"{API}/assets/{asset['id']}", headers=factory.admin, json={"criticality": "critical"})
    assert updated.json()["criticality"] == "critical"
    # The code is the machine's identity and is not part of the update schema
    assert client.patch(f"{API}/assets/{asset['id']}", headers=factory.admin, json={"asset_code": "X-1"}).status_code == 422

    assert client.post(f"{API}/assets/{asset['id']}/archive", headers=factory.admin).json()["status"] == "archived"
    assert [a["asset_code"] for a in client.get(f"{API}/assets", headers=factory.admin).json()["items"]] == ["PRESS-07"]
    assert client.get(f"{API}/assets", headers=factory.admin, params={"status": "archived"}).json()["total"] == 1


def test_invalid_and_duplicate_asset_codes_are_rejected(client, factory):
    factory.asset("CNC-01")
    duplicate = client.post(f"{API}/assets", headers=factory.admin, json={"asset_code": "cnc-01", "name": "Again"})
    assert duplicate.status_code == 409
    for bad in ("", "A", "has space", "-LEADING", "X" * 40, "semi;colon"):
        response = client.post(f"{API}/assets", headers=factory.admin, json={"asset_code": bad, "name": "Machine"})
        assert response.status_code == 422, bad
    missing_name = client.post(f"{API}/assets", headers=factory.admin, json={"asset_code": "OK-1"})
    assert missing_name.status_code == 422


def test_the_browser_cannot_choose_the_organization(client, factory, other_factory):
    """organization_id in a request body is refused, and the same code may exist in two factories."""
    smuggled = client.post(f"{API}/assets", headers=factory.admin, json={
        "asset_code": "CNC-01", "name": "Machine", "organization_id": other_factory.organization_id,
    })
    assert smuggled.status_code == 422
    mine, theirs = factory.asset("CNC-01"), other_factory.asset("CNC-01")
    assert mine["organization_id"] == factory.organization_id
    assert theirs["organization_id"] == other_factory.organization_id


def test_assets_are_invisible_across_organizations(client, factory, other_factory):
    asset = factory.asset("CNC-01")
    assert client.get(f"{API}/assets", headers=other_factory.admin).json()["total"] == 0
    assert client.get(f"{API}/assets/{asset['id']}", headers=other_factory.admin).status_code == 404
    assert client.patch(f"{API}/assets/{asset['id']}", headers=other_factory.admin, json={"name": "Stolen"}).status_code == 404
    assert client.post(f"{API}/assets/{asset['id']}/archive", headers=other_factory.admin).status_code == 404
    assert client.get(f"{API}/assets/not-an-id", headers=factory.admin).status_code == 404


def test_second_factory_helper_is_independent(client):
    first, second = Factory(client, "gamma"), Factory(client, "delta")
    assert first.organization_id != second.organization_id
