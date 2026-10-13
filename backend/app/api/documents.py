"""Document library: manuals, SOPs and parts lists of a factory."""
import logging
import os

from fastapi import APIRouter, BackgroundTasks, Depends, File, Form, HTTPException, Query, UploadFile, status
from fastapi.responses import FileResponse

from ..core.config import settings
from ..core.database import assets, documents
from ..core.security import get_current_user, require_role
from ..core.utils import clean, now, oid, paginate
from ..schemas import DocumentVersionUpdate
from ..services import audit_service, ingestion, retrieval

router = APIRouter(prefix="/documents", tags=["documents"])
log = logging.getLogger(__name__)

DOC_TYPES = ["manual", "sop", "spare_parts", "other"]


def get_document(organization_id: str, document_id: str) -> dict:
    doc = documents.find_one({"_id": oid(document_id), "organization_id": organization_id})
    if doc is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Document not found")
    return doc


@router.post("", status_code=status.HTTP_202_ACCEPTED)
def upload_document(
    background: BackgroundTasks,
    file: UploadFile = File(...),
    doc_type: str = Form("manual"),
    asset_ids: str = Form("", description="Comma-separated ids of the assets this document belongs to; empty: general"),
    user: dict = Depends(require_role("maintenance_manager")),
):
    """Store the file and start processing in the background. Poll GET /documents/{id} for its status."""
    org = user["organization_id"]
    if doc_type not in DOC_TYPES:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"doc_type must be one of: {', '.join(DOC_TYPES)}")
    linked = [a for a in (s.strip() for s in asset_ids.split(",")) if a]
    for asset_id in linked:
        if assets.find_one({"_id": oid(asset_id), "organization_id": org}) is None:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Unknown asset in asset_ids.")

    filename = os.path.basename((file.filename or "file").replace("\\", "/"))[:200]
    data = file.file.read(settings.MAX_UPLOAD_MB * 1024 * 1024 + 1)
    try:
        ext = ingestion.validate(filename, data)
    except ingestion.RejectedFile as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(e))

    digest = ingestion.file_hash(data)
    same = documents.find_one({"organization_id": org, "file_hash": digest})
    if same is not None:
        raise HTTPException(status.HTTP_409_CONFLICT, f"This exact file is already in the library as \"{same['filename']}\".")

    doc = {
        "organization_id": org,
        "filename": filename,
        "storage_key": ingestion.store(org, ext, data),
        "mime_type": ingestion.MIME_TYPES[ext],
        "file_hash": digest,
        "size_bytes": len(data),
        "doc_type": doc_type,
        "asset_ids": linked,
        # Version facts are unknown until a manager records them
        "revision": None,
        "effective_date": None,
        "lifecycle": None,
        "supersedes_document_id": None,
        "status": "queued",
        "error": None,
        "chunk_count": 0,
        "page_count": None,
        "parser_version": None,
        "embedding_model": None,
        "uploaded_by": user["id"],
        "uploaded_by_name": user["name"],
        "created_at": now(),
        "processed_at": None,
    }
    doc["_id"] = documents.insert_one(doc).inserted_id
    background.add_task(ingestion.process_document, doc["_id"])
    audit_service.record(user, "document.upload", "document", str(doc["_id"]), detail=filename)
    return clean(doc)


@router.get("")
def list_documents(
    status_: str = Query("", alias="status"),
    asset_id: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: dict = Depends(get_current_user),
):
    query: dict = {"organization_id": user["organization_id"]}
    if status_:
        query["status"] = status_
    if asset_id:
        query["asset_ids"] = asset_id
    return paginate(documents, query, page, page_size, [("created_at", -1)])


@router.get("/{document_id}")
def view_document(document_id: str, user: dict = Depends(get_current_user)):
    return clean(get_document(user["organization_id"], document_id))


@router.get("/{document_id}/file")
def download_document(document_id: str, user: dict = Depends(get_current_user)):
    """The original file, for opening a citation. Served only through this authenticated endpoint."""
    doc = get_document(user["organization_id"], document_id)
    path = ingestion.stored_path(doc["storage_key"])
    if not path.is_file():
        raise HTTPException(status.HTTP_404_NOT_FOUND, "The original file is no longer in storage.")
    return FileResponse(path, media_type=doc["mime_type"], filename=doc["filename"], content_disposition_type="inline")


@router.post("/{document_id}/reprocess", status_code=status.HTTP_202_ACCEPTED)
def reprocess_document(
    document_id: str, background: BackgroundTasks, user: dict = Depends(require_role("maintenance_manager"))
):
    """Run processing again, e.g. after a failure. Existing chunks are replaced, so nothing is duplicated."""
    doc = get_document(user["organization_id"], document_id)
    if doc["status"] in ("queued", "processing"):
        raise HTTPException(status.HTTP_409_CONFLICT, "This document is already being processed.")
    documents.update_one({"_id": doc["_id"]}, {"$set": {"status": "queued", "error": None}})
    background.add_task(ingestion.process_document, doc["_id"])
    audit_service.record(user, "document.reprocess", "document", document_id, detail=doc["filename"])
    return clean(documents.find_one({"_id": doc["_id"]}))


@router.delete("/{document_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_document(document_id: str, user: dict = Depends(require_role("maintenance_manager"))):
    """Remove the indexed chunks, the stored file and the record, in that order.

    The chunks go first: if a later step fails the document can no longer be cited, and the
    record that remains lets the deletion be repeated.
    """
    doc = get_document(user["organization_id"], document_id)
    try:
        retrieval.delete_document(user["organization_id"], document_id)
    except Exception:
        log.exception("Could not delete chunks of document %s", document_id)
        audit_service.record(user, "document.delete", "document", document_id, "failed", doc["filename"])
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "The search index is unavailable; nothing was deleted.")
    ingestion.remove_stored(doc["storage_key"])
    documents.delete_one({"_id": doc["_id"]})
    audit_service.record(user, "document.delete", "document", document_id, detail=doc["filename"])
    return None


@router.patch("/{document_id}/version")
def update_version(
    document_id: str, body: DocumentVersionUpdate, user: dict = Depends(require_role("maintenance_manager"))
):
    """Record which revision a document is and whether it is superseded.

    Only what a manager states here counts: an older upload or a file name never makes a document
    "superseded". Naming `supersedes_document_id` marks that other document as superseded by this one.
    """
    org = user["organization_id"]
    doc = get_document(org, document_id)
    changes = body.model_dump(exclude_unset=True)
    if not changes:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Nothing to change.")
    if changes.get("effective_date") is not None:
        changes["effective_date"] = changes["effective_date"].isoformat()
    if changes.get("supersedes_document_id"):
        if changes["supersedes_document_id"] == document_id:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "A document cannot supersede itself.")
        get_document(org, changes["supersedes_document_id"])
    documents.update_one({"_id": doc["_id"]}, {"$set": changes})
    detail = ", ".join(f"{k}={v}" for k, v in changes.items())
    audit_service.record(user, "document.version", "document", document_id, detail=f"{doc['filename']}: {detail}")
    return clean(documents.find_one({"_id": doc["_id"]}))
