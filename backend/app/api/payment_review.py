"""The page behind the Accept / Reject buttons in the owner's payment mail.

The link carries a random token (only its hash is stored); it works once, for a limited time, and only while the
payment waits for review. Opening the link changes nothing: mail scanners open links by themselves, so the
decision needs one more click on this page (a POST).
"""
import html
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Form, Query, Response
from fastapi.responses import HTMLResponse

from ..core.config import settings
from ..core.database import payments, users
from ..core.utils import now
from . import billing

router = APIRouter(include_in_schema=False)

_HEADERS = {
    "Cache-Control": "no-store", "Referrer-Policy": "no-referrer", "X-Frame-Options": "DENY",
    "X-Content-Type-Options": "nosniff",
}
_MARK = {True: ("#16a34a", "OK"), False: ("#dc2626", "FAILED"), None: ("#d97706", "UNSURE")}


def _waiting(token: str, fields: dict | None = None) -> dict | None:
    """The payment this link decides, while it still waits for review and the link has not expired."""
    if not token:
        return None
    payment = payments.find_one(
        {"review_token_hash": billing.review_token_hash(token), "status": "needs_review"}, fields or {"screenshot": 0}
    )
    if payment is None or payment["review_expires_at"] <= now():
        return None
    return payment


def _page(title: str, body: str, status_code: int = 200) -> HTMLResponse:
    return HTMLResponse(f"""<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1"><meta name="robots" content="noindex">
<title>{html.escape(title)} · {settings.APP_NAME}</title>
<style>
body{{margin:0;background:#f1f5f9;font:15px/1.5 Arial,sans-serif;color:#0f172a}}
main{{max-width:560px;margin:24px auto;padding:24px 20px;background:#fff;border:1px solid #e2e8f0;border-radius:14px}}
h1{{font-size:20px;margin:0 0 4px}} .muted{{color:#64748b}} ul{{padding-left:18px}}
.facts{{display:grid;grid-template-columns:auto 1fr;gap:4px 14px;margin:14px 0}}
.shot{{display:block;max-width:100%;max-height:520px;margin:12px auto;border:1px solid #e2e8f0;border-radius:10px}}
.warn{{background:#fef3c7;padding:10px 12px;border-radius:8px}}
form{{margin-top:16px;padding:14px;border:1px solid #e2e8f0;border-radius:10px}}
form.chosen{{border:2px solid #2563eb}} textarea{{width:100%;box-sizing:border-box;font:inherit;margin:6px 0 10px}}
button{{border:0;border-radius:8px;padding:12px 22px;font:bold 15px Arial,sans-serif;color:#fff;cursor:pointer}}
.accept{{background:#16a34a}} .reject{{background:#dc2626}}
@media (max-width:600px){{main{{margin:0;border-radius:0;min-height:100vh}}}}
</style></head><body><main>{body}</main></body></html>""", status_code=status_code, headers=_HEADERS)


def _gone() -> HTMLResponse:
    return _page("Link no longer valid", f"""<h1>This link no longer works</h1>
<p class="muted">The payment was already decided, or the link expired after {billing.REVIEW_LINK_DAYS} days.</p>
<p>Sign in as the platform owner and open the Payments page: <a href="{html.escape(settings.APP_BASE_URL)}/#/payments">Payments</a></p>""", 410)


@router.get("/payment-review")
def review_page(token: str = Query(""), action: str = Query("")):
    payment = _waiting(token)
    if payment is None:
        return _gone()
    t = html.escape(token)
    checks = "".join(
        f"<li><b style='color:{_MARK[c['ok']][0]}'>{_MARK[c['ok']][1]}</b> {html.escape(c['label'])}"
        + (f" <span class='muted'>· {html.escape(c['detail'])}</span>" if c["detail"] else "") + "</li>"
        for c in payment["checks"]
    )
    verdict = "All checks passed." if payment.get("checks_passed") else "The check found problems: look carefully."
    return _page("Confirm payment", f"""<h1>Confirm a registration payment</h1>
<p class="muted">Sent {payment['created_at'].astimezone(ZoneInfo(settings.LOCAL_TIMEZONE)).strftime('%d %b %Y, %H:%M')} by {html.escape(payment['submitted_by_email'])}</p>
<div class="facts"><span class="muted">Company</span><b>{html.escape(payment['organization_name'])}</b>
<span class="muted">Amount</span><b>Rs {payment['amount']}</b><span class="muted">UTR</span><b>{html.escape(payment['utr'])}</b></div>
<p><b>{verdict}</b></p><ul>{checks}</ul>
<img class="shot" src="/payment-review/screenshot?token={t}" alt="Payment screenshot sent by the company">
<p class="warn">Accept only if you find UTR <b>{html.escape(payment['utr'])}</b> for Rs {payment['amount']} in your bank or
UPI app. The AI check cannot see your bank account.</p>
<form method="post" action="/payment-review" class="{'chosen' if action == 'accept' else ''}">
<input type="hidden" name="token" value="{t}"><input type="hidden" name="decision" value="accept">
<button class="accept" type="submit">Accept payment: give {html.escape(payment['organization_name'])} access</button></form>
<form method="post" action="/payment-review" class="{'chosen' if action == 'reject' else ''}">
<input type="hidden" name="token" value="{t}"><input type="hidden" name="decision" value="reject">
<label>Reason, sent to the company (optional)<textarea name="note" rows="2" maxlength="300"></textarea></label>
<button class="reject" type="submit">Reject payment</button></form>""")


@router.get("/payment-review/screenshot")
def review_screenshot(token: str = Query("")):
    payment = _waiting(token, {"screenshot": 1, "screenshot_type": 1, "review_expires_at": 1})
    if payment is None:
        return Response(status_code=404, headers=_HEADERS)
    return Response(bytes(payment["screenshot"]), media_type=payment["screenshot_type"], headers=_HEADERS)


@router.post("/payment-review")
def review_decision(token: str = Form(""), decision: str = Form(""), note: str = Form("", max_length=300)):
    payment = _waiting(token)
    if payment is None or decision not in ("accept", "reject"):
        return _gone()
    owner = users.find_one({"email": settings.PLATFORM_OWNER_EMAIL}) if settings.PLATFORM_OWNER_EMAIL else None
    if owner:
        owner["id"] = str(owner["_id"])
    payment = billing.decide(payment, decision, note.strip(), owner)
    company = html.escape(payment["organization_name"])
    if payment["status"] == "accepted":
        return _page("Payment accepted", f"""<h1 style="color:#16a34a">Payment accepted</h1>
<p><b>{company}</b> can now use {settings.APP_NAME}. Its administrator gets the "registered" email.</p>""")
    reason = "; ".join(c["detail"] for c in payment["checks"] if c["ok"] is False and c["key"] == "utr_unused")
    return _page("Payment rejected", f"""<h1 style="color:#dc2626">Payment rejected</h1>
<p>{company} was told by email and can send a new proof.{' ' + html.escape(reason) if reason else ''}</p>""")
