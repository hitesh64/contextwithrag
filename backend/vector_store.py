"""ChromaDB: LONG-TERM memory.

Two persistent collections:
  - documents         : chunks of the bank's documents, each marked with the departments that may read it
  - long_term_memory  : past question/answer pairs of one user, recalled semantically in later chats

Documents are found by hybrid search: the vector ranking and a keyword (BM25) ranking of the
same chunks are merged, so exact strings such as part numbers and error codes are found too.

Embeddings come from the Gemini API (llm.embed). Running an embedding model inside the server
was too slow and too memory-hungry for a small host: a 24-chunk PDF took the best part of a
minute there and about 2 seconds through the API.

A host without a permanent disk loses this folder on every restart. Remembered exchanges are
therefore also kept in MongoDB (with their vectors) and put back at startup, and exchanges
that were never stored are embedded again from the chats that still exist.
"""
import re
import threading

import chromadb

from . import llm
from .config import settings
from .database import memories as saved_memories, messages
from .keyword_search import KeywordIndex, fuse

BATCH = 100
# How many chunks each of the two rankings contributes before they are merged
CANDIDATES = 20
# Cosine distance above which a remembered conversation is considered unrelated
# (with Gemini embeddings related exchanges score about 0.2, unrelated ones 0.4 and more)
MEMORY_MAX_DISTANCE = 0.33
# Collection names carry the embedding they were built with; vectors of different models cannot be mixed
COLLECTIONS = {"documents": "documents_gemini", "long_term_memory": "long_term_memory_gemini"}


_lock = threading.Lock()
_collections: dict = {}
# reader department (None: administrator) -> (chunk ids, chunks, KeywordIndex); dropped when the library changes
_keyword_cache: dict[str | None, tuple[list[str], list[dict], KeywordIndex]] = {}


def init() -> None:
    """Open the store and both collections exactly once.

    Requests run in a thread pool; two of them opening a fresh store at the same time corrupts
    its setup ("Could not connect to tenant default_tenant"), so opening is serialised here
    and done at server startup.
    """
    with _lock:
        if not _collections:
            client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
            for key, name in COLLECTIONS.items():
                # embedding_function=None: vectors are always supplied, Chroma never loads its own model
                _collections[key] = client.get_or_create_collection(
                    name, metadata={"hnsw:space": "cosine"}, embedding_function=None
                )


def _collection(name: str):
    if not _collections:
        init()
    return _collections[name]


def _documents():
    return _collection("documents")


def _memory():
    return _collection("long_term_memory")


# ---------- knowledge base ----------

def _chunk(text: str, meta: dict) -> dict:
    return {
        "text": text, "source": meta.get("source", "Unknown"), "page": meta.get("page"),
        "category": meta.get("category"), "effective_date": meta.get("effective_date"),
    }


def _department_flag(department: str) -> str:
    """Chroma metadata holds no lists, so each department that may read a chunk is a flag of its own."""
    return "dept_" + re.sub(r"[^a-z0-9]+", "_", department.lower()).strip("_")


def _readable_by(department: str | None) -> dict | None:
    """Filter for the chunks a reader of this department may see (None: an administrator, who sees all)."""
    if department is None:
        return None
    return {"$or": [{"dept_all": True}, {_department_flag(department): True}]}


def add_document_chunks(
    file_id: str, source: str, chunks: list[dict], departments: list[str], category: str, effective_date: str | None
) -> None:
    """chunks: {"text", "page"} as produced by processor.split_documents (page may be None).

    departments: who may read the document; empty means every department.
    """
    col = _documents()
    base = {"file_id": file_id, "source": source, "category": category}
    if effective_date:
        base["effective_date"] = effective_date
    base.update({_department_flag(d): True for d in departments} or {"dept_all": True})
    # Embed everything first, so a failed embedding leaves nothing half-stored
    vectors = llm.embed([c["text"] for c in chunks], "RETRIEVAL_DOCUMENT")
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i:i + BATCH]
        col.add(
            ids=[f"{file_id}_{i + j}" for j in range(len(batch))],
            embeddings=vectors[i:i + BATCH],
            documents=[c["text"] for c in batch],
            metadatas=[{**base, "page": c["page"]} if c["page"] else base for c in batch],
        )
    _keyword_cache.clear()


def _keywords(department: str | None) -> tuple[list[str], list[dict], KeywordIndex]:
    cached = _keyword_cache.get(department)
    if cached is None:
        res = _documents().get(where=_readable_by(department), include=["documents", "metadatas"])
        chunks = [_chunk(doc, meta) for doc, meta in zip(res["documents"], res["metadatas"])]
        cached = _keyword_cache[department] = (res["ids"], chunks, KeywordIndex([c["text"] for c in chunks]))
    return cached


def search_documents(department: str | None, question: str, query_vector: list[float], k: int = 8) -> list[dict]:
    """Hybrid search: the best k chunks this reader may see, by meaning (vectors) and by wording (BM25) together.

    department: the reader's department, or None for an administrator.
    """
    res = _documents().query(
        query_embeddings=[query_vector], n_results=CANDIDATES, where=_readable_by(department)
    )
    by_meaning = res["ids"][0]
    found = {
        id_: _chunk(doc, meta) for id_, doc, meta in zip(by_meaning, res["documents"][0], res["metadatas"][0])
    }

    ids, chunks, index = _keywords(department)
    by_wording = []
    for position in index.search(question, CANDIDATES):
        by_wording.append(ids[position])
        found.setdefault(ids[position], chunks[position])

    return [found[id_] for id_ in fuse([by_meaning, by_wording], k)]


def indexed_file_ids() -> set[str]:
    """Files that really have chunks here (the store is wiped when a host without a disk restarts)."""
    return {m["file_id"] for m in _documents().get(include=["metadatas"])["metadatas"]}


def delete_document(file_id: str) -> None:
    _documents().delete(where={"file_id": file_id})
    _keyword_cache.clear()


def share_old_documents() -> None:
    """Chunks stored before departments existed carry no reader; make them readable by everyone (run at startup)."""
    res = _documents().get(include=["metadatas"])
    old = [
        (id_, meta) for id_, meta in zip(res["ids"], res["metadatas"])
        if not any(key.startswith("dept_") for key in meta)
    ]
    for i in range(0, len(old), BATCH):
        batch = old[i:i + BATCH]
        _documents().update(ids=[id_ for id_, _ in batch], metadatas=[{**meta, "dept_all": True} for _, meta in batch])


# ---------- conversation memory ----------

def _exchange_text(question: str, answer: str) -> str:
    return f"User asked: {question}\nAssistant answered: {answer[:1500]}"


def _fill(rows: list[dict]) -> None:
    """rows: documents of the MongoDB "memories" collection."""
    for i in range(0, len(rows), BATCH):
        batch = rows[i:i + BATCH]
        _memory().upsert(
            ids=[r["_id"] for r in batch],
            embeddings=[r["embedding"] for r in batch],
            documents=[r["text"] for r in batch],
            metadatas=[{k: r[k] for k in ("user_id", "session_id", "created_at")} for r in batch],
        )


def _remember_many(exchanges: list[dict]) -> None:
    """exchanges: {"_id", "user_id", "session_id", "created_at", "text"}; the id is that of the assistant message."""
    vectors = llm.embed([e["text"] for e in exchanges], "RETRIEVAL_DOCUMENT")
    rows = [{**e, "embedding": v} for e, v in zip(exchanges, vectors)]
    for row in rows:
        saved_memories.replace_one({"_id": row["_id"]}, row, upsert=True)
    _fill(rows)


def remember(user_id: str, session_id: str, message_id: str, question: str, answer: str, created_at: str) -> None:
    text = _exchange_text(question, answer)
    _remember_many([{
        "_id": message_id, "user_id": user_id, "session_id": session_id, "created_at": created_at, "text": text,
    }])


def restore_memory() -> None:
    """Put back the remembered exchanges this store lost (run at startup; needs no embedding)."""
    known = _memory().get(include=[])["ids"]
    _fill(list(saved_memories.find({"_id": {"$nin": known}})))


def backfill_memory() -> None:
    """Remember the exchanges of existing chats that were never stored (run at startup, in the background)."""
    known = set(saved_memories.distinct("_id"))
    question: dict[str, str] = {}
    missing = []
    for m in messages.find().sort([("session_id", 1), ("created_at", 1)]):
        if m["role"] == "user":
            question[m["session_id"]] = m["content"]
        elif str(m["_id"]) not in known and m["session_id"] in question:
            missing.append({
                "_id": str(m["_id"]), "user_id": m["user_id"], "session_id": m["session_id"],
                "created_at": m["created_at"].isoformat(),
                "text": _exchange_text(question[m["session_id"]], m["content"]),
            })
    if not missing:
        return
    try:
        _remember_many(missing)
    except llm.LLMError:
        pass  # no key or no quota right now; the next start tries again


def recall(user_id: str, query_vector: list[float], skip_ids: set[str], k: int = 3) -> list[str]:
    """Related past exchanges of the user, from any chat.

    skip_ids: exchanges already sent to the model as short-term memory. Older turns of the
    current chat are not skipped, so a long chat can still recall its own beginning.
    """
    res = _memory().query(
        query_embeddings=[query_vector],
        n_results=k + len(skip_ids),
        where={"user_id": user_id},
    )
    related = [
        doc for id_, doc, dist in zip(res["ids"][0], res["documents"][0], res["distances"][0])
        if id_ not in skip_ids and dist <= MEMORY_MAX_DISTANCE
    ]
    return related[:k]


def forget_session(user_id: str, session_id: str) -> None:
    saved_memories.delete_many({"user_id": user_id, "session_id": session_id})
    _memory().delete(where={"$and": [{"user_id": user_id}, {"session_id": session_id}]})


def memory_count(user_id: str) -> int:
    return len(_memory().get(where={"user_id": user_id}, include=[])["ids"])
