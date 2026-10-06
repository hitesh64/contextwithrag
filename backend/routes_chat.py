from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from . import llm, vector_store
from .config import settings
from .database import messages, sessions
from .schemas import ChatIn, ChatOut
from .security import get_current_user

router = APIRouter(prefix="/api", tags=["chat"])


def _own_session(session_id: str, user_id: str) -> dict:
    session = None
    if ObjectId.is_valid(session_id):
        session = sessions.find_one({"_id": ObjectId(session_id), "user_id": user_id})
    if session is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Chat not found (it may have expired)")
    return session


def _build_prompt(question: str, docs: list[dict], history: list[dict], memories: list[str]) -> str:
    context = "\n\n".join(
        f"--- Source: {d['source']}{', page ' + str(d['page']) if d.get('page') else ''} ---\n{d['text']}"
        for d in docs
    )
    recent = "\n".join(f"{m['role'].upper()}: {m['content']}" for m in history)
    past = "\n\n".join(memories)
    return (
        f"LONG-TERM MEMORY (related exchanges from earlier chats):\n{past or '(none)'}\n\n"
        f"DOCUMENT CONTEXT:\n{context or '(no documents uploaded)'}\n\n"
        f"RECENT CONVERSATION:\n{recent or '(new chat)'}\n\n"
        f"USER QUESTION:\n{question}"
    )


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

    # Long-term memory (ChromaDB): uploaded documents + related past conversations
    docs = vector_store.search_documents(user_id, body.message)
    memories = vector_store.recall(user_id, session_id or "", body.message)

    try:
        answer = llm.generate(_build_prompt(body.message, docs, history, memories))
    except llm.LLMError as e:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, str(e))

    sources = sorted({d["source"] for d in docs})

    if session_id is None:
        session_id = str(
            sessions.insert_one(
                {"user_id": user_id, "title": body.message[:60], "created_at": now, "updated_at": now}
            ).inserted_id
        )
    else:
        sessions.update_one({"_id": ObjectId(session_id)}, {"$set": {"updated_at": now}})

    base = {"session_id": session_id, "user_id": user_id}
    messages.insert_one({**base, "role": "user", "content": body.message, "sources": [], "created_at": now})
    reply_id = messages.insert_one(
        {**base, "role": "assistant", "content": answer, "sources": sources,
         "created_at": datetime.now(timezone.utc)}
    ).inserted_id

    vector_store.remember(user_id, session_id, str(reply_id), body.message, answer, now.isoformat())

    return ChatOut(session_id=session_id, answer=answer, sources=sources)


@router.get("/sessions")
def list_sessions(user: dict = Depends(get_current_user)):
    cursor = sessions.find({"user_id": user["id"]}).sort("updated_at", -1).limit(50)
    return [{"id": str(s["_id"]), "title": s["title"], "updated_at": s["updated_at"]} for s in cursor]


@router.get("/sessions/{session_id}/messages")
def session_messages(session_id: str, user: dict = Depends(get_current_user)):
    _own_session(session_id, user["id"])
    cursor = messages.find({"session_id": session_id}).sort("created_at", 1)
    return [{"role": m["role"], "content": m["content"], "sources": m.get("sources", [])} for m in cursor]


@router.delete("/sessions/{session_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_session(session_id: str, user: dict = Depends(get_current_user)):
    _own_session(session_id, user["id"])
    messages.delete_many({"session_id": session_id})
    sessions.delete_one({"_id": ObjectId(session_id)})


@router.get("/memory")
def memory_stats(user: dict = Depends(get_current_user)):
    return {
        "long_term_items": vector_store.memory_count(user["id"]),
        "short_term_ttl_hours": settings.SHORT_TERM_TTL_HOURS,
    }


@router.delete("/memory", status_code=status.HTTP_204_NO_CONTENT)
def clear_memory(user: dict = Depends(get_current_user)):
    vector_store.forget_all(user["id"])
