"""The bank's document library: administrators publish documents, staff read what their department may see."""
import os
import tempfile
from datetime import date, datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status

from . import llm, vector_store
from .config import settings
from .database import files
from .processor import ALLOWED_EXTENSIONS, file_extension, load_documents, split_documents
from .security import get_current_user, reader_department, require_admin

router = APIRouter(prefix="/api/files", tags=["files"])

MAX_BYTES = settings.MAX_UPLOAD_MB * 1024 * 1024


def _file_out(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "filename": doc["filename"],
        "chunks": doc["chunks"],
        "size": doc["size"],
        "uploaded_at": doc["uploaded_at"],
        "category": doc["category"],
        "effective_date": doc["effective_date"],
        "departments": doc["departments"],
    }


def _index_one(upload: UploadFile, user: dict, category: str, effective_date: str | None, departments: list[str]) -> dict:
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
            docs = load_documents(tmp_path, ext, llm.read_page, settings.MAX_SCANNED_PAGES)
        except (ValueError, llm.LLMError):
            raise
        except Exception:
            raise ValueError("could not be read (corrupt or protected file)")
    finally:
        os.remove(tmp_path)

    if sum(len(d.page_content.strip()) for d in docs) < 10:
        raise ValueError("no readable text found")

    chunks = split_documents(docs, ext)
    if len(chunks) > settings.MAX_FILE_CHUNKS:
        raise ValueError(
            f"too much text to index ({len(chunks)} sections, the limit is {settings.MAX_FILE_CHUNKS}). "
            "Split the file into smaller parts."
        )

    file_id = ObjectId()
    doc = {
        "_id": file_id,
        "user_id": user["id"],
        "uploaded_by": user["username"],
        "filename": filename,
        "chunks": len(chunks),
        "size": len(data),
        "uploaded_at": datetime.now(timezone.utc),
        "category": category,
        "effective_date": effective_date,
        # Empty list: every department may read it
        "departments": departments,
    }
    try:
        vector_store.add_document_chunks(str(file_id), filename, chunks, departments, category, effective_date)
        files.insert_one(doc)
    except Exception:
        # Never leave half a file behind
        vector_store.delete_document(str(file_id))
        raise
    return doc


@router.post("", status_code=status.HTTP_201_CREATED)
def upload_file(
    upload: UploadFile = File(...),
    category: str = Form(...),
    effective_date: str = Form(""),
    departments: list[str] = Form([]),
    user: dict = Depends(require_admin),
):
    """One file per request: indexing is memory- and CPU-heavy, so files are handled one at a time.

    departments: who may read the document; none given means every department.
    """
    if category not in settings.CATEGORIES:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Unknown document category.")
    unknown = [d for d in departments if d not in settings.DEPARTMENTS]
    if unknown:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"Unknown department: {unknown[0]}")
    try:
        effective = date.fromisoformat(effective_date).isoformat() if effective_date else None
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The effective date must look like 2025-04-01.")

    try:
        return _file_out(_index_one(upload, user, category, effective, departments))
    except ValueError as e:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, f"{upload.filename}: {e}")
    except llm.LLMError as e:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(e))


@router.get("")
def list_files(user: dict = Depends(get_current_user)):
    department = reader_department(user)
    visible = {} if department is None else {"$or": [{"departments": {"$size": 0}}, {"departments": department}]}
    # Only files whose chunks are really in the vector store can be searched, so only those are listed
    indexed = vector_store.indexed_file_ids()
    cursor = files.find(visible).sort("uploaded_at", -1)
    return [_file_out(d) for d in cursor if str(d["_id"]) in indexed]


@router.delete("/{file_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_file(file_id: str, _: dict = Depends(require_admin)):
    if not ObjectId.is_valid(file_id) or not files.find_one({"_id": ObjectId(file_id)}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "File not found")
    vector_store.delete_document(file_id)
    files.delete_one({"_id": ObjectId(file_id)})
