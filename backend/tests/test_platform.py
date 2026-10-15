"""The platform owner's console: every company, and no factory workspace of the owner's own."""
import pytest

from backend.app.core import database
from backend.app.core.config import settings

from .conftest import API, PASSWORD, Factory

OWNER = "owner@platform.example.com"


@pytest.fixture
def owner(client, monkeypatch):
    monkeypatch.setattr(settings, "PLATFORM_OWNER_EMAIL", OWNER)
    Factory(client, "platform")  # the company record that holds the owner's account
    database.users.update_one({"email": "admin@platform.example.com"}, {"$set": {"email": OWNER}})
    token = client.post(f"{API}/auth/login", json={"email": OWNER, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_owner_never_enters_a_company(client, owner):
    me = client.get(f"{API}/auth/me", headers=owner).json()
    assert me["platform_owner"] is True
    for path in ("dashboard", "assets", "documents", "breakdowns", "work-orders", "users", "audit", "assets/options"):
        response = client.get(f"{API}/{path}", headers=owner)
        assert response.status_code == 403, path
        assert "no factory workspace" in response.json()["detail"]
    assert client.post(f"{API}/assets", headers=owner, json={"asset_code": "X-1", "name": "Machine"}).status_code == 403


def test_owner_sees_every_company_but_not_the_own_record(client, owner, factory, other_factory):
    factory.asset("CNC-01")
    factory.user("technician")
    database.organizations.update_one({"name": "beta"}, {"$set": {"status": "pending_payment"}})

    data = client.get(f"{API}/platform/companies", headers=owner).json()
    names = {c["name"]: c for c in data["items"]}
    assert set(names) == {"alpha", "beta"}
    alpha = names["alpha"]
    assert alpha["admin_email"] == "admin@alpha.example.com"
    assert (alpha["users"], alpha["assets"], alpha["status"]) == (2, 1, "active")
    assert data["summary"] == {"companies": 2, "active": 1, "pending_payment": 1, "users": 3}

    waiting = client.get(f"{API}/platform/companies", headers=owner, params={"status": "pending_payment"}).json()
    assert [c["name"] for c in waiting["items"]] == ["beta"]
    found = client.get(f"{API}/platform/companies", headers=owner, params={"q": "ALP"}).json()
    assert [c["name"] for c in found["items"]] == ["alpha"]


def test_only_the_owner_sees_the_companies(client, owner, factory):
    assert client.get(f"{API}/platform/companies", headers=factory.admin).status_code == 403
    assert client.get(f"{API}/platform/companies").status_code == 401
