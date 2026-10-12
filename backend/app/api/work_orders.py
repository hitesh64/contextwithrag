"""Work orders: drafts (written by hand or generated from evidence), editing, approval and progress."""
from fastapi import APIRouter, Depends, HTTPException, Query, status

from ..core.database import work_orders
from ..core.security import get_current_user, require_role
from ..core.utils import clean, now, oid, paginate
from ..schemas import CommentIn, TransitionIn, WorkOrderCreate, WorkOrderGenerate, WorkOrderUpdate
from ..services import audit_service, llm, work_order_service
from .assets import get_asset
from .chat import ai_limiter, model_unavailable

router = APIRouter(prefix="/work-orders", tags=["work orders"])


def _get(organization_id: str, order_id: str) -> dict:
    order = work_orders.find_one({"_id": oid(order_id), "organization_id": organization_id})
    if order is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Work order not found")
    return order


def _out(order: dict, user: dict) -> dict:
    out = clean(order)
    # What this user may do next, so the interface shows only buttons the backend will accept
    out["allowed_transitions"] = work_order_service.allowed_transitions(user, order)
    out["can_edit"] = work_order_service.may_edit(user, order)
    return out


@router.get("")
def list_work_orders(
    status_: str = Query("", alias="status"),
    asset_id: str = "",
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: dict = Depends(get_current_user),
):
    query: dict = {"organization_id": user["organization_id"]}
    if status_:
        query["status"] = status_
    if asset_id:
        query["asset_id"] = asset_id
    return paginate(work_orders, query, page, page_size, [("created_at", -1)])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_work_order(body: WorkOrderCreate, user: dict = Depends(require_role("technician"))):
    """A draft written by hand."""
    asset = get_asset(user["organization_id"], body.asset_id)
    order = work_order_service.new_work_order(
        user, asset, title=body.title, description=body.description, priority=body.priority,
        proposed_checklist=[work_order_service.checklist_item(i.step, [], set()) for i in body.checklist],
    )
    audit_service.record(user, "work_order.create", "work_order", str(order["_id"]), detail=order["order_no"])
    return _out(order, user)


@router.post("/generate", status_code=status.HTTP_201_CREATED)
def generate_work_order(body: WorkOrderGenerate, user: dict = Depends(require_role("technician"))):
    """A draft generated from the asset's SOPs and breakdown history. It only creates a draft record."""
    ai_limiter.check(user["id"])
    asset = get_asset(user["organization_id"], body.asset_id)
    try:
        order = work_order_service.generate_draft(user, asset, body.problem)
    except llm.LLMError as e:
        raise model_unavailable(e)
    audit_service.record(user, "work_order.generate", "work_order", str(order["_id"]), detail=order["order_no"])
    return _out(order, user)


@router.get("/{order_id}")
def view_work_order(order_id: str, user: dict = Depends(get_current_user)):
    return _out(_get(user["organization_id"], order_id), user)


@router.patch("/{order_id}")
def edit_work_order(order_id: str, body: WorkOrderUpdate, user: dict = Depends(require_role("technician"))):
    """Edit a draft. Once submitted, a work order is frozen so that what was approved is what gets done."""
    order = _get(user["organization_id"], order_id)
    if not work_order_service.may_edit(user, order):
        raise HTTPException(
            status.HTTP_409_CONFLICT if order["status"] not in ("draft", "rejected") else status.HTTP_403_FORBIDDEN,
            "Only a draft can be edited, by its author or a manager.",
        )
    changes = body.model_dump(exclude_none=True, exclude={"checklist"})
    if body.checklist is not None:
        valid = {ref["n"] for ref in order["source_references"]}
        changes["proposed_checklist"] = [work_order_service.checklist_item(i.step, i.sources, valid) for i in body.checklist]
    if changes:
        work_orders.update_one({"_id": order["_id"]}, {"$set": {**changes, "updated_at": now()}})
        audit_service.record(user, "work_order.edit", "work_order", order_id, detail=", ".join(changes))
    return _out(work_orders.find_one({"_id": order["_id"]}), user)


@router.post("/{order_id}/approve")
def approve_work_order(order_id: str, body: CommentIn | None = None, user: dict = Depends(get_current_user)):
    order = _get(user["organization_id"], order_id)
    return _out(work_order_service.transition(user, order, "approved", body.comment if body else ""), user)


@router.post("/{order_id}/transition")
def transition_work_order(order_id: str, body: TransitionIn, user: dict = Depends(get_current_user)):
    order = _get(user["organization_id"], order_id)
    return _out(work_order_service.transition(user, order, body.to, body.comment), user)
