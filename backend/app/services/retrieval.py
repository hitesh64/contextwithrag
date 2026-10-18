"""ChromaDB: the searchable chunks of every organization's documents.

Chunks are found by hybrid search: the vector ranking and a keyword (BM25) ranking of the same
chunks are merged, so exact strings such as part numbers and error codes are found too.

Every chunk carries its organization_id, and every search is filtered by the organization of
the logged-in user. Nothing in this module accepts an organization from the browser.
"""
import re
import threading
from collections.abc import Callable

import chromadb

from . import llm
from ..core.config import settings
from ..core.database import documents
from .keyword_search import KeywordIndex, fuse

BATCH = 100
# How many chunks each of the two rankings contributes before they are merged
CANDIDATES = 20
# Bump when chunk size, overlap or metadata change; documents must then be reprocessed
CHUNKING_VERSION = 1

_lock = threading.Lock()
_collection = None
# organization_id -> (chunk ids, chunks, KeywordIndex); dropped when that organization's library changes
_keyword_cache: dict[str, tuple[list[str], list[dict], KeywordIndex]] = {}


def collection_name() -> str:
    """Vectors of different embedding models or chunking versions cannot be mixed, so the name carries both."""
    model = re.sub(r"[^a-z0-9]+", "_", settings.EMBEDDING_MODEL.lower()).strip("_")
    return f"chunks_{model}_v{CHUNKING_VERSION}"


def init() -> None:
    """Open the store exactly once. Two requests opening a fresh store at the same time corrupt its setup."""
    global _collection
    with _lock:
        if _collection is None:
            client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
            # embedding_function=None: vectors are always supplied, Chroma never loads its own model
            _collection = client.get_or_create_collection(
                collection_name(), metadata={"hnsw:space": "cosine"}, embedding_function=None
            )


def _chunks():
    if _collection is None:
        init()
    return _collection


def _as_chunk(id_: str, text: str, meta: dict) -> dict:
    return {
        "chunk_id": id_,
        "text": text,
        "organization_id": meta["organization_id"],
        "document_id": meta["document_id"],
        "chunk_index": meta["chunk_index"],
        # Absent when the parser could not establish a location; never guessed
        "page": meta.get("page"),
        "section": meta.get("section"),
    }


def index_document(
    organization_id: str, document_id: str, chunks: list[dict], progress: Callable[[int, int], None] | None = None
) -> None:
    """Replace the indexed chunks of one document. chunks: {"text", "page", "section"}.

    Everything is embedded first, so a failed embedding stores nothing; ids are fixed by position,
    so running this again for the same document can never leave duplicates. progress(done, total)
    is called after each embedding batch.
    """
    texts = [c["text"] for c in chunks]
    vectors = []
    for start in range(0, len(texts), llm.EMBED_BATCH):
        vectors.extend(llm.embed(texts[start:start + llm.EMBED_BATCH], "RETRIEVAL_DOCUMENT"))
        if progress:
            progress(len(vectors), len(texts))
    delete_document(organization_id, document_id)
    col = _chunks()
    for start in range(0, len(chunks), BATCH):
        batch = chunks[start:start + BATCH]
        metadatas = []
        for offset, chunk in enumerate(batch):
            meta = {"organization_id": organization_id, "document_id": document_id, "chunk_index": start + offset}
            if chunk.get("page"):
                meta["page"] = chunk["page"]
            if chunk.get("section"):
                meta["section"] = chunk["section"]
            metadatas.append(meta)
        col.upsert(
            ids=[f"{document_id}:{start + offset}" for offset in range(len(batch))],
            embeddings=vectors[start:start + BATCH],
            documents=[c["text"] for c in batch],
            metadatas=metadatas,
        )
    _keyword_cache.pop(organization_id, None)


def delete_document(organization_id: str, document_id: str) -> None:
    _chunks().delete(where={"document_id": document_id})
    _keyword_cache.pop(organization_id, None)


def count_chunks(document_id: str) -> int:
    return len(_chunks().get(where={"document_id": document_id}, include=[])["ids"])


def _keywords(organization_id: str) -> tuple[list[str], list[dict], KeywordIndex]:
    cached = _keyword_cache.get(organization_id)
    if cached is None:
        res = _chunks().get(where={"organization_id": organization_id}, include=["documents", "metadatas"])
        chunks = [_as_chunk(i, d, m) for i, d, m in zip(res["ids"], res["documents"], res["metadatas"])]
        cached = _keyword_cache[organization_id] = (res["ids"], chunks, KeywordIndex([c["text"] for c in chunks]))
    return cached


def search(organization_id: str, question: str, k: int, document_ids: list[str] | None = None) -> list[dict]:
    """The best k chunks of this organization, by meaning (vectors) and by wording (BM25) together.

    document_ids: search only inside these documents (None: the whole library of the organization).
    """
    if document_ids is not None and not document_ids:
        return []
    where = {"organization_id": organization_id}
    if document_ids is not None:
        where = {"$and": [where, {"document_id": {"$in": document_ids}}]}

    ids, chunks, index = _keywords(organization_id)
    if not ids:
        return []
    allowed = None if document_ids is None else set(document_ids)
    by_wording = [
        ids[p] for p in index.search(question, len(ids)) if allowed is None or chunks[p]["document_id"] in allowed
    ][:CANDIDATES]

    vector = llm.embed([question], "RETRIEVAL_QUERY")[0]
    res = _chunks().query(query_embeddings=[vector], n_results=CANDIDATES, where=where)
    by_meaning = res["ids"][0]

    found = {i: _as_chunk(i, d, m) for i, d, m in zip(by_meaning, res["documents"][0], res["metadatas"][0])}
    position = {id_: p for p, id_ in enumerate(ids)}
    for id_ in by_wording:
        found.setdefault(id_, chunks[position[id_]])

    best = [found[id_] for id_ in fuse([by_meaning, by_wording], k)]
    # The filters above already guarantee this; a chunk of another organization must never get through
    return [c for c in best if c["organization_id"] == organization_id]


def reconcile() -> int:
    """Remove chunks whose document no longer exists in MongoDB (a deletion that failed half-way)."""
    res = _chunks().get(include=["metadatas"])
    indexed = {m["document_id"] for m in res["metadatas"]}
    known = {str(d["_id"]) for d in documents.find({}, {"_id": 1})}
    orphans = indexed - known
    for document_id in orphans:
        _chunks().delete(where={"document_id": document_id})
    if orphans:
        _keyword_cache.clear()
    return len(orphans)
