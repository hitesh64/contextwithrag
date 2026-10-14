"""The registration fee: the company's QR code and proof of payment, and the platform owner's review."""
import hashlib
import re
import secrets
from datetime import timedelta

from bson import Binary
from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, Response, UploadFile, status
from pymongo.errors import DuplicateKeyError

from ..core.config import settings
from ..core.database import organizations, payments, users
from ..core.security import get_signed_in_user, require_platform_owner
from ..core.utils import RateLimiter, clean, now, oid, read_image
from ..schemas import PaymentDecisionIn
from ..services import audit_service, llm, mailer, payment_check

router = APIRouter(tags=["billing"])
proof_limiter = RateLimiter(3)

SCREENSHOT_KB = 2048
# Each proof costs one model call, and a free key allows about 20 a day for the whole platform
PROOFS_PER_DAY = 5
# How long the Accept / Reject link in the owner's mail works
REVIEW_LINK_DAYS = 7
_NO_PICTURE = {"screenshot": 0}
_PRIVATE = ("screenshot", "accepted_utr", "review_token_hash", "review_expires_at")


def _payment_out(payment: dict) -> dict:
    return clean({k: v for k, v in payment.items() if k not in _PRIVATE})


def review_token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def _organization(organization_id: str) -> dict:
    org = organizations.find_one({"_id": oid(organization_id)}, {"logo": 0})
    if org is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    return org


def _accept(payment: dict, decided_by: str, note: str = "") -> dict:
    """Mark the payment accepted and the company active; mail the company once, when it becomes active."""
    decided = {"decided_at": now(), "decided_by": decided_by, "decision_note": note}
    try:
        payments.update_one({"_id": payment["_id"]}, {"$set": {"status": "accepted", "accepted_utr": payment["utr"], **decided}})
    except DuplicateKeyError:
        # Another company's payment with this UTR was accepted a moment earlier
        failed = payment_check.check("utr_unused", "UTR not used before", False, "This UTR was already accepted for another company.")
        payments.update_one({"_id": payment["_id"]}, {"$set": {"status": "rejected", **decided}, "$push": {"checks": failed}})
        return payments.find_one({"_id": payment["_id"]}, _NO_PICTURE)
    org_id = oid(payment["organization_id"])
    activated = organizations.update_one(
        {"_id": org_id, "status": "pending_payment"}, {"$set": {"status": "active", "activated_at": now()}}
    )
    if activated.modified_count:
        admin = users.find_one({"organization_id": payment["organization_id"], "role": "admin"}, sort=[("created_at", 1)])
        if admin:
            mailer.company_registered(organizations.find_one({"_id": org_id}, {"logo": 0}), admin, payment)
    return payments.find_one({"_id": payment["_id"]}, _NO_PICTURE)


@router.get("/billing/fee")
def registration_fee():
    """Public: shown on the registration form before anyone is signed in."""
    return {"fee": settings.REGISTRATION_FEE, "configured": bool(settings.UPI_ID)}


@router.get("/billing")
def billing(user: dict = Depends(get_signed_in_user)):
    """What the company must pay, the QR code to pay it, and its proofs so far."""
    org = _organization(user["organization_id"])
    state = org.get("status", "active")
    out = {
        "status": state, "organization_name": org["name"], "fee": settings.REGISTRATION_FEE,
        "upi_id": settings.UPI_ID, "payee_name": settings.UPI_PAYEE_NAME, "configured": bool(settings.UPI_ID),
        "reference": payment_check.reference(user["organization_id"]),
        "payments": [_payment_out(p) for p in payments.find({"organization_id": user["organization_id"]}, _NO_PICTURE).sort("created_at", -1).limit(5)],
    }
    if state != "active" and settings.UPI_ID:
        out["upi_uri"] = payment_check.upi_uri(user["organization_id"])
        out["qr_svg"] = payment_check.qr_svg(out["upi_uri"])
    return out


@router.post("/billing/proof", status_code=status.HTTP_201_CREATED)
def submit_proof(utr: str = Form(...), screenshot: UploadFile = File(...), user: dict = Depends(get_signed_in_user)):
    """The UTR and screenshot of the UPI payment. Checked at once: rejected, or needs_review for the platform owner.

    Never accepted here: a made-up screenshot can pass every check, so the owner confirms each payment against
    the bank account. checks_passed tells the owner whether the check found anything wrong."""
    if user["role"] != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the administrator who registered the company sends the payment.")
    org_id = user["organization_id"]
    org = _organization(org_id)
    if org.get("status", "active") == "active":
        raise HTTPException(status.HTTP_409_CONFLICT, "Your company is already active.")
    if not settings.UPI_ID:
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Payments are not set up on this server yet (UPI_ID).")
    utr = re.sub(r"\s", "", utr)
    if not payment_check.UTR_PATTERN.match(utr):
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "The UTR is the 12-digit UPI transaction number in your UPI app.")
    if payments.find_one({"organization_id": org_id, "status": "needs_review"}):
        raise HTTPException(status.HTTP_409_CONFLICT, "Your previous payment is waiting for review. You will get an email.")
    proof_limiter.check(org_id)
    if payments.count_documents({"organization_id": org_id, "created_at": {"$gte": now() - timedelta(days=1)}}) >= PROOFS_PER_DAY:
        raise HTTPException(status.HTTP_429_TOO_MANY_REQUESTS, f"At most {PROOFS_PER_DAY} payment proofs a day. Try again tomorrow.")
    data, kind = read_image(screenshot, SCREENSHOT_KB)
    image_hash = payment_check.screenshot_hash(data)

    checks = payment_check.database_checks(org_id, utr, image_hash)
    read = None
    if not any(c["ok"] is False for c in checks):  # a spent UTR or screenshot is refused without a model call
        try:
            read = payment_check.read_screenshot(data, kind)
            checks += payment_check.screenshot_checks(read, utr, org["created_at"], org_id)
        except llm.LLMError as e:
            checks.append(payment_check.check("ai", "AI check of the screenshot", None, str(e)))
    verdict = payment_check.verdict(checks)
    payment = {
        "organization_id": org_id, "organization_name": org["name"],
        "submitted_by": user["id"], "submitted_by_email": user["email"],
        "amount": settings.REGISTRATION_FEE, "utr": utr,
        "screenshot": Binary(data), "screenshot_type": kind, "screenshot_hash": image_hash,
        "ai_read": read, "checks": checks, "checks_passed": verdict == "passed",
        "status": "rejected" if verdict == "rejected" else "needs_review",
        "created_at": now(), "decided_at": None, "decided_by": None, "decision_note": "",
    }
    review_link = None
    if payment["status"] == "needs_review":
        # The owner decides from the mail: only the hash of this random link is kept, like a login token
        token = secrets.token_urlsafe(32)
        payment["review_token_hash"] = review_token_hash(token)
        payment["review_expires_at"] = now() + timedelta(days=REVIEW_LINK_DAYS)
        review_link = f"{settings.APP_BASE_URL}/payment-review?token={token}"
    payment["_id"] = payments.insert_one(payment).inserted_id
    audit_service.record(user, "payment.submit", "payment", str(payment["_id"]), result=payment["status"], detail=f"UTR {utr}")
    if review_link:
        mailer.payment_for_owner(org, payment, review_link, data, kind)
    return {"payment": _payment_out(payment), "organization_status": _organization(org_id).get("status", "active")}


@router.get("/platform/payments")
def list_payments(
    status_: str = Query("", alias="status"), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
    _: dict = Depends(require_platform_owner),
):
    query = {"status": status_} if status_ else {}
    cursor = payments.find(query, _NO_PICTURE).sort("created_at", -1).skip((page - 1) * page_size).limit(page_size)
    return {"items": [_payment_out(p) for p in cursor], "total": payments.count_documents(query), "page": page, "page_size": page_size}


@router.get("/platform/payments/{payment_id}/screenshot")
def payment_screenshot(payment_id: str, _: dict = Depends(require_platform_owner)):
    payment = payments.find_one({"_id": oid(payment_id)}, {"screenshot": 1, "screenshot_type": 1})
    if payment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    return Response(bytes(payment["screenshot"]), media_type=payment["screenshot_type"], headers={"X-Content-Type-Options": "nosniff"})


@router.post("/platform/payments/{payment_id}/decision")
def decide_payment(payment_id: str, body: PaymentDecisionIn, owner: dict = Depends(require_platform_owner)):
    """Accept a payment found in the bank account, or reject one, also after it was accepted (money never arrived)."""
    payment = payments.find_one({"_id": oid(payment_id)}, _NO_PICTURE)
    if payment is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    if body.decision == "accept" and payment["status"] == "accepted":
        raise HTTPException(status.HTTP_409_CONFLICT, "This payment is already accepted.")
    return _payment_out(decide(payment, body.decision, body.note, owner))


def decide(payment: dict, decision: str, note: str, owner: dict | None) -> dict:
    """The owner's decision, from the Payments page or from the link in the mail. Either way the link stops working."""
    decided_by = owner["email"] if owner else settings.PLATFORM_OWNER_EMAIL
    payments.update_one({"_id": payment["_id"]}, {"$unset": {"review_token_hash": "", "review_expires_at": ""}})
    if decision == "accept":
        payment = _accept(payment, decided_by, note)
    else:
        if payment["status"] == "accepted":
            # The company loses access until it pays: its money never reached the account
            organizations.update_one({"_id": oid(payment["organization_id"])}, {"$set": {"status": "pending_payment"}})
        payments.update_one({"_id": payment["_id"]}, {
            "$set": {"status": "rejected", "decided_at": now(), "decided_by": decided_by, "decision_note": note},
            "$unset": {"accepted_utr": ""},
        })
        payment = payments.find_one({"_id": payment["_id"]}, _NO_PICTURE)
        mailer.payment_rejected(payment["submitted_by_email"], payment["organization_name"], payment["utr"], note)
    if owner:
        audit_service.record(owner, f"payment.{decision}", "payment", str(payment["_id"]), result=payment["status"],
                             detail=f"{payment['organization_name']}, UTR {payment['utr']}")
    return payment
