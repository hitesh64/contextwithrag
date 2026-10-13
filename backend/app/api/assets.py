"""Asset register: the machines of a factory."""
import re

from fastapi import APIRouter, Depends, HTTPException, Query, status
from pymongo.errors import DuplicateKeyError

from ..core.database import assets, breakdowns, documents, work_orders
from ..core.security import get_current_user, has_permission, require_permission
from ..core.utils import EXPORT_LIMIT, clean, now, oid, paginate, xlsx_download
from ..schemas import AssetCreate, AssetUpdate
from ..services import audit_service, factory_context

router = APIRouter(prefix="/assets", tags=["assets"])


def get_asset(organization_id: str, asset_id: str) -> dict:
    """An asset of this organization; one that belongs to another organization does not exist for the caller."""
    asset = assets.find_one({"_id": oid(asset_id), "organization_id": organization_id})
    if asset is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Asset not found")
    return asset


@router.get("")
def list_assets(
    q: str = Query("", max_length=100),
    status_: str = Query("", alias="status"),
    criticality: str = "",
    asset_type: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: dict = Depends(require_permission("assets.view")),
):
    query: dict = {"organization_id": user["organization_id"]}
    # Archived assets stay in the records but leave the everyday list
    query["status"] = status_ if status_ else {"$ne": "archived"}
    if criticality:
        query["criticality"] = criticality
    if asset_type:
        query["asset_type"] = asset_type
    if q:
        pattern = {"$regex": re.escape(q), "$options": "i"}
        query["$or"] = [{f: pattern} for f in ("asset_code", "name", "location", "manufacturer", "model")]
    return paginate(assets, query, page, page_size, [("asset_code", 1)])


@router.get("/export")
def export_assets(user: dict = Depends(require_permission("assets.view"))):
    """The whole asset register, archived machines included, as an Excel file."""
    found = list(assets.find({"organization_id": user["organization_id"]}).sort("asset_code", 1).limit(EXPORT_LIMIT))
    audit_service.record(user, "asset.export", "asset", detail=f"{len(found)} records")
    return xlsx_download("assets.xlsx", [
        ("Asset code", "asset_code"), ("Name", "name"), ("Type", "asset_type"), ("Manufacturer", "manufacturer"),
        ("Model", "model"), ("Serial number", "serial_number"), ("Location", "location"),
        ("Criticality", "criticality"), ("Status", "status"), ("Created", "created_at"),
    ], found)


@router.get("/options")
def asset_options(user: dict = Depends(get_current_user)):
    """Code and name of every asset in use, for the pick lists of forms. Open to anyone logged in: a person who
    may report a breakdown or ask about a machine has to be able to name it, even without the Assets section."""
    query = {"organization_id": user["organization_id"], "status": {"$ne": "archived"}}
    found = assets.find(query, {"asset_code": 1, "name": 1}).sort("asset_code", 1)
    return [{"id": str(a["_id"]), "asset_code": a["asset_code"], "name": a["name"]} for a in found]


@router.post("", status_code=status.HTTP_201_CREATED)
def create_asset(body: AssetCreate, user: dict = Depends(require_permission("assets.manage"))):
    asset = {"organization_id": user["organization_id"], **body.model_dump(), "created_at": now(), "updated_at": now()}
    try:
        asset["_id"] = assets.insert_one(asset).inserted_id
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, f"Asset code {body.asset_code} already exists.")
    audit_service.record(user, "asset.create", "asset", str(asset["_id"]), detail=body.asset_code)
    return clean(asset)


@router.get("/{asset_id}")
def view_asset(asset_id: str, user: dict = Depends(require_permission("assets.view"))):
    """The asset with everything connected to it: documents, breakdown facts and work orders."""
    org = user["organization_id"]
    asset = get_asset(org, asset_id)
    out = clean(asset)
    # A section the user may not see is left out (None), not shown as empty
    see_documents, see_breakdowns, see_orders = (
        has_permission(user, key) for key in ("documents.view", "breakdowns.view", "work_orders.view")
    )
    out["documents"] = [
        clean(d) for d in documents.find({"organization_id": org, "asset_ids": asset_id}).sort("created_at", -1)
    ] if see_documents else None
    out["breakdown_summary"] = factory_context.breakdown_summary(org, asset_id) if see_breakdowns else None
    out["recent_breakdowns"] = [
        clean(b) for b in breakdowns.find({"organization_id": org, "asset_id": asset_id}).sort("reported_at", -1).limit(10)
    ] if see_breakdowns else None
    out["work_orders"] = [
        clean(w) for w in work_orders.find({"organization_id": org, "asset_id": asset_id}).sort("created_at", -1).limit(10)
    ] if see_orders else None
    return out


@router.get("/{asset_id}/breakdown-summary")
def asset_breakdown_summary(asset_id: str, user: dict = Depends(require_permission("breakdowns.view"))):
    get_asset(user["organization_id"], asset_id)
    return factory_context.breakdown_summary(user["organization_id"], asset_id)


@router.patch("/{asset_id}")
def update_asset(asset_id: str, body: AssetUpdate, user: dict = Depends(require_permission("assets.manage"))):
    asset = get_asset(user["organization_id"], asset_id)
    changes = body.model_dump(exclude_none=True)
    if changes:
        assets.update_one({"_id": asset["_id"]}, {"$set": {**changes, "updated_at": now()}})
        audit_service.record(user, "asset.update", "asset", asset_id, detail=", ".join(changes))
    return clean(assets.find_one({"_id": asset["_id"]}))


@router.post("/{asset_id}/archive")
def archive_asset(asset_id: str, user: dict = Depends(require_permission("assets.manage"))):
    """Retire an asset. Its documents, breakdowns and work orders are kept."""
    asset = get_asset(user["organization_id"], asset_id)
    assets.update_one({"_id": asset["_id"]}, {"$set": {"status": "archived", "updated_at": now()}})
    audit_service.record(user, "asset.archive", "asset", asset_id, detail=asset["asset_code"])
    return clean(assets.find_one({"_id": asset["_id"]}))
