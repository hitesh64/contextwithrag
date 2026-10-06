"""ChromaDB: LONG-TERM memory.

Two persistent collections, both filtered per user:
  - documents         : chunks of the user's uploaded files (knowledge base)
  - long_term_memory  : past question/answer pairs, recalled semantically in later chats

Embeddings come from the Gemini API (llm.embed). Running an embedding model inside the server
was too slow and too memory-hungry for a small host: a 24-chunk PDF took the best part of a
minute there and about 2 seconds through the API.
"""
import threading

import chromadb

from . import llm
from .config import settings

BATCH = 100
# Cosine distance above which a remembered conversation is considered unrelated
# (with Gemini embeddings related exchanges score about 0.2, unrelated ones 0.4 and more)
MEMORY_MAX_DISTANCE = 0.33
# Collection names carry the embedding they were built with; vectors of different models cannot be mixed
COLLECTIONS = {"documents": "documents_gemini", "long_term_memory": "long_term_memory_gemini"}


_lock = threading.Lock()
_collections: dict = {}


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

def add_document_chunks(user_id: str, file_id: str, source: str, chunks: list[dict]) -> None:
    """chunks: {"text", "page"} as produced by processor.split_documents (page may be None)."""
    col = _documents()
    base = {"user_id": user_id, "file_id": file_id, "source": source}
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


def search_documents(user_id: str, query_vector: list[float], k: int = 8) -> list[dict]:
    res = _documents().query(query_embeddings=[query_vector], n_results=k, where={"user_id": user_id})
    return [
        {"text": doc, "source": meta.get("source", "Unknown"), "page": meta.get("page")}
        for doc, meta in zip(res["documents"][0], res["metadatas"][0])
    ]


def indexed_file_ids(user_id: str) -> set[str]:
    """Files that really have chunks here (the store is wiped when a host without a disk restarts)."""
    metas = _documents().get(where={"user_id": user_id}, include=["metadatas"])["metadatas"]
    return {m["file_id"] for m in metas}


def delete_document(user_id: str, file_id: str) -> None:
    _documents().delete(where={"$and": [{"user_id": user_id}, {"file_id": file_id}]})


# ---------- conversation memory ----------

def remember(user_id: str, session_id: str, message_id: str, question: str, answer: str, created_at: str) -> None:
    text = f"User asked: {question}\nAssistant answered: {answer[:1500]}"
    _memory().add(
        ids=[message_id],
        embeddings=llm.embed([text], "RETRIEVAL_DOCUMENT"),
        documents=[text],
        metadatas=[{"user_id": user_id, "session_id": session_id, "created_at": created_at}],
    )


def recall(user_id: str, session_id: str, query_vector: list[float], k: int = 3) -> list[str]:
    """Related exchanges from the user's OTHER chats (the current chat is covered by short-term memory)."""
    res = _memory().query(
        query_embeddings=[query_vector],
        n_results=k,
        where={"$and": [{"user_id": user_id}, {"session_id": {"$ne": session_id}}]},
    )
    return [
        doc for doc, dist in zip(res["documents"][0], res["distances"][0])
        if dist <= MEMORY_MAX_DISTANCE
    ]


def forget_all(user_id: str) -> None:
    _memory().delete(where={"user_id": user_id})


def memory_count(user_id: str) -> int:
    return len(_memory().get(where={"user_id": user_id}, include=[])["ids"])
