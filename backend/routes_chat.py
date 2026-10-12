import base64
import binascii
import re
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from . import llm, vector_store
from .config import settings
from .database import audit, messages, sessions
from .schemas import ChatIn, ChatOut
from .security import get_current_user, reader_department

router = APIRouter(prefix="/api", tags=["chat"])

_CODE_BLOCK = re.compile(r"(```.*?```)", re.S)
# [2] or [1, 3] - but not an index such as items[2], nor a markdown link [2](...)
_MARKER = re.compile(r"(?<!\w)\[(\d+(?:\s*,\s*\d+)*)\](?!\()")


def _own_session(session_id: str, user_id: str) -> dict:
    session = None
    if ObjectId.is_valid(session_id):
        session = sessions.find_one({"_id": ObjectId(session_id), "user_id": user_id})
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Chat not found (it may have expired)")
    return session


def _source_line(doc: dict) -> str:
    line = f"Source: {doc['source']}"
    if doc.get("page"):
        line += f", page {doc['page']}"
    if doc.get("category"):
        line += f" | {doc['category']}"
    if doc.get("effective_date"):
        line += f" | effective {doc['effective_date']}"
    return line


def _build_prompt(
    question: str, docs: list[dict], history: list[dict], memories: list[str], photo_reading: str | None = None
) -> str:
    context = "\n\n".join(
        f"[{n}] {_source_line(d)}\n{d['text']}" for n, d in enumerate(docs, start=1)
    )
    recent = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history)
    past = "\n\n".join(memories)
    return (
        f"LONG-TERM MEMORY (related earlier exchanges):\n{past or '(none)'}\n\n"
        f"DOCUMENT CONTEXT:\n{context or '(no documents available)'}\n\n"
        f"RECENT CONVERSATION:\n{recent or '(new chat)'}\n\n"
        + (f"PHOTO READING:\n{photo_reading}\n\n" if photo_reading else "") +
        f"USER QUESTION:\n{question}\n\n"
        # Without this at the very end, a question in English about a Japanese manual is answered in Japanese
        "Write the whole answer in the language of the USER QUESTION, not in the language of the documents."
    )


def _cite(answer: str, docs: list[dict]) -> tuple[str, list[dict]]:
    """Keep only the passages the answer really cites and number them 1, 2, 3 in the order they appear.

    The model is given 8 passages and usually uses two or three; without renumbering the reader
    would get an answer that cites [3] and [7] only.
    """
    renumbered: dict[int, int] = {}

    def renumber(match: re.Match) -> str:
        given = [int(n) for n in match.group(1).split(",")]
        valid = [n for n in given if 1 <= n <= len(docs)]
        if not valid:
            return match.group(0)  # not a citation, e.g. "[2024]"
        return "".join(f"[{renumbered.setdefault(n, len(renumbered) + 1)}]" for n in valid)

    parts = _CODE_BLOCK.split(answer)
    # Odd parts are code blocks, where [1] is code and not a citation
    parts[::2] = [_MARKER.sub(renumber, part) for part in parts[::2]]
    citations = [{"number": new, **docs[old - 1]} for old, new in renumbered.items()]
    return "".join(parts), citations


@router.post("/chat", response_model=ChatOut)
def chat(body: ChatIn, user: dict = Depends(get_current_user)):
    user_id = user["id"]
    now = datetime.now(timezone.utc)

    if body.session_id:
        session_id = str(_own_session(body.session_id, user_id)["_id"])
    else:
        session_id = None

    # Short-term memory (MongoDB): the last few messages of this chat
    history = []
    if session_id:
        history = list(
            messages.find({"session_id": session_id}).sort("created_at", -1).limit(settings.SHORT_TERM_TURNS)
        )[::-1]

    image = None
    if body.image:
        try:
            image = (base64.b64decode(body.image, validate=True), body.image_type)
        except binascii.Error:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "The photo could not be read.")

    # Long-term memory (ChromaDB): uploaded documents + related past conversations
    try:
        # A photo is first put into words (the alarm code on the display, the part, the damage),
        # because the manuals can only be searched with text
        photo_reading = llm.read_photo(*image) if image else None
        asked = f"{body.message}\n{photo_reading}" if photo_reading else body.message
        # One embedding of the question serves both searches
        query_vector = llm.embed_query(asked)
        docs = vector_store.search_documents(reader_department(user), asked, query_vector)
        # Each exchange is stored under the id of its assistant message
        in_history = {str(m["_id"]) for m in history if m["role"] == "assistant"}
        memories = vector_store.recall(user_id, query_vector, in_history)
        answer = llm.generate(_build_prompt(body.message, docs, history, memories, photo_reading), image)
    except llm.LLMError as e:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(e))

    answer, citations = _cite(answer, docs)
    sources = list(dict.fromkeys(c["source"] for c in citations))

    if session_id is None:
        session_id = str(
            sessions.insert_one(
                {"user_id": user_id, "title": body.message[:60], "created_at": now, "updated_at": now}
            ).inserted_id
        )
    else:
        sessions.update_one({"_id": ObjectId(session_id)}, {"$set": {"updated_at": now}})

    base = {"session_id": session_id, "user_id": user_id}
    # The photo itself is not kept, only that there was one and what was read from it
    messages.insert_one(
        {**base, "role": "user", "content": body.message, "sources": [], "has_photo": bool(image), "created_at": now}
    )
    reply_id = messages.insert_one(
        {**base, "role": "assistant", "content": answer, "sources": sources, "citations": citations,
         "photo_reading": photo_reading,
         "created_at": datetime.now(timezone.utc)}
    ).inserted_id

    # A bank must be able to show who asked what and which document the answer rested on
    audit.insert_one({
        "user_id": user_id, "username": user["username"], "department": user["department"],
        "question": body.message, "answered": bool(citations),
        "citations": [{"source": c["source"], "page": c["page"]} for c in citations],
        "created_at": now,
    })

    try:
        vector_store.remember(user_id, session_id, str(reply_id), asked, answer, now.isoformat())
    except llm.LLMError:
        pass  # the answer is saved; the exchange is added to long-term memory at the next start

    return ChatOut(
        session_id=session_id, answer=answer, sources=sources, citations=citations, photo_reading=photo_reading
    )


@router.get("/sessions")
def list_sessions(user: dict = Depends(get_current_user)):
    cursor = sessions.find({"user_id": user["id"]}).sort("updated_at", -1).limit(50)
    return [{"id": str(s["_id"]), "title": s["title"], "updated_at": s["updated_at"]} for s in cursor]


@router.get("/sessions/{session_id}/messages")
def session_messages(session_id: str, user: dict = Depends(get_current_user)):
    _own_session(session_id, user["id"])
    cursor = messages.find({"session_id": session_id}).sort("created_at", 1)
    return [
        {"role": m["role"], "content": m["content"], "sources": m.get("sources", []),
         "citations": m.get("citations", []), "has_photo": m.get("has_photo", False),
         "photo_reading": m.get("photo_reading")}
        for m in cursor
    ]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, user: dict = Depends(get_current_user)):
    _own_session(session_id, user["id"])
    messages.delete_many({"session_id": session_id})
    sessions.delete_one({"_id": ObjectId(session_id)})
    # A chat the user deletes is forgotten for good (one that merely expires stays in long-term memory)
    vector_store.forget_session(user["id"], session_id)


@router.get("/memory")
def memory_stats(user: dict = Depends(get_current_user)):
    return {
        "long_term_items": vector_store.memory_count(user["id"]),
        "short_term_ttl_hours": settings.SHORT_TERM_TTL_HOURS,
    }
