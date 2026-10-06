"""ChromaDB: LONG-TERM memory.

Two persistent collections, both filtered per user:
  - documents         : chunks of the user's uploaded files (knowledge base)
  - long_term_memory  : past question/answer pairs, recalled semantically in later chats

Embeddings use Chroma's built-in all-MiniLM-L6-v2 (ONNX) model, which runs locally.
"""
from functools import lru_cache

import chromadb

from .config import settings

# Chunks embedded per call. The local ONNX model's memory grows with the batch size: 100 at a time
# peaks near 900 MB and gets the server killed on a 512 MB host, 4 at a time stays under 400 MB.
BATCH = 4
# Cosine distance above which a remembered conversation is considered unrelated
MEMORY_MAX_DISTANCE = 0.75


@lru_cache
def _client():
    return chromadb.PersistentClient(path=str(settings.CHROMA_DIR))


def _collection(name: str):
    return _client().get_or_create_collection(name, metadata={"hnsw:space": "cosine"})


def _documents():
    return _collection("documents")


def _memory():
    return _collection("long_term_memory")


# ---------- knowledge base ----------

def add_document_chunks(user_id: str, file_id: str, source: str, chunks: list[dict]) -> None:
    """chunks: {"text", "page"} as produced by processor.split_documents (page may be None)."""
    col = _documents()
    base = {"user_id": user_id, "file_id": file_id, "source": source}
    for i in range(0, len(chunks), BATCH):
        batch = chunks[i:i + BATCH]
        col.add(
            ids=[f"{file_id}_{i + j}" for j in range(len(batch))],
            documents=[c["text"] for c in batch],
            metadatas=[{**base, "page": c["page"]} if c["page"] else base for c in batch],
        )


def search_documents(user_id: str, query: str, k: int = 8) -> list[dict]:
    res = _documents().query(query_texts=[query], n_results=k, where={"user_id": user_id})
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
    _memory().add(
        ids=[message_id],
        documents=[f"User asked: {question}\nAssistant answered: {answer[:1500]}"],
        metadatas=[{"user_id": user_id, "session_id": session_id, "created_at": created_at}],
    )


def recall(user_id: str, session_id: str, query: str, k: int = 3) -> list[str]:
    """Related exchanges from the user's OTHER chats (the current chat is covered by short-term memory)."""
    res = _memory().query(
        query_texts=[query],
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
