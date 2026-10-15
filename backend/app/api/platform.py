"""The platform owner's console: every company registered on this server. The owner has no factory workspace of
their own; the company record that holds the owner's account is left out of the list."""
import re

from fastapi import APIRouter, Depends, Query

from ..core.database import assets, documents, organizations, payments, users
from ..core.security import require_platform_owner
from ..core.utils import oid

router = APIRouter(tags=["platform"])

# Companies created before the registration fee existed have no status and count as active
_ACTIVE = {"$or": [{"status": "active"}, {"status": {"$exists": False}}]}


def _company_out(org: dict) -> dict:
    org_id = str(org["_id"])
    admin = users.find_one({"organization_id": org_id, "role": "admin"}, {"name": 1, "email": 1}, sort=[("created_at", 1)])
    paid = payments.find_one({"organization_id": org_id, "status": "paid"}, {"amount": 1, "paid_at": 1, "test_mode": 1},
                             sort=[("paid_at", -1)])
    return {
        "id": org_id,
        "name": org["name"],
        "status": org.get("status", "active"),
        "created_at": org.get("created_at"),
        "admin_name": admin["name"] if admin else "",
        "admin_email": admin["email"] if admin else "",
        "users": users.count_documents({"organization_id": org_id}),
        "active_users": users.count_documents({"organization_id": org_id, "is_active": {"$ne": False}}),
        "assets": assets.count_documents({"organization_id": org_id}),
        "documents": documents.count_documents({"organization_id": org_id}),
        "paid_amount": paid["amount"] if paid else None,
        "paid_at": paid["paid_at"] if paid else None,
        "test_payment": bool(paid and paid.get("test_mode")),
    }


@router.get("/platform/companies")
def list_companies(
    q: str = Query("", max_length=100),
    status_: str = Query("", alias="status", pattern="^(active|pending_payment|rejected)?$"),
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=100),
    owner: dict = Depends(require_platform_owner),
):
    everyone = {"_id": {"$ne": oid(owner["organization_id"])}}
    query = dict(everyone)
    if q:
        query["name"] = {"$regex": re.escape(q), "$options": "i"}
    if status_ == "active":
        query.update(_ACTIVE)
    elif status_:
        query["status"] = status_
    cursor = organizations.find(query, {"logo": 0}).sort("created_at", -1).skip((page - 1) * page_size).limit(page_size)
    company_ids = [str(o["_id"]) for o in organizations.find(everyone, {"_id": 1})]
    return {
        "items": [_company_out(org) for org in cursor],
        "total": organizations.count_documents(query),
        "page": page,
        "page_size": page_size,
        "summary": {
            "companies": len(company_ids),
            "active": organizations.count_documents({**everyone, **_ACTIVE}),
            "pending_payment": organizations.count_documents({**everyone, "status": "pending_payment"}),
            "users": users.count_documents({"organization_id": {"$in": company_ids}}),
        },
    }
