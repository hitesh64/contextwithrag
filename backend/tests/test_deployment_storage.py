"""A host whose disk is emptied on every restart (free cloud plans): files and the index must come back."""
import shutil

from backend.app.core import database
from backend.app.core.config import settings
from backend.app.services import ingestion, retrieval

from .conftest import API

SOP = b"Hydraulic press SOP. Operating pressure is 180 bar. Replace the hydraulic filter every 500 hours."


def wipe_disk(doc_id: str) -> None:
    """What a restart on such a host does: the uploaded files and the vector index are gone."""
    shutil.rmtree(settings.STORAGE_DIR, ignore_errors=True)
    retrieval.delete_document("", doc_id)


def test_files_kept_in_the_database_survive_a_wiped_disk(client, factory, monkeypatch):
    monkeypatch.setattr(settings, "FILE_STORE", "database")
    doc = factory.document("press.txt", SOP)
    assert database.stored_files.count_documents({}) == 1
    wipe_disk(doc["id"])
    assert retrieval.search(factory.organization_id, "operating pressure", 3) == []

    assert ingestion.reindex_missing() == 1
    again = client.get(f"{API}/documents/{doc['id']}", headers=factory.admin).json()
    assert again["status"] == "ready" and again["chunk_count"] == 1
    assert retrieval.search(factory.organization_id, "operating pressure", 3)[0]["document_id"] == doc["id"]
    # The original can be opened again, and nothing is indexed twice
    assert client.get(f"{API}/documents/{doc['id']}/file", headers=factory.admin).content == SOP
    assert ingestion.reindex_missing() == 0 and retrieval.count_chunks(doc["id"]) == 1

    # Deleting the document removes the copy in the database as well
    assert client.delete(f"{API}/documents/{doc['id']}", headers=factory.admin).status_code == 204
    assert database.stored_files.count_documents({}) == 0


def test_without_a_copy_a_lost_document_is_reported_and_not_shown_as_ready(client, factory):
    doc = factory.document("press.txt", SOP)  # FILE_STORE=disk, the default
    assert database.stored_files.count_documents({}) == 0
    wipe_disk(doc["id"])

    assert ingestion.reindex_missing() == 1
    lost = client.get(f"{API}/documents/{doc['id']}", headers=factory.admin).json()
    assert lost["status"] == "failed" and "no longer in storage" in lost["error"]


def test_the_copy_in_the_database_stays_inside_its_organization(client, factory, other_factory, monkeypatch):
    monkeypatch.setattr(settings, "FILE_STORE", "database")
    doc = factory.document("press.txt", SOP)
    shutil.rmtree(settings.STORAGE_DIR, ignore_errors=True)
    assert client.get(f"{API}/documents/{doc['id']}/file", headers=other_factory.admin).status_code == 404
    assert client.get(f"{API}/documents/{doc['id']}/file", headers=factory.admin).content == SOP


def test_health_tells_keys_apart_without_showing_them(client):
    import hashlib

    health = client.get("/health").json()
    assert health["llm_key_fingerprint"] == hashlib.sha256(b"test-key").hexdigest()[:8] + "/8"
    assert "test-key" not in str(health)
