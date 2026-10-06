"""Look inside the ChromaDB data (read-only).

Usage:
    python view_chroma.py                 summary of both collections
    python view_chroma.py docs            list stored document chunks
    python view_chroma.py memory          list remembered question/answer pairs
    python view_chroma.py search "text"   semantic search in the document chunks
Add a number at the end to change how many rows are shown (default 10), e.g.  docs 30
"""
import sys
from collections import Counter

import chromadb

from backend import llm
from backend.config import settings
from backend.vector_store import COLLECTIONS as NAMES

COLLECTIONS = {"docs": NAMES["documents"], "memory": NAMES["long_term_memory"]}


def show(text: str, width: int = 300) -> str:
    text = " ".join(text.split())
    return text if len(text) <= width else text[:width] + "…"


def summary(client) -> None:
    print(f"ChromaDB folder: {settings.CHROMA_DIR}\n")
    for col in client.list_collections():
        metas = col.get(include=["metadatas"])["metadatas"]
        print(f"[{col.name}]  {len(metas)} items")
        if col.name.startswith("documents"):
            for (user, source), n in sorted(Counter((m["user_id"], m["source"]) for m in metas).items()):
                print(f"    user {user}  {source}: {n} chunks")
        else:
            for user, n in sorted(Counter(m["user_id"] for m in metas).items()):
                print(f"    user {user}: {n} remembered exchanges")
        print()


def rows(client, name: str, limit: int) -> None:
    data = client.get_collection(name).get(limit=limit, include=["documents", "metadatas"])
    for id_, doc, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        print(f"id: {id_}\nmeta: {meta}\ntext: {show(doc)}\n")
    print(f"({len(data['ids'])} rows shown)")


def search(client, query: str, limit: int) -> None:
    res = client.get_collection(COLLECTIONS["docs"]).query(query_embeddings=[llm.embed_query(query)], n_results=limit)
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        page = f", page {meta['page']}" if meta.get("page") else ""
        print(f"distance {dist:.3f}  {meta['source']}{page}\n{show(doc)}\n")


def main() -> None:
    args = sys.argv[1:]
    limit = int(args.pop()) if args and args[-1].isdigit() else 10
    client = chromadb.PersistentClient(path=str(settings.CHROMA_DIR))
    if not args:
        summary(client)
    elif args[0] in COLLECTIONS:
        rows(client, COLLECTIONS[args[0]], limit)
    elif args[0] == "search" and len(args) > 1:
        search(client, " ".join(args[1:]), limit)
    else:
        print(__doc__)


if __name__ == "__main__":
    main()
