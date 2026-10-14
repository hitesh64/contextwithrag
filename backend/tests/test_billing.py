"""Registration fee by UPI: QR code, proof checks, the platform owner's review, mails, and the company logo."""
import json
import re
from datetime import timedelta

import pytest

from backend.app.api import billing
from backend.app.core import database
from backend.app.core.config import settings
from backend.app.core.utils import now
from backend.app.services import llm, mailer

from .conftest import API, PASSWORD, Factory

OWNER = "owner@platform.example.com"
PNG = b"\x89PNG\r\n\x1a\n" + b"picture-bytes"


@pytest.fixture(autouse=True)
def fee(monkeypatch):
    monkeypatch.setattr(settings, "REGISTRATION_FEE", 2999)
    monkeypatch.setattr(settings, "UPI_ID", "owner@okbank")
    monkeypatch.setattr(settings, "UPI_PAYEE_NAME", "Platform Owner")
    monkeypatch.setattr(settings, "PLATFORM_OWNER_EMAIL", OWNER)
    billing.proof_limiter.reset()


@pytest.fixture
def mails(monkeypatch):
    sent = []
    def send(to, subject, text, html_body=None, attachment=None):
        sent.append({"to": to, "subject": subject, "text": text, "html": html_body, "attachment": attachment})

    monkeypatch.setattr(mailer, "send", send)
    return sent


class Screenshot:
    """Stands in for Gemini reading a screenshot: set .read to a dict or an exception."""

    def __init__(self):
        self.calls = 0
        self.read = {}
        self.prompts = []

    def __call__(self, prompt, system, image, mime_type):
        self.calls += 1
        self.prompts.append(prompt)
        if isinstance(self.read, Exception):
            raise self.read
        return json.dumps(self.read)


@pytest.fixture
def screenshot(monkeypatch):
    fake = Screenshot()
    monkeypatch.setattr(llm, "generate_with_image", fake)
    return fake


def good_read(utr: str) -> dict:
    return {
        "is_upi_payment_screenshot": True, "status": "success", "amount": 2999, "utr": utr,
        "payee_upi_id": "owner@okbank", "payee_name": "Platform Owner",
        "paid_on": now().date().isoformat(), "note": None, "signs_of_editing": [],
    }


def register(client, name: str) -> dict:
    email = f"admin@{name}.example.com"
    created = client.post(f"{API}/auth/register", json={
        "organization_name": name, "name": f"{name} admin", "email": email, "password": PASSWORD,
    })
    assert created.status_code == 201, created.text
    token = client.post(f"{API}/auth/login", json={"email": email, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def prove(client, headers, utr: str, picture: bytes = PNG, kind: str = "image/png"):
    return client.post(f"{API}/billing/proof", headers=headers, data={"utr": utr}, files={"screenshot": ("pay.png", picture, kind)})


def owner_headers(client) -> dict:
    Factory(client, "platform")  # the owner's own company; the fixture activates it
    database.users.update_one({"email": "admin@platform.example.com"}, {"$set": {"email": OWNER}})
    token = client.post(f"{API}/auth/login", json={"email": OWNER, "password": PASSWORD}).json()["access_token"]
    return {"Authorization": f"Bearer {token}"}


def test_new_company_waits_for_payment(client):
    headers = register(client, "acme")
    me = client.get(f"{API}/auth/me", headers=headers).json()
    assert me["organization_status"] == "pending_payment"
    for path in ("assets", "documents", "dashboard", "users", "assets/options"):
        assert client.get(f"{API}/{path}", headers=headers).status_code == 402, path
    info = client.get(f"{API}/billing", headers=headers).json()
    assert info["fee"] == 2999 and info["status"] == "pending_payment"
    assert info["upi_uri"].startswith("upi://pay?pa=owner@okbank&") and "am=2999.00" in info["upi_uri"]
    assert info["reference"] in info["upi_uri"]
    assert info["qr_svg"].startswith("<svg")


def test_no_fee_means_active_at_once(client, monkeypatch):
    monkeypatch.setattr(settings, "REGISTRATION_FEE", 0)
    headers = register(client, "free")
    assert client.get(f"{API}/assets", headers=headers).status_code == 200


def test_no_upi_id_closes_registration(client, monkeypatch):
    """Without a UPI ID a new company could never pay, so it is not created at all."""
    monkeypatch.setattr(settings, "UPI_ID", "")
    assert client.get(f"{API}/billing/fee").json() == {"fee": 2999, "configured": False}
    refused = client.post(f"{API}/auth/register", json={
        "organization_name": "stuck", "name": "stuck admin", "email": "admin@stuck.example.com", "password": PASSWORD,
    })
    assert refused.status_code == 503 and "payments are not set up" in refused.json()["detail"]
    assert database.organizations.find_one({"name": "stuck"}) is None


def accept(client, owner: dict, payment: dict) -> dict:
    decided = client.post(f"{API}/platform/payments/{payment['id']}/decision", headers=owner, json={"decision": "accept"})
    assert decided.status_code == 200, decided.text
    return decided.json()


def test_correct_proof_still_waits_for_the_owner(client, screenshot, mails):
    """A made-up screenshot can pass every check, so only the owner, who sees the bank account, accepts."""
    headers = register(client, "acme")
    screenshot.read = good_read("123456789012")
    response = prove(client, headers, "1234 5678 9012")
    assert response.status_code == 201, response.text
    body = response.json()
    assert body["payment"]["status"] == "needs_review" and body["payment"]["checks_passed"] is True
    assert body["organization_status"] == "pending_payment"
    assert all(c["ok"] for c in body["payment"]["checks"])
    # The model's own idea of today is out of date: it is told the date, so a payment made today is not "future"
    assert f"Today is {now().date().isoformat()}" in screenshot.prompts[0]
    assert "screenshot" not in body["payment"]
    assert client.get(f"{API}/assets", headers=headers).status_code == 402
    assert [m["to"] for m in mails] == [OWNER] and "Payment to confirm" in mails[0]["subject"]
    assert prove(client, headers, "123456789012").status_code == 409  # waits for the owner

    accept(client, owner_headers(client), body["payment"])
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
    company = [m for m in mails if m["to"] == "admin@acme.example.com"]
    assert len(company) == 1 and "acme is registered on ContextBasedRAG" in company[0]["subject"]
    assert prove(client, headers, "123456789012").status_code == 409  # already active


@pytest.mark.parametrize("change, failed", [
    ({"amount": 299}, "amount"),
    ({"status": "failed"}, "status"),
    ({"utr": "999999999999"}, "utr_matches"),
    ({"payee_upi_id": "someone@else"}, "payee"),
    ({"is_upi_payment_screenshot": False}, "receipt"),
])
def test_wrong_proof_is_rejected(client, screenshot, mails, change, failed):
    headers = register(client, "acme")
    screenshot.read = {**good_read("123456789012"), **change}
    body = prove(client, headers, "123456789012").json()
    assert body["payment"]["status"] == "rejected" and body["organization_status"] == "pending_payment"
    assert [c["key"] for c in body["payment"]["checks"] if c["ok"] is False] == [failed]
    assert client.get(f"{API}/assets", headers=headers).status_code == 402
    assert not mails


def test_payment_dated_before_registration_is_rejected(client, screenshot):
    headers = register(client, "acme")
    screenshot.read = {**good_read("123456789012"), "paid_on": (now() - timedelta(days=3)).date().isoformat()}
    body = prove(client, headers, "123456789012").json()
    assert body["payment"]["status"] == "rejected"


def test_payment_timed_later_than_now_is_rejected(client, screenshot):
    """A screenshot showing a time that has not come yet cannot be a real payment."""
    headers = register(client, "acme")
    later = now() + timedelta(hours=1)
    screenshot.read = {**good_read("123456789012"), "paid_on": later.date().isoformat(), "paid_at": f"{later:%H:%M}"}
    payment = prove(client, headers, "123456789012").json()["payment"]
    assert payment["status"] == "rejected"
    assert [c["key"] for c in payment["checks"] if c["ok"] is False] == ["date"]


def test_payment_with_a_minute_of_clock_drift_passes(client, screenshot):
    headers = register(client, "acme")
    screenshot.read = {**good_read("123456789012"), "paid_at": f"{now() + timedelta(minutes=1):%H:%M}"}
    payment = prove(client, headers, "123456789012").json()["payment"]
    assert payment["status"] == "needs_review" and payment["checks_passed"] is True


def test_another_companys_reference_is_rejected(client, screenshot):
    headers = register(client, "acme")
    reference = client.get(f"{API}/billing", headers=headers).json()["reference"]
    screenshot.read = {**good_read("123456789012"), "references": ["CBR000000"]}
    payment = prove(client, headers, "123456789012").json()["payment"]
    assert payment["status"] == "rejected"
    assert [c["key"] for c in payment["checks"] if c["ok"] is False] == ["reference"]

    screenshot.read = {**good_read("222222222222"), "note": f"ContextBasedRAG {reference}"}
    payment = prove(client, headers, "222222222222", PNG + b"2").json()["payment"]
    assert payment["status"] == "needs_review" and payment["checks_passed"] is True


def test_reused_utr_or_screenshot_is_rejected_without_a_model_call(client, screenshot):
    first = register(client, "acme")
    screenshot.read = good_read("123456789012")
    accept(client, owner_headers(client), prove(client, first, "123456789012").json()["payment"])
    calls = screenshot.calls

    second = register(client, "copycat")
    same_utr = prove(client, second, "123456789012", PNG + b"other").json()["payment"]
    assert same_utr["status"] == "rejected" and same_utr["checks"][0]["ok"] is False
    same_picture = prove(client, second, "222222222222").json()["payment"]
    assert same_picture["status"] == "rejected" and same_picture["checks"][1]["ok"] is False
    assert screenshot.calls == calls


def test_doubtful_proof_goes_to_the_owner(client, screenshot, mails):
    headers = register(client, "acme")
    screenshot.read = {**good_read("123456789012"), "signs_of_editing": ["digits in a different font"]}
    payment = prove(client, headers, "123456789012").json()["payment"]
    assert payment["status"] == "needs_review" and payment["checks_passed"] is False
    assert "check found problems" in mails[0]["subject"]
    assert client.get(f"{API}/platform/payments", headers=headers).status_code == 403

    owner = owner_headers(client)
    listed = client.get(f"{API}/platform/payments", headers=owner, params={"status": "needs_review"}).json()
    assert [p["id"] for p in listed["items"]] == [payment["id"]]
    picture = client.get(f"{API}/platform/payments/{payment['id']}/screenshot", headers=owner)
    assert picture.content == PNG and picture.headers["content-type"] == "image/png"
    assert accept(client, owner, payment)["status"] == "accepted"
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
    assert any("registered" in m["subject"] for m in mails if m["to"] == "admin@acme.example.com")


def test_model_failure_needs_review(client, screenshot):
    headers = register(client, "acme")
    screenshot.read = llm.QuotaError("The request quota of the Gemini API key is used up. Try again later.")
    payment = prove(client, headers, "123456789012").json()["payment"]
    assert payment["status"] == "needs_review"
    assert payment["checks"][-1]["key"] == "ai" and payment["checks"][-1]["ok"] is None


def test_owner_can_withdraw_an_accepted_payment(client, screenshot, mails):
    headers = register(client, "acme")
    screenshot.read = good_read("123456789012")
    payment = prove(client, headers, "123456789012").json()["payment"]
    owner = owner_headers(client)
    accept(client, owner, payment)
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
    rejected = client.post(f"{API}/platform/payments/{payment['id']}/decision", headers=owner,
                           json={"decision": "reject", "note": "Not in the bank statement"})
    assert rejected.json()["status"] == "rejected"
    assert client.get(f"{API}/assets", headers=headers).status_code == 402
    assert any("not accepted" in m["subject"] and "Not in the bank statement" in m["text"] for m in mails)


def test_proof_input_is_checked(client, screenshot):
    headers = register(client, "acme")
    assert prove(client, headers, "12345").status_code == 422
    assert prove(client, headers, "123456789012", b"<svg onload=alert(1)>", "image/png").status_code == 415
    assert screenshot.calls == 0


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


def review_token(mail: dict) -> str:
    return re.search(r"payment-review\?token=([\w-]+)&action=accept", mail["text"]).group(1)


def test_owner_accepts_from_the_mail(client, screenshot, mails):
    headers = register(client, "acme")
    screenshot.read = good_read("123456789012")
    prove(client, headers, "123456789012")
    mail = mails[0]
    assert mail["to"] == OWNER and "Accept payment" in mail["html"] and mail["attachment"][0] == PNG
    token = review_token(mail)
    assert token not in json.dumps(client.get(f"{API}/billing", headers=headers).json())  # never shown to the company

    page = client.get("/payment-review", params={"token": token, "action": "accept"})
    assert page.status_code == 200 and "acme" in page.text and "123456789012" in page.text
    assert page.headers["referrer-policy"] == "no-referrer"
    assert client.get("/payment-review/screenshot", params={"token": token}).content == PNG
    # Opening the link (as a mail scanner does) changes nothing
    assert client.get(f"{API}/assets", headers=headers).status_code == 402

    done = client.post("/payment-review", data={"token": token, "decision": "accept"})
    assert done.status_code == 200 and "Payment accepted" in done.text
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
    assert any("registered" in m["subject"] for m in mails if m["to"] == "admin@acme.example.com")
    # Once only
    assert client.post("/payment-review", data={"token": token, "decision": "reject"}).status_code == 410
    assert client.get("/payment-review", params={"token": token}).status_code == 410
    assert client.get("/payment-review/screenshot", params={"token": token}).status_code == 404


def test_owner_rejects_from_the_mail(client, screenshot, mails):
    headers = register(client, "acme")
    screenshot.read = good_read("123456789012")
    prove(client, headers, "123456789012")
    token = review_token(mails[0])
    done = client.post("/payment-review", data={"token": token, "decision": "reject", "note": "No such UTR in the bank"})
    assert "Payment rejected" in done.text
    assert client.get(f"{API}/billing", headers=headers).json()["payments"][0]["status"] == "rejected"
    assert any("No such UTR in the bank" in m["text"] for m in mails if m["to"] == "admin@acme.example.com")


def test_mail_link_stops_working(client, screenshot, mails):
    headers = register(client, "acme")
    screenshot.read = good_read("123456789012")
    payment = prove(client, headers, "123456789012").json()["payment"]
    token = review_token(mails[0])
    assert client.get("/payment-review", params={"token": "made-up"}).status_code == 410
    assert client.post("/payment-review", data={"token": token, "decision": "approve"}).status_code == 410

    database.payments.update_one({}, {"$set": {"review_expires_at": now() - timedelta(seconds=1)}})
    assert client.post("/payment-review", data={"token": token, "decision": "accept"}).status_code == 410
    database.payments.update_one({}, {"$set": {"review_expires_at": now() + timedelta(days=1)}})
    accept(client, owner_headers(client), payment)  # decided on the Payments page instead
    assert client.post("/payment-review", data={"token": token, "decision": "reject"}).status_code == 410
    assert client.get(f"{API}/assets", headers=headers).status_code == 200
