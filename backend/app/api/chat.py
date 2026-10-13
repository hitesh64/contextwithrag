"""Grounded question answering over the factory's documents and breakdown records."""
from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..core.config import settings
from ..core.database import chat_logs
from ..core.security import get_current_user, require_role
from ..core.utils import RateLimiter, now, paginate
from ..schemas import ChatIn
from ..services import answering, audit_service, llm
from .assets import get_asset
from .documents import get_document

router = APIRouter(tags=["chat"])
ai_limiter = RateLimiter(settings.AI_RATE_PER_MINUTE)


def model_unavailable(error: llm.LLMError) -> HTTPException:
    code = status.HTTP_429_TOO_MANY_REQUESTS if isinstance(error, llm.QuotaError) else status.HTTP_503_SERVICE_UNAVAILABLE
    return HTTPException(code, str(error))


@router.post("/chat")
def chat(body: ChatIn, user: dict = Depends(get_current_user)):
    org = user["organization_id"]
    ai_limiter.check(user["id"])
    # Both filters are looked up inside the caller's organization; an id from elsewhere is "not found"
    asset = get_asset(org, body.asset_id) if body.asset_id else None
    if body.document_id:
        get_document(org, body.document_id)

    try:
        result = answering.answer(org, body.question, asset, body.document_id)
    except llm.LLMError as e:
        raise model_unavailable(e)
    result["request_id"] = audit_service.request_id.get()

    # Kept so that unanswered questions show which documents the library is missing
    chat_logs.insert_one({
        "organization_id": org,
        "user_id": user["id"],
        "user_name": user["name"],
        "question": body.question,
        "asset_id": body.asset_id,
        "insufficient_evidence": result["insufficient_evidence"],
        "conflict": result["conflict"],
        "cited_document_ids": sorted({c["document_id"] for c in result["citations"] if c["type"] == "document"}),
        "request_id": result["request_id"],
        "created_at": now(),
    })
    return result


@router.get("/chat/unanswered")
def unanswered_questions(
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_role("maintenance_manager")),
):
    """Questions the records could not answer: a to-do list of documents to add."""
    query = {"organization_id": user["organization_id"], "insufficient_evidence": True}
    return paginate(chat_logs, query, page, page_size, [("created_at", -1)])
