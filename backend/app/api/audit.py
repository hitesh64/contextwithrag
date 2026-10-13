"""Audit history and the dashboard figures. Every number is counted from the organization's own records."""
from datetime import timedelta

from fastapi import APIRouter, Depends, Query

from ..core.database import assets, audit_events, breakdowns, chat_logs, documents, work_orders
from ..core.security import require_permission
from ..core.utils import now, paginate

router = APIRouter(tags=["audit"])


@router.get("/audit")
def list_audit(
    action: str = "",
    resource_type: str = "",
    result: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_permission("audit.view")),
):
    query: dict = {"organization_id": user["organization_id"]}
    if action:
        query["action"] = action
    if resource_type:
        query["resource_type"] = resource_type
    if result:
        query["result"] = result
    return paginate(audit_events, query, page, page_size, [("created_at", -1)])


def _count_by(collection, organization_id: str, field: str) -> dict:
    rows = collection.aggregate([
        {"$match": {"organization_id": organization_id}}, {"$group": {"_id": f"${field}", "count": {"$sum": 1}}}
    ])
    return {r["_id"]: r["count"] for r in rows}


@router.get("/dashboard")
def dashboard(days: int = Query(90, ge=7, le=730), user: dict = Depends(require_permission("dashboard.view"))):
    org = user["organization_id"]
    since = now() - timedelta(days=days)
    downtime = list(breakdowns.aggregate([
        {"$match": {"organization_id": org, "reported_at": {"$gte": since}}},
        {"$group": {"_id": "$asset_code", "downtime_minutes": {"$sum": {"$ifNull": ["$downtime_minutes", 0]}}, "breakdowns": {"$sum": 1}}},
        {"$sort": {"downtime_minutes": -1}},
        {"$limit": 10},
    ]))
    return {
        "period_days": days,
        "period_start": since,
        "assets": _count_by(assets, org, "status"),
        "documents": _count_by(documents, org, "status"),
        "work_orders": _count_by(work_orders, org, "status"),
        "breakdowns": _count_by(breakdowns, org, "resolution_status"),
        "downtime_by_asset": [
            {"asset_code": d["_id"], "downtime_minutes": d["downtime_minutes"], "breakdowns": d["breakdowns"]} for d in downtime
        ],
        "questions_asked": chat_logs.count_documents({"organization_id": org, "created_at": {"$gte": since}}),
        "questions_unanswered": chat_logs.count_documents(
            {"organization_id": org, "created_at": {"$gte": since}, "insufficient_evidence": True}
        ),
    }
