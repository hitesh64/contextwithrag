import os
import tempfile
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status

from . import vector_store
from .config import settings
from .database import files
from .processor import ALLOWED_EXTENSIONS, file_extension, load_documents, split_documents
from .security import get_current_user

router = APIRouter(prefix="/api/files", tags=["files"])

MAX_BYTES = settings.MAX_UPLOAD_MB * 1024 * 1024


def _file_out(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "chunks": doc["chunks"],
        "size": doc["size"],
        "uploaded_at": doc["uploaded_at"],
    }


def _index_one(upload: UploadFile, user_id: str) -> dict:
    """Extract, chunk and store one file. Raises ValueError with a user-facing reason on failure."""
    filename = os.path.basename(upload.filename or "file")
    ext = file_extension(filename)
    if ext not in ALLOWED_EXTENSIONS:
        raise ValueError("unsupported file type")

    data = upload.file.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise ValueError(f"larger than {settings.MAX_UPLOAD_MB} MB")

    fd, tmp_path = tempfile.mkstemp(suffix=f".{ext}")
    try:
        with os.fdopen(fd, "wb") as tmp:
            tmp.write(data)
        try:
            docs = load_documents(tmp_path, ext)
        except Exception:
            raise ValueError("could not be read (corrupt or protected file)")
    finally:
        os.remove(tmp_path)

    if sum(len(d.page_content.strip()) for d in docs) < 10:
        raise ValueError("no readable text found (scanned PDFs without a text layer are not supported)")

    chunks = split_documents(docs, ext)
    file_id = ObjectId()
    vector_store.add_document_chunks(user_id, str(file_id), filename, chunks)
    doc = {
        "_id": file_id,
        "user_id": user_id,
        "filename": filename,
        "chunks": len(chunks),
        "size": len(data),
        "uploaded_at": datetime.now(timezone.utc),
    }
    files.insert_one(doc)
    return doc


@router.post("")
def upload_files(uploads: list[UploadFile] = File(...), user: dict = Depends(get_current_user)):
    indexed, skipped = [], []
    for upload in uploads:
        try:
            indexed.append(_file_out(_index_one(upload, user["id"])))
        except ValueError as e:
            skipped.append({"filename": upload.filename, "reason": str(e)})
    if not indexed:
        reasons = "; ".join(f"{s['filename']}: {s['reason']}" for s in skipped)
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"No files could be indexed. {reasons}")
    return {"indexed": indexed, "skipped": skipped}


@router.get("")
def list_files(user: dict = Depends(get_current_user)):
    return [_file_out(d) for d in files.find({"user_id": user["id"]}).sort("uploaded_at", -1)]


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: str, user: dict = Depends(get_current_user)):
    # Filtering by user_id means a user can only ever delete their own files
    if not ObjectId.is_valid(file_id) or not files.find_one({"_id": ObjectId(file_id), "user_id": user["id"]}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    vector_store.delete_document(user["id"], file_id)
    files.delete_one({"_id": ObjectId(file_id)})
