"""Registration fee through Razorpay (a fake Razorpay here), registering again before paying, and the company logo."""
import hashlib
import hmac
import json

import pytest

from backend.app.api import auth
from backend.app.core import database
from backend.app.core.config import settings
from backend.app.services import mailer, razorpay

from .conftest import API, PASSWORD, Factory

OWNER = "owner@platform.example.com"
PNG = b"\x89PNG\r\n\x1a\n" + b"picture-bytes"
SECRET = "test-key-secret"
WEBHOOK_SECRET = "test-webhook-secret"


class FakeRazorpay:
    """Stands in for api.razorpay.com: orders, payments made in Checkout, capture."""

    def __init__(self):
        self.orders, self.payments, self.down = {}, {}, False

    def __call__(self, method, path, json=None):
        if self.down:
            raise razorpay.RazorpayError("Razorpay could not be reached (ConnectError). Try again.")
        parts = path.strip("/").split("/")
        if method == "POST" and parts == ["orders"]:
            order = {"id": f"order_{len(self.orders) + 1}", "status": "created", **json}
            self.orders[order["id"]] = order
            return order
        if method == "GET" and parts[0] == "orders":
            return {"items": [p for p in self.payments.values() if p["order_id"] == parts[1]]}
        if method == "GET" and parts[0] == "payments":
            return self.payments[parts[1]]
        if method == "POST" and parts[2:] == ["capture"]:
            self.payments[parts[1]]["status"] = "captured"
            return self.payments[parts[1]]
        raise AssertionError(f"unexpected Razorpay call {method} {path}")

    def pay(self, order_id: str, status: str = "captured", amount: int | None = None) -> dict:
        """What Checkout gives the browser after paying: ids and a signature made with the key secret."""
        payment_id = f"pay_{len(self.payments) + 1}"
        self.payments[payment_id] = {
            "id": payment_id, "order_id": order_id, "amount": amount or self.orders[order_id]["amount"],
            "currency": "INR", "status": status, "method": "upi",
            "error_description": "Payment failed at the bank." if status == "failed" else None,
        }
        signature = hmac.new(SECRET.encode(), f"{order_id}|{payment_id}".encode(), hashlib.sha256).hexdigest()
        return {"razorpay_order_id": order_id, "razorpay_payment_id": payment_id, "razorpay_signature": signature}


@pytest.fixture(autouse=True)
def gateway(monkeypatch):
    monkeypatch.setattr(settings, "REGISTRATION_FEE", 2999)
    monkeypatch.setattr(settings, "RAZORPAY_KEY_ID", "rzp_test_example")
    monkeypatch.setattr(settings, "RAZORPAY_KEY_SECRET", SECRET)
    monkeypatch.setattr(settings, "RAZORPAY_WEBHOOK_SECRET", WEBHOOK_SECRET)
    monkeypatch.setattr(settings, "PLATFORM_OWNER_EMAIL", OWNER)
    fake = FakeRazorpay()
    monkeypatch.setattr(razorpay, "_call", fake)
    return fake


@pytest.fixture
def mails(monkeypatch):
    sent = []
    monkeypatch.setattr(mailer, "send", lambda to, subject, text: sent.append({"to": to, "subject": subject, "text": text}))
    return sent


def register(client, name: str) -> dict:
    email = f"admin@{name}.example.com"
    created = client.post(f"{API}/auth/register", json={
        "organization_name": name, "name": f"{name} admin", "email": email, "password": PASSWORD,
    })
    assert created.status_code == 201, created.text
    token = client.post(f"{API}/auth/login", json={"email": email, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def order(client, headers) -> dict:
    response = client.post(f"{API}/billing/order", headers=headers)
    assert response.status_code == 200, response.text
    return response.json()


def verify(client, headers, paid: dict):
    return client.post(f"{API}/billing/verify", headers=headers, json=paid)


def status_of(client, headers) -> str:
    return client.get(f"{API}/auth/me", headers=headers).json()["organization_status"]


def owner_headers(client) -> dict:
    Factory(client, "platform")  # the owner's own company; the fixture activates it
    database.users.update_one({"email": "admin@platform.example.com"}, {"$set": {"email": OWNER}})
    token = client.post(f"{API}/auth/login", json={"email": OWNER, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_new_company_waits_for_payment(client):
    headers = register(client, "acme")
    assert status_of(client, headers) == "pending_payment"
    for path in ("assets", "documents", "dashboard", "users", "assets/options"):
        assert client.get(f"{API}/{path}", headers=headers).status_code == 402, path
    info = client.get(f"{API}/billing", headers=headers).json()
    assert info["fee"] == 2999 and info["status"] == "pending_payment"
    assert info["configured"] is True and info["test_mode"] is True and info["payments"] == []


def test_no_fee_means_active_at_once(client, monkeypatch):
    monkeypatch.setattr(settings, "REGISTRATION_FEE", 0)
    headers = register(client, "free")
    assert client.get(f"{API}/assets", headers=headers).status_code == 200


def test_no_razorpay_keys_closes_registration(client, monkeypatch):
    """Without keys a new company could never pay, so it is not created at all."""
    monkeypatch.setattr(settings, "RAZORPAY_KEY_SECRET", "")
    assert client.get(f"{API}/billing/fee").json() == {"fee": 2999, "configured": False}
    refused = client.post(f"{API}/auth/register", json={
        "organization_name": "stuck", "name": "stuck admin", "email": "admin@stuck.example.com", "password": PASSWORD,
    })
    assert refused.status_code == 503 and "payments are not set up" in refused.json()["detail"]
    assert database.organizations.find_one({"name": "stuck"}) is None


def test_paying_activates_the_company(client, gateway, mails):
    headers = register(client, "acme")
    checkout = order(client, headers)
    assert checkout["key_id"] == "rzp_test_example" and checkout["amount"] == 299900 and checkout["currency"] == "INR"
    assert gateway.orders[checkout["order_id"]]["amount"] == 299900

    paid = gateway.pay(checkout["order_id"])
    response = verify(client, headers, paid)
    assert response.status_code == 200, response.text
    assert response.json()["organization_status"] == "active"
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
    record = client.get(f"{API}/billing", headers=headers).json()["payments"][0]
    assert record["status"] == "paid" and record["payment_id"] == paid["razorpay_payment_id"] and record["method"] == "upi"
    assert [m["to"] for m in mails] == ["admin@acme.example.com"] and paid["razorpay_payment_id"] in mails[0]["text"]

    assert verify(client, headers, paid).status_code == 200  # reported twice: counted once
    assert len(mails) == 1
    assert client.post(f"{API}/billing/order", headers=headers).status_code == 409


def test_an_unpaid_order_is_reused(client, gateway):
    headers = register(client, "acme")
    assert order(client, headers)["order_id"] == order(client, headers)["order_id"]
    assert len(gateway.orders) == 1


def test_made_up_signature_is_refused(client, gateway):
    headers = register(client, "acme")
    paid = gateway.pay(order(client, headers)["order_id"])
    assert verify(client, headers, {**paid, "razorpay_signature": "0" * 64}).status_code == 400
    assert status_of(client, headers) == "pending_payment"


def test_signature_alone_is_not_enough(client, gateway):
    """A failed or underpaid payment at Razorpay activates nothing, whatever the browser says."""
    headers = register(client, "acme")
    order_id = order(client, headers)["order_id"]
    failed = verify(client, headers, gateway.pay(order_id, status="failed"))
    assert failed.status_code == 402
    assert client.get(f"{API}/billing", headers=headers).json()["payments"][0]["error"] == "Payment failed at the bank."
    assert verify(client, headers, gateway.pay(order_id, amount=100)).status_code == 402
    assert status_of(client, headers) == "pending_payment"


def test_authorised_payment_is_captured(client, gateway):
    headers = register(client, "acme")
    paid = gateway.pay(order(client, headers)["order_id"], status="authorized")
    assert verify(client, headers, paid).status_code == 200
    assert gateway.payments[paid["razorpay_payment_id"]]["status"] == "captured"
    assert status_of(client, headers) == "active"


def test_another_companys_order_is_refused(client, gateway):
    first, second = register(client, "acme"), register(client, "other")
    paid = gateway.pay(order(client, first)["order_id"])
    assert verify(client, second, paid).status_code == 404
    assert status_of(client, second) == "pending_payment"


def test_payment_counts_when_the_browser_closed(client, gateway):
    """Paid, but Checkout never reported back: the payment page asks Razorpay about the open order."""
    headers = register(client, "acme")
    gateway.pay(order(client, headers)["order_id"])
    assert client.get(f"{API}/billing", headers=headers).json()["status"] == "active"


def test_webhook_activates_the_company(client, gateway):
    headers = register(client, "acme")
    paid = gateway.pay(order(client, headers)["order_id"])
    entity = gateway.payments[paid["razorpay_payment_id"]]
    event = json.dumps({"event": "payment.captured", "payload": {"payment": {"entity": entity}}})
    forged = client.post(f"{API}/billing/webhook", content=event, headers={"X-Razorpay-Signature": "0" * 64})
    assert forged.status_code == 400 and status_of(client, headers) == "pending_payment"
    signature = hmac.new(WEBHOOK_SECRET.encode(), event.encode(), hashlib.sha256).hexdigest()
    assert client.post(f"{API}/billing/webhook", content=event, headers={"X-Razorpay-Signature": signature}).status_code == 200
    assert status_of(client, headers) == "active"


def test_razorpay_down_is_reported(client, gateway):
    headers = register(client, "acme")
    gateway.down = True
    response = client.post(f"{API}/billing/order", headers=headers)
    assert response.status_code == 502 and "could not be reached" in response.json()["detail"]


def test_only_the_administrator_pays(client):
    register(client, "acme")
    admin = database.users.find_one({"email": "admin@acme.example.com"})
    auth._new_user(admin["organization_id"], "acme viewer", "viewer@acme.example.com", PASSWORD, "viewer")
    token = client.post(f"{API}/auth/login", json={"email": "viewer@acme.example.com", "password": PASSWORD}).json()["access_token"]
    assert client.post(f"{API}/billing/order", headers={"Authorization": f"Bearer {token}"}).status_code == 403


def test_owner_sees_every_payment(client, gateway):
    headers = register(client, "acme")
    verify(client, headers, gateway.pay(order(client, headers)["order_id"]))
    register(client, "unpaid")
    order(client, register(client, "later"))
    owner = owner_headers(client)
    every = client.get(f"{API}/platform/payments", headers=owner).json()
    assert every["total"] == 2
    paid = client.get(f"{API}/platform/payments", headers=owner, params={"status": "paid"}).json()["items"]
    assert [p["organization_name"] for p in paid] == ["acme"]
    assert client.get(f"{API}/platform/payments", headers=headers).status_code == 403


def test_registering_again_continues_an_unpaid_registration(client):
    """Same email and password before paying: the same company, not a second one."""
    register(client, "acme")
    again = client.post(f"{API}/auth/register", json={
        "organization_name": "Acme Industries", "name": "acme owner", "email": "admin@acme.example.com", "password": PASSWORD,
    })
    assert again.status_code == 200, again.text
    assert again.json()["organization_name"] == "Acme Industries"
    assert database.organizations.count_documents({"name": {"$in": ["acme", "Acme Industries"]}}) == 1

    wrong = client.post(f"{API}/auth/register", json={
        "organization_name": "takeover", "name": "someone", "email": "admin@acme.example.com", "password": "another-password-1",
    })
    assert wrong.status_code == 409 and "same password" in wrong.json()["detail"]
    assert database.organizations.find_one({"name": "takeover"}) is None


def test_active_company_email_cannot_register_again(client):
    factory = Factory(client, "active")
    again = client.post(f"{API}/auth/register", json={
        "organization_name": "active", "name": "someone", "email": "admin@active.example.com", "password": PASSWORD,
    })
    assert again.status_code == 409 and "Sign in instead" in again.json()["detail"]
    assert factory


def test_company_logo(client):
    headers = register(client, "acme")
    assert client.get(f"{API}/auth/me", headers=headers).json()["organization_logo_url"] is None
    uploaded = client.put(f"{API}/organization/logo", headers=headers, files={"file": ("logo.png", PNG, "image/png")})
    assert uploaded.status_code == 200, uploaded.text
    url = client.get(f"{API}/auth/me", headers=headers).json()["organization_logo_url"]
    assert url == uploaded.json()["logo_url"]
    picture = client.get(url)  # no login needed: an <img> cannot send one
    assert picture.content == PNG and picture.headers["content-type"] == "image/png"
    assert client.put(f"{API}/organization/logo", headers=headers, files={"file": ("x.svg", b"<svg/>", "image/svg+xml")}).status_code == 415
    big = PNG + b"x" * (513 * 1024)
    assert client.put(f"{API}/organization/logo", headers=headers, files={"file": ("big.png", big, "image/png")}).status_code == 413
    assert client.delete(f"{API}/organization/logo", headers=headers).status_code == 204
    assert client.get(url).status_code == 404


def test_only_the_administrator_changes_the_logo(client, factory):
    viewer = factory.user("viewer")
    response = client.put(f"{API}/organization/logo", headers=viewer, files={"file": ("logo.png", PNG, "image/png")})
    assert response.status_code == 403
