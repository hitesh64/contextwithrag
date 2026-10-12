"""Test setup: an in-memory MongoDB, a temporary vector index and storage folder, and no real model calls.

The environment is set before the application is imported, so no test can reach the real
database or spend Gemini quota.
"""
import hashlib
import math
import os
import shutil
import tempfile

_TMP = tempfile.mkdtemp(prefix="contextbasedrag_test_")
os.environ.update(
    MONGO_URI="mongomock://test",
    MONGO_DB="test",
    CHROMA_DIR=os.path.join(_TMP, "chroma"),
    STORAGE_DIR=os.path.join(_TMP, "storage"),
    GOOGLE_API_KEY="test-key",
    ALLOW_SELF_APPROVAL="false",
    AI_RATE_PER_MINUTE="1000",
    LOGIN_RATE_PER_MINUTE="1000",
    CORS_ORIGINS="",
    LOCAL_TIMEZONE="UTC",
)

import pytest  # noqa: E402
from fastapi.testclient import TestClient  # noqa: E402

from backend.app.api import auth, chat  # noqa: E402
from backend.app.core import database  # noqa: E402
from backend.app.main import app  # noqa: E402
from backend.app.services import llm, retrieval  # noqa: E402
from backend.app.services.keyword_search import tokenize  # noqa: E402

API = "/api/v1"
PASSWORD = "test-password-1"
DIMENSIONS = 64


def fake_embed(texts: list[str], task: str) -> list[list[float]]:
    """A bag-of-words vector: texts sharing words are close. Deterministic and free."""
    vectors = []
    for text in texts:
        vector = [0.01] * DIMENSIONS
        for token in tokenize(text):
            vector[int(hashlib.md5(token.encode()).hexdigest(), 16) % DIMENSIONS] += 1.0
        norm = math.sqrt(sum(v * v for v in vector))
        vectors.append([v / norm for v in vector])
    return vectors


class FakeLLM:
    """Stands in for Gemini. Set .reply to a string, an exception, or a function of (prompt, system)."""

    def __init__(self):
        self.reply = "INSUFFICIENT_EVIDENCE"
        self.calls: list[dict] = []

    def generate(self, prompt: str, system: str, json_output: bool = False) -> str:
        self.calls.append({"prompt": prompt, "system": system, "json_output": json_output})
        reply = self.reply(prompt, system) if callable(self.reply) else self.reply
        if isinstance(reply, Exception):
            raise reply
        return reply


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client


@pytest.fixture(autouse=True)
def clean_state(client, monkeypatch):
    for name in database.db.list_collection_names():
        database.db[name].delete_many({})
    ids = retrieval._chunks().get(include=[])["ids"]
    if ids:
        retrieval._chunks().delete(ids=ids)
    retrieval._keyword_cache.clear()
    shutil.rmtree(os.environ["STORAGE_DIR"], ignore_errors=True)
    os.makedirs(os.environ["STORAGE_DIR"])
    auth.login_limiter.reset()
    chat.ai_limiter.reset()
    monkeypatch.setattr(llm, "embed", fake_embed)


@pytest.fixture
def fake_llm(monkeypatch):
    fake = FakeLLM()
    monkeypatch.setattr(llm, "generate", fake.generate)
    return fake


class Factory:
    """One registered organization and helpers to act inside it."""

    def __init__(self, client: TestClient, name: str):
        self.client = client
        self.name = name
        email = f"admin@{name}.example.com"
        created = client.post(f"{API}/auth/register", json={
            "organization_name": name, "name": f"{name} admin", "email": email, "password": PASSWORD,
        })
        assert created.status_code == 201, created.text
        self.organization_id = created.json()["organization_id"]
        self.admin = self.login(email)

    def login(self, email: str) -> dict:
        response = self.client.post(f"{API}/auth/login", json={"email": email, "password": PASSWORD})
        assert response.status_code == 200, response.text
        return {"Authorization": f"Bearer {response.json()['access_token']}"}

    def user(self, role: str) -> dict:
        """Headers of a new user with this role."""
        email = f"{role}{len(list(database.users.find()))}@{self.name}.example.com"
        created = self.client.post(f"{API}/users", headers=self.admin, json={
            "name": f"{self.name} {role}", "email": email, "password": PASSWORD, "role": role,
        })
        assert created.status_code == 201, created.text
        return self.login(email)

    def asset(self, code: str = "CNC-01", **fields) -> dict:
        body = {"asset_code": code, "name": f"Machine {code}", "criticality": "high", **fields}
        created = self.client.post(f"{API}/assets", headers=self.admin, json=body)
        assert created.status_code == 201, created.text
        return created.json()

    def upload(self, filename: str, data: bytes, asset_ids: str = "", doc_type: str = "manual"):
        return self.client.post(
            f"{API}/documents", headers=self.admin,
            files={"file": (filename, data)}, data={"asset_ids": asset_ids, "doc_type": doc_type},
        )

    def document(self, filename: str, data: bytes, asset_ids: str = "") -> dict:
        """Upload a file and return its record after background processing."""
        uploaded = self.upload(filename, data, asset_ids)
        assert uploaded.status_code == 202, uploaded.text
        return self.client.get(f"{API}/documents/{uploaded.json()['id']}", headers=self.admin).json()

    def breakdown(self, asset_id: str, **fields) -> dict:
        body = {"asset_id": asset_id, "reported_at": "2026-03-01T08:00:00Z", "symptoms": "Machine stopped", **fields}
        created = self.client.post(f"{API}/breakdowns", headers=self.admin, json=body)
        assert created.status_code == 201, created.text
        return created.json()


@pytest.fixture
def factory(client):
    return Factory(client, "alpha")


@pytest.fixture
def other_factory(client):
    return Factory(client, "beta")


def make_pdf(pages: list[str]) -> bytes:
    import pymupdf

    pdf = pymupdf.open()
    for text in pages:
        pdf.new_page().insert_textbox(pymupdf.Rect(50, 50, 550, 800), text, fontsize=11)
    return pdf.tobytes()
