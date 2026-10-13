"""Conflicts between documents that were found when answering. Closing one is a permission of its own."""
from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..core.database import conflicts
from ..core.security import has_permission, require_permission
from ..core.utils import clean, oid, paginate
from ..schemas import ConflictResolveIn
from ..services import audit_service, conflict_service

router = APIRouter(prefix="/conflicts", tags=["conflicts"])


def get_conflict(organization_id: str, conflict_id: str) -> dict:
    record = conflicts.find_one({"_id": oid(conflict_id), "organization_id": organization_id})
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Conflict not found")
    return record


@router.get("")
def list_conflicts(
    status_: str = Query("", alias="status", pattern="^(open|resolved)?$"),
    kind: str = Query("", pattern="^(conflict|needs_review)?$"),
    page: int = Query(1, ge=1), page_size: int = Query(20, ge=1, le=100),
    user: dict = Depends(require_permission("conflicts.view")),
):
    query: dict = {"organization_id": user["organization_id"]}
    if status_:
        query["status"] = status_
    if kind:
        query["kind"] = kind
    return paginate(conflicts, query, page, page_size, [("last_seen_at", -1)])


@router.get("/{conflict_id}")
def view_conflict(conflict_id: str, user: dict = Depends(require_permission("conflicts.view"))):
    return clean(get_conflict(user["organization_id"], conflict_id))


@router.post("/{conflict_id}/resolve")
def resolve_conflict(conflict_id: str, body: ConflictResolveIn, user: dict = Depends(require_permission("conflicts.view"))):
    record = get_conflict(user["organization_id"], conflict_id)
    if not has_permission(user, "conflicts.resolve"):
        audit_service.record(user, "conflict.resolve", "conflict", conflict_id, "denied", "no permission to close conflicts")
        raise HTTPException(
            status.HTTP_403_FORBIDDEN, "You do not have the permission to close a conflict. Ask an administrator for access."
        )
    if record["status"] != "open":
        raise HTTPException(status.HTTP_409_CONFLICT, "This conflict is already resolved.")
    try:
        updated = conflict_service.resolve(user, record, body.decision, body.document_id, body.note)
    except ValueError as e:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, str(e))
    return clean(updated)
