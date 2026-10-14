"""Razorpay: orders for the registration fee, and proof that a payment for an order really happened.

The flow (https://razorpay.com/docs/payments/payment-gateway/web-integration/standard/):
1. The server creates an order for the fee; the browser opens Razorpay Checkout with it.
2. After paying, Checkout hands the browser a payment id and a signature: HMAC-SHA256 of "order_id|payment_id"
   with the key secret. Only Razorpay and this server know the secret, so a valid signature cannot be made up.
3. The server checks the signature and also asks Razorpay for the payment itself (status, amount, order) before
   the company becomes active. A payment only authorised, not captured, is captured here.

Test keys (rzp_test_...) work the same way with test money: Checkout offers test cards and UPI IDs, nothing is charged.
"""
import hashlib
import hmac

import httpx

from ..core.config import settings

API = "https://api.razorpay.com/v1"
TIMEOUT = 20


class RazorpayError(Exception):
    """Razorpay could not be reached or refused the request."""


def configured() -> bool:
    return bool(settings.RAZORPAY_KEY_ID and settings.RAZORPAY_KEY_SECRET)


def test_mode() -> bool:
    return settings.RAZORPAY_KEY_ID.startswith("rzp_test_")


def _call(method: str, path: str, json: dict | None = None) -> dict:
    try:
        response = httpx.request(method, f"{API}{path}", json=json, timeout=TIMEOUT,
                                 auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))
    except httpx.HTTPError as e:
        raise RazorpayError(f"Razorpay could not be reached ({type(e).__name__}). Try again.") from e
    if response.status_code >= 400:
        try:
            reason = response.json()["error"]["description"]
        except (ValueError, KeyError, TypeError):
            reason = response.text[:200]
        raise RazorpayError(f"Razorpay refused the request ({response.status_code}): {reason}")
    return response.json()


def create_order(amount_paise: int, receipt: str, notes: dict) -> dict:
    return _call("POST", "/orders", {"amount": amount_paise, "currency": "INR", "receipt": receipt, "notes": notes})


def fetch_payment(payment_id: str) -> dict:
    return _call("GET", f"/payments/{payment_id}")


def order_payments(order_id: str) -> list[dict]:
    return _call("GET", f"/orders/{order_id}/payments").get("items", [])


def capture(payment_id: str, amount_paise: int) -> dict:
    return _call("POST", f"/payments/{payment_id}/capture", {"amount": amount_paise, "currency": "INR"})


def _same(expected: str, signature: str) -> bool:
    return hmac.compare_digest(expected, (signature or "").strip())


def valid_payment_signature(order_id: str, payment_id: str, signature: str) -> bool:
    message = f"{order_id}|{payment_id}".encode()
    return _same(hmac.new(settings.RAZORPAY_KEY_SECRET.encode(), message, hashlib.sha256).hexdigest(), signature)


def valid_webhook_signature(body: bytes, signature: str) -> bool:
    if not settings.RAZORPAY_WEBHOOK_SECRET:
        return False
    return _same(hmac.new(settings.RAZORPAY_WEBHOOK_SECRET.encode(), body, hashlib.sha256).hexdigest(), signature)
