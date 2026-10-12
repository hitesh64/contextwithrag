"""Conflicts found in answers: stored once, listed for reviewers, closed only by a person with the right role.

A record is keyed by what disagrees (the documents and their values), so asking the same question twice
does not create two. A recorded decision stands only while the documents it was made about are unchanged.
"""
from ..core.database import conflicts, documents
from ..core.utils import now, oid
from . import audit_service


def _signature(organization_id: str, document_ids: list[str]) -> str:
    """The state of the documents involved; any change of version facts or of the document itself alters it."""
    parts = []
    for document_id in sorted(document_ids):
        doc = documents.find_one({"_id": oid(document_id), "organization_id": organization_id})
        if doc is None:
            parts.append(f"{document_id}:deleted")
        else:
            parts.append(
                f"{document_id}:{doc.get('file_hash')}:{doc.get('revision')}:{doc.get('effective_date')}"
                f":{doc.get('lifecycle')}:{doc.get('supersedes_document_id')}"
            )
    return "|".join(parts)


def sync(organization_id: str, finding: dict) -> dict:
    """Store or refresh the record of a finding; a resolved one reopens if its documents changed since."""
    document_ids = sorted({c["document_id"] for c in finding["claims"]})
    signature = _signature(organization_id, document_ids)
    snapshot = [
        {k: c[k] for k in ("document_id", "filename", "page", "section", "sentence", "value", "revision")}
        for c in finding["claims"]
    ]
    record = conflicts.find_one({"organization_id": organization_id, "fingerprint": finding["fingerprint"]})
    stamp = now()
    if record is None:
        record = {
            "organization_id": organization_id,
            "fingerprint": finding["fingerprint"],
            "kind": finding["kind"],
            "topic": finding["topic"],
            "dimension": finding["dimension"],
            "claims": snapshot,
            "document_ids": document_ids,
            "differences": finding["differences"],
            "notes": finding["notes"],
            "status": "open",
            "signature": signature,
            "resolution": None,
            "history": [],
            "times_seen": 1,
            "first_seen_at": stamp,
            "last_seen_at": stamp,
        }
        record["_id"] = conflicts.insert_one(record).inserted_id
        return record

    update = {
        "kind": finding["kind"], "claims": snapshot, "differences": finding["differences"],
        "notes": finding["notes"], "signature": signature, "last_seen_at": stamp,
    }
    resolution = record.get("resolution")
    if record["status"] == "resolved" and resolution and resolution["signature"] != signature:
        update.update(status="open", resolution=None, reopened_at=stamp)
        update["history"] = record["history"] + [resolution]
    conflicts.update_one({"_id": record["_id"]}, {"$set": update, "$inc": {"times_seen": 1}})
    return conflicts.find_one({"_id": record["_id"]})


def resolve(user: dict, record: dict, decision: str, document_id: str | None, note: str) -> dict:
    """Close a conflict with the decision of a person. The caller has already checked the role."""
    document_name = None
    if decision in ("governs", "outdated"):
        match = next((c for c in record["claims"] if c["document_id"] == document_id), None)
        if match is None:
            raise ValueError("Name one of the documents in this conflict.")
        document_name = match["filename"]
    resolution = {
        "decision": decision,
        "document_id": document_id if document_name else None,
        "document_name": document_name,
        "note": note,
        "resolved_by": user["id"],
        "resolved_by_name": user["name"],
        "resolved_at": now(),
        "sources": [{"document_id": c["document_id"], "filename": c["filename"]} for c in record["claims"]],
        "signature": _signature(record["organization_id"], record["document_ids"]),
        "request_id": audit_service.request_id.get(),
    }
    conflicts.update_one({"_id": record["_id"]}, {"$set": {"status": "resolved", "resolution": resolution}})
    audit_service.record(
        user, "conflict.resolve", "conflict", str(record["_id"]),
        detail=f"{decision}; documents " + ",".join(record["document_ids"]),
    )
    return conflicts.find_one({"_id": record["_id"]})
