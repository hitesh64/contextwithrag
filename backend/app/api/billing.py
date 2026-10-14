"""The registration fee, paid through Razorpay Checkout, and the platform owner's list of payments.

A company becomes active only when this server has seen the payment at Razorpay: a valid Checkout signature and
the payment itself fetched from Razorpay (captured, the right amount, for this company's order). Three ways lead
there, all to the same _settle(), so a payment is counted once whichever arrives first:
- /billing/verify, called by the browser right after Checkout;
- /billing/webhook, called by Razorpay (when a webhook secret is set);
- GET /billing, which asks Razorpay about the open order (a browser closed during payment).
"""
import json
import logging

from fastapi import APIRouter, Depends, Header, HTTPException, Query, Request, status

from ..core.config import settings
from ..core.database import organizations, payments, users
from ..core.security import get_signed_in_user, require_platform_owner
from ..core.utils import clean, now, oid
from ..schemas import PaymentVerifyIn
from ..services import audit_service, mailer, razorpay

log = logging.getLogger(__name__)
router = APIRouter(tags=["billing"])


def _organization(organization_id: str) -> dict:
    org = organizations.find_one({"_id": oid(organization_id)}, {"logo": 0})
    if org is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    return org


def _paise() -> int:
    return settings.REGISTRATION_FEE * 100


def _bad_gateway(e: razorpay.RazorpayError) -> HTTPException:
    return HTTPException(status.HTTP_502_BAD_GATEWAY, str(e))


def _settle(record: dict, payment: dict) -> bool:
    """Count a Razorpay payment for its order: True once the company's fee is paid.

    Checked against Razorpay's own record, never against what the browser says."""
    if record["status"] == "paid":
        return True
    if (payment.get("order_id") != record["order_id"] or payment.get("amount") != record["amount"] * 100
            or payment.get("currency") != "INR"):
        log.error("Razorpay payment %s does not belong to order %s", payment.get("id"), record["order_id"])
        return False
    if payment.get("status") == "authorized":
        try:
            payment = razorpay.capture(payment["id"], payment["amount"])
        except razorpay.RazorpayError:
            payment = razorpay.fetch_payment(payment["id"])  # captured a moment ago by the webhook or the browser
    if payment.get("status") != "captured":
        if payment.get("status") == "failed":
            payments.update_one({"_id": record["_id"]}, {"$set": {"error": payment.get("error_description") or "Payment failed."}})
        return False
    paid = payments.update_one(
        {"_id": record["_id"], "status": {"$ne": "paid"}},
        {"$set": {"status": "paid", "payment_id": payment["id"], "method": payment.get("method", ""),
                  "paid_at": now(), "error": ""}},
    )
    if paid.modified_count:
        org_id = oid(record["organization_id"])
        organizations.update_one({"_id": org_id, "status": "pending_payment"},
                                 {"$set": {"status": "active", "activated_at": now()}})
        admin = users.find_one({"organization_id": record["organization_id"], "role": "admin"}, sort=[("created_at", 1)])
        if admin:
            admin["id"] = str(admin["_id"])
            audit_service.record(admin, "payment.paid", "payment", str(record["_id"]), detail=f"Razorpay {payment['id']}")
            mailer.company_registered(organizations.find_one({"_id": org_id}, {"logo": 0}), admin,
                                      payments.find_one({"_id": record["_id"]}))
    return True


def _check_open_order(organization_id: str) -> None:
    """Ask Razorpay whether the company's open order was paid while nobody was watching."""
    record = payments.find_one({"organization_id": organization_id, "status": "unpaid"}, sort=[("created_at", -1)])
    if record is None or not razorpay.configured():
        return
    try:
        for payment in razorpay.order_payments(record["order_id"]):
            if payment.get("status") in ("authorized", "captured") and _settle(record, payment):
                return
    except razorpay.RazorpayError as e:
        log.warning("Could not ask Razorpay about order %s: %s", record["order_id"], e)


def _payment_out(record: dict) -> dict:
    return clean(record)


@router.get("/billing/fee")
def registration_fee():
    """Public: shown on the registration form before anyone is signed in."""
    return {"fee": settings.REGISTRATION_FEE, "configured": razorpay.configured()}


@router.get("/billing")
def billing(user: dict = Depends(get_signed_in_user)):
    """What the company must pay, and its payments so far."""
    if _organization(user["organization_id"]).get("status") == "pending_payment":
        _check_open_order(user["organization_id"])
    org = _organization(user["organization_id"])
    records = payments.find({"organization_id": user["organization_id"], "order_id": {"$exists": True}}).sort("created_at", -1)
    return {
        "status": org.get("status", "active"), "organization_name": org["name"], "fee": settings.REGISTRATION_FEE,
        "configured": razorpay.configured(), "test_mode": razorpay.test_mode(),
        "payments": [_payment_out(p) for p in records.limit(5)],
    }


@router.post("/billing/order")
def create_order(user: dict = Depends(get_signed_in_user)):
    """A Razorpay order for the fee, opened by Checkout in the browser. An unpaid order is reused."""
    if user["role"] != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the administrator who registered the company pays.")
    org_id = user["organization_id"]
    org = _organization(org_id)
    if org.get("status", "active") == "active":
        raise HTTPException(status.HTTP_409_CONFLICT, "Your company is already active.")
    if not razorpay.configured():
        raise HTTPException(status.HTTP_503_SERVICE_UNAVAILABLE, "Payments are not set up on this server yet.")
    record = payments.find_one({"organization_id": org_id, "status": "unpaid", "amount": settings.REGISTRATION_FEE},
                               sort=[("created_at", -1)])
    if record is None:
        try:
            order = razorpay.create_order(_paise(), f"org-{org_id}", {"organization_id": org_id, "organization": org["name"]})
        except razorpay.RazorpayError as e:
            raise _bad_gateway(e)
        record = {
            "organization_id": org_id, "organization_name": org["name"], "order_id": order["id"],
            "amount": settings.REGISTRATION_FEE, "status": "unpaid", "test_mode": razorpay.test_mode(),
            "created_by": user["id"], "created_by_email": user["email"], "created_at": now(), "error": "",
        }
        record["_id"] = payments.insert_one(record).inserted_id
    return {
        "key_id": settings.RAZORPAY_KEY_ID, "order_id": record["order_id"], "amount": record["amount"] * 100,
        "currency": "INR", "name": settings.APP_NAME, "description": f"Registration of {org['name']}",
        "prefill": {"name": user["name"], "email": user["email"]},
    }


@router.post("/billing/verify")
def verify_payment(body: PaymentVerifyIn, user: dict = Depends(get_signed_in_user)):
    """Checkout's answer after a payment: the signature, then the payment itself at Razorpay."""
    record = payments.find_one({"organization_id": user["organization_id"], "order_id": body.razorpay_order_id})
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "This order does not belong to your company.")
    if not razorpay.valid_payment_signature(body.razorpay_order_id, body.razorpay_payment_id, body.razorpay_signature):
        audit_service.record(user, "payment.verify", "payment", str(record["_id"]), result="denied", detail="bad signature")
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "The payment could not be verified.")
    try:
        paid = _settle(record, razorpay.fetch_payment(body.razorpay_payment_id))
    except razorpay.RazorpayError as e:
        raise _bad_gateway(e)
    if not paid:
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED, "Razorpay has not confirmed this payment.")
    return {"organization_status": _organization(user["organization_id"]).get("status", "active")}


@router.post("/billing/webhook", include_in_schema=False)
async def webhook(request: Request, x_razorpay_signature: str = Header("")):
    """payment.captured / order.paid from Razorpay, for a payment whose browser never reported back."""
    body = await request.body()
    if not razorpay.valid_webhook_signature(body, x_razorpay_signature):
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid signature")
    event = json.loads(body)
    payment = ((event.get("payload") or {}).get("payment") or {}).get("entity") or {}
    record = payments.find_one({"order_id": payment.get("order_id")}) if payment.get("order_id") else None
    if record and event.get("event") in ("payment.captured", "payment.authorized", "order.paid"):
        try:
            _settle(record, payment)
        except razorpay.RazorpayError as e:
            raise _bad_gateway(e)  # Razorpay sends the webhook again later
    return {"ok": True}


@router.get("/platform/payments")
def list_payments(
    status_: str = Query("", alias="status"), page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100),
    _: dict = Depends(require_platform_owner),
):
    query = {"order_id": {"$exists": True}, **({"status": status_} if status_ else {})}
    cursor = payments.find(query).sort("created_at", -1).skip((page - 1) * page_size).limit(page_size)
    return {"items": [_payment_out(p) for p in cursor], "total": payments.count_documents(query), "page": page, "page_size": page_size}
