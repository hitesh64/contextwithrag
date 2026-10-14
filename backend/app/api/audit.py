"""Audit history and the dashboard figures. Every number is counted from the organization's own records."""
from collections import Counter
from datetime import datetime, timedelta, timezone

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


def _utc(value: datetime | None) -> datetime | None:
    """Stored datetimes may come back without a zone (mongomock); they are UTC."""
    return value.replace(tzinfo=timezone.utc) if value is not None and value.tzinfo is None else value


CRITICALITY_RANK = {"critical": 0, "high": 1, "medium": 2, "low": 3}
UNRESOLVED = ["open", "in_progress"]
WORK_ORDER_CLOSED = ["completed", "cancelled", "rejected"]


def _maintenance_figures(org: str, since: datetime, days: int) -> dict:
    """Reliability figures of the period, from the factory's own breakdown and work order records.

    MTTR: mean recorded downtime per breakdown (records without a downtime value are left out).
    MTBF and availability: calendar time of the assets in service (not inactive), as if they ran round the clock,
    minus the recorded downtime; per breakdown, and as a share. Plant schedules are not recorded, so this is the
    24/7 basis, stated as such on the dashboard."""
    end = now()
    records = [
        {**r, "reported_at": _utc(r["reported_at"])}
        for r in breakdowns.find(
            {"organization_id": org, "reported_at": {"$gte": since}},
            {"reported_at": 1, "downtime_minutes": 1, "asset_code": 1, "error_code": 1, "resolution_status": 1},
        )
    ]
    in_service = assets.count_documents({"organization_id": org, "status": {"$ne": "inactive"}})
    downtimes = [r["downtime_minutes"] for r in records if r.get("downtime_minutes") is not None]
    downtime_minutes = sum(downtimes)
    calendar_hours = days * 24 * in_service
    running_hours = max(0.0, calendar_hours - downtime_minutes / 60)
    kpis = {
        "breakdowns": len(records),
        "downtime_minutes": downtime_minutes,
        "mttr_minutes": round(sum(downtimes) / len(downtimes), 1) if downtimes else None,
        "mtbf_hours": round(running_hours / len(records), 1) if records and in_service else None,
        "availability_pct": round(100 * running_hours / calendar_hours, 2) if calendar_hours else None,
        "assets_in_service": in_service,
    }

    # Trend: daily buckets for a month or less, weekly beyond
    step = timedelta(days=1 if days <= 31 else 7)
    buckets = []
    start = since
    while start < end:
        buckets.append({"start": start, "breakdowns": 0, "downtime_minutes": 0})
        start += step
    for r in records:
        index = min(len(buckets) - 1, int((r["reported_at"] - since) / step))
        if index >= 0:
            buckets[index]["breakdowns"] += 1
            buckets[index]["downtime_minutes"] += r.get("downtime_minutes") or 0

    names = {a["asset_code"]: a for a in assets.find({"organization_id": org}, {"asset_code": 1, "name": 1, "criticality": 1, "status": 1})}
    per_asset = Counter(r["asset_code"] for r in records)
    codes = Counter((r.get("error_code") or "").strip().upper() for r in records if (r.get("error_code") or "").strip())

    # Needs attention: assets with an unresolved breakdown (any date) or under maintenance, most critical first
    unresolved = Counter(
        r["asset_code"] for r in breakdowns.find({"organization_id": org, "resolution_status": {"$in": UNRESOLVED}}, {"asset_code": 1})
    )
    attention = [
        {"asset_code": code, "name": a.get("name", ""), "criticality": a.get("criticality", "medium"),
         "status": a.get("status", "active"), "unresolved_breakdowns": unresolved.get(code, 0)}
        for code, a in names.items() if unresolved.get(code) or a.get("status") == "under_maintenance"
    ]
    attention.sort(key=lambda a: (CRITICALITY_RANK.get(a["criticality"], 9), -a["unresolved_breakdowns"], a["asset_code"]))

    open_orders = Counter(
        w.get("priority", "medium")
        for w in work_orders.find({"organization_id": org, "status": {"$nin": WORK_ORDER_CLOSED}}, {"priority": 1})
    )
    cycle = [
        (_utc(w["completed_at"]) - _utc(w["created_at"])).total_seconds() / 3600
        for w in work_orders.find({"organization_id": org, "status": "completed", "completed_at": {"$gte": since}},
                                  {"created_at": 1, "completed_at": 1})
        if w.get("completed_at") and w.get("created_at")
    ]
    return {
        "kpis": kpis,
        "trend": buckets,
        "trend_step_days": step.days,
        "top_error_codes": [{"error_code": c, "breakdowns": n} for c, n in codes.most_common(5)],
        "repeat_assets": [
            {"asset_code": c, "name": names.get(c, {}).get("name", ""), "breakdowns": n}
            for c, n in per_asset.most_common() if n >= 2
        ][:5],
        "attention": attention[:8],
        "work_orders_open_by_priority": dict(open_orders),
        "work_order_cycle_hours": round(sum(cycle) / len(cycle), 1) if cycle else None,
        "assets_by_criticality": _count_by(assets, org, "criticality"),
        "asset_names": {c: a.get("name", "") for c, a in names.items()},
    }


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
        **_maintenance_figures(org, since, days),
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
