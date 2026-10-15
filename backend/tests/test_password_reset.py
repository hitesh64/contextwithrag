import re
from datetime import timedelta

import pytest

from backend.app.core import database
from backend.app.core.config import settings
from backend.app.core.utils import now
from backend.app.services import mailer

from .conftest import API, PASSWORD

EMAIL = "admin@alpha.example.com"
NEW_PASSWORD = "brand-new-password-2"


@pytest.fixture
def mails(monkeypatch):
    sent = []
    monkeypatch.setattr(settings, "SMTP_USER", "mailer@example.com")
    monkeypatch.setattr(settings, "SMTP_PASSWORD", "app-password")
    monkeypatch.setattr(mailer, "send", lambda to, subject, text: sent.append({"to": to, "subject": subject, "text": text}))
    return sent


def ask_for_link(client, email=EMAIL):
    response = client.post(f"{API}/auth/forgot-password", json={"email": email})
    assert response.status_code == 200, response.text
    return response.json()["detail"]


def token_in(mail: dict) -> str:
    return re.search(r"#/reset-password\?token=([\w-]+)", mail["text"]).group(1)


def reset(client, token, password=NEW_PASSWORD, confirm=None):
    return client.post(f"{API}/auth/reset-password", json={
        "token": token, "password": password, "confirm_password": password if confirm is None else confirm,
    })


def login(client, password):
    return client.post(f"{API}/auth/login", json={"email": EMAIL, "password": password})


def test_full_reset_flow(client, factory, mails):
    ask_for_link(client)
    assert len(mails) == 1 and mails[0]["to"] == EMAIL
    assert f"{settings.APP_BASE_URL}/#/reset-password?token=" in mails[0]["text"]
    token = token_in(mails[0])
    # Only the hash of the token is stored
    stored = database.password_resets.find_one({})
    assert token not in str(stored)

    checked = client.post(f"{API}/auth/reset-password/check", json={"token": token})
    assert checked.status_code == 200 and checked.json()["email"] == EMAIL

    assert reset(client, token).status_code == 200
    assert login(client, NEW_PASSWORD).status_code == 200
    assert login(client, PASSWORD).status_code == 401
    # Logins made with the old password end at once
    assert client.get(f"{API}/auth/me", headers=factory.admin).status_code == 401
    assert mails[-1]["to"] == EMAIL and "password was changed" in mails[-1]["subject"]
    assert database.audit_events.find_one({"action": "user.password_reset"})


def test_link_works_once(client, factory, mails):
    ask_for_link(client)
    token = token_in(mails[0])
    assert reset(client, token).status_code == 200
    again = reset(client, token, "another-password-3")
    assert again.status_code == 400
    assert client.post(f"{API}/auth/reset-password/check", json={"token": token}).status_code == 400


def test_passwords_must_match_and_be_long_enough(client, factory, mails):
    ask_for_link(client)
    token = token_in(mails[0])
    mismatch = reset(client, token, NEW_PASSWORD, "something-else-9")
    assert mismatch.status_code == 422 and "do not match" in mismatch.json()["detail"]
    assert reset(client, token, "short").status_code == 422
    # A refused attempt does not use up the link
    assert reset(client, token).status_code == 200


def test_unknown_email_gets_the_same_answer_and_no_mail(client, factory, mails):
    known = ask_for_link(client)
    unknown = ask_for_link(client, "nobody@alpha.example.com")
    assert known.replace(EMAIL, "") == unknown.replace("nobody@alpha.example.com", "")
    assert [m["to"] for m in mails] == [EMAIL]


def test_expired_link_is_refused(client, factory, mails):
    ask_for_link(client)
    database.password_resets.update_many({}, {"$set": {"expires_at": now() - timedelta(seconds=1)}})
    assert reset(client, token_in(mails[0])).status_code == 400
    assert login(client, PASSWORD).status_code == 200


def test_a_new_link_replaces_the_old_one(client, factory, mails):
    ask_for_link(client)
    ask_for_link(client)
    first, second = token_in(mails[0]), token_in(mails[1])
    assert reset(client, first).status_code == 400
    assert reset(client, second).status_code == 200


def test_deactivated_user_gets_no_link(client, factory, mails):
    ask_for_link(client)
    database.users.update_one({"email": EMAIL}, {"$set": {"is_active": False}})
    assert reset(client, token_in(mails[0])).status_code == 400
    ask_for_link(client)
    assert len(mails) == 1


def test_made_up_token_is_refused(client, factory, mails):
    assert reset(client, "x" * 43).status_code == 400


def test_without_smtp_the_server_says_so(client, factory, monkeypatch):
    monkeypatch.setattr(settings, "SMTP_USER", "")
    response = client.post(f"{API}/auth/forgot-password", json={"email": EMAIL})
    assert response.status_code == 503


def test_new_password_follows_the_password_rule(client, factory, mails):
    ask_for_link(client)
    token = token_in(mails[0])
    assert reset(client, token, "onlyletters").status_code == 422
    assert reset(client, token, "a1" * 40).status_code == 422
    assert login(client, PASSWORD).status_code == 200
