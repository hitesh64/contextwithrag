"""Checking a registration fee paid by UPI to the platform's own UPI ID.

A plain UPI payment sends no signal to this server, so the company sends its proof: the UTR (the 12-digit UPI
transaction number) and a screenshot of the payment. The proof is checked in two steps:

1. Against the database: the same UTR or the same screenshot used for another company is refused.
2. By the model: Gemini reads the screenshot (amount, status, payee, UTR, date, signs of editing) and these
   facts are compared with what was expected here, by the rules below, not by the model.

A clear mismatch: rejected at once, and the company may send another proof. Everything else waits for the
platform owner, who confirms the UTR in the bank account; the checks tell the owner what looked wrong, if anything.

Why the owner always confirms: the check cannot prove that money arrived. A made-up screenshot can pass every
check; only the receiving bank account shows the truth.
"""
import hashlib
import json
import re
from datetime import date, datetime, time, timedelta
from urllib.parse import quote
from zoneinfo import ZoneInfo

import qrcode
import qrcode.image.svg

from ..core.config import settings
from ..core.database import payments
from . import llm

UTR_PATTERN = re.compile(r"^\d{12}$")
REFERENCE_PATTERN = re.compile(r"CBR[0-9A-F]{6}", re.IGNORECASE)
# A phone clock can be a little ahead of this server's; a payment later than this is in the future
CLOCK_SLACK = timedelta(minutes=10)

SYSTEM = """You read one screenshot of a UPI payment (Google Pay, PhonePe, Paytm, BHIM or a bank app).
Report only what is visible in the picture; never guess or fill in a value that is not shown.
Answer with one JSON object with exactly these keys:
- "is_upi_payment_screenshot": true if this is a screenshot of a UPI payment result or transaction detail
- "status": "success", "pending", "failed" or "unknown"
- "amount": the amount paid in rupees as a number, or null
- "utr": the UPI transaction ID / UTR / UPI reference number, digits only, or null
- "payee_upi_id": the UPI ID the money was sent to, or null if not shown
- "payee_name": the name of who received the money, or null
- "paid_on": the payment date as YYYY-MM-DD, or null
- "paid_at": the payment time as HH:MM in 24-hour form (3:27 PM is "15:27"), or null
- "note": the payment note / message, or null
- "references": every other reference code or ID shown (not the UTR), exactly as written; [] if none
- "signs_of_editing": a list of short descriptions of visible signs that the picture was edited (digits in a
  different font or size, misaligned or overwritten text, inconsistent spacing or colours); [] if none.
  Only what the pixels show: never whether a date, amount or name seems plausible, which is checked elsewhere.
  Your own idea of the current date is out of date; today's date is given in the message."""


def reference(organization_id: str) -> str:
    """Short code put in the UPI note, so the owner can find the payment in the bank statement."""
    return "CBR" + organization_id[-6:].upper()


def upi_uri(organization_id: str) -> str:
    note = f"{settings.APP_NAME} {reference(organization_id)}"
    return (
        f"upi://pay?pa={quote(settings.UPI_ID, safe='@.')}&pn={quote(settings.UPI_PAYEE_NAME)}"
        f"&am={settings.REGISTRATION_FEE}.00&cu=INR&tn={quote(note)}"
    )


def qr_svg(text: str) -> str:
    """A QR code of the text as an SVG drawing (made here, so no outside service sees the payment details)."""
    return qrcode.make(text, image_factory=qrcode.image.svg.SvgPathImage, box_size=10, border=2).to_string(encoding="unicode")


def screenshot_hash(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def check(key: str, label: str, ok: bool | None, detail: str = "") -> dict:
    """ok: True passed, False failed (the proof is wrong), None could not be decided (a person must look)."""
    return {"key": key, "label": label, "ok": ok, "detail": detail}


def database_checks(organization_id: str, utr: str, image_hash: str) -> list[dict]:
    """Refuse a UTR or screenshot that another company has already used. No model call."""
    elsewhere = {"organization_id": {"$ne": organization_id}, "status": {"$in": ["accepted", "needs_review"]}}
    utr_used = payments.find_one({**elsewhere, "utr": utr}) is not None or payments.find_one({"accepted_utr": utr}) is not None
    shot_used = payments.find_one({"organization_id": {"$ne": organization_id}, "screenshot_hash": image_hash}) is not None
    return [
        check("utr_unused", "UTR not used before", not utr_used,
               "This UTR was already submitted for another company." if utr_used else ""),
        check("screenshot_unused", "Screenshot not used before", not shot_used,
               "This exact screenshot was already submitted for another company." if shot_used else ""),
    ]


def _parse_date(value) -> date | None:
    try:
        return date.fromisoformat(str(value)[:10])
    except (TypeError, ValueError):
        return None


def _parse_time(value) -> time | None:
    try:
        return time.fromisoformat(str(value).strip()[:5])
    except (TypeError, ValueError):
        return None


def _amount(value) -> float | None:
    try:
        return float(str(value).replace(",", "").replace("₹", "").strip())
    except (TypeError, ValueError):
        return None


def screenshot_checks(read: dict, utr: str, registered_at: datetime, organization_id: str) -> list[dict]:
    """Compare what the model read in the screenshot with what this payment must be."""
    checks = []
    receipt = read.get("is_upi_payment_screenshot") is True
    checks.append(check("receipt", "Is a UPI payment screenshot", receipt, "" if receipt else "The picture is not a UPI payment."))

    state = str(read.get("status") or "unknown").lower()
    checks.append(check(
        "status", "Payment successful", True if state == "success" else None if state == "unknown" else False,
        "" if state == "success" else f"The screenshot shows the payment as {state}.",
    ))

    amount = _amount(read.get("amount"))
    checks.append(check(
        "amount", f"Amount is Rs {settings.REGISTRATION_FEE}",
        None if amount is None else abs(amount - settings.REGISTRATION_FEE) < 0.01,
        "No amount readable." if amount is None else "" if abs(amount - settings.REGISTRATION_FEE) < 0.01 else f"The screenshot shows Rs {amount:g}.",
    ))

    seen_utr = re.sub(r"\D", "", str(read.get("utr") or ""))
    checks.append(check(
        "utr_matches", "UTR in the screenshot matches", None if not seen_utr else seen_utr == utr,
        "No UTR readable in the screenshot." if not seen_utr else "" if seen_utr == utr else f"The screenshot shows UTR {seen_utr}.",
    ))

    payee_id = str(read.get("payee_upi_id") or "").strip().lower()
    payee_name = str(read.get("payee_name") or "").strip().lower()
    expected_name = settings.UPI_PAYEE_NAME.lower()
    if payee_id:
        payee_ok, detail = payee_id == settings.UPI_ID.lower(), f"Paid to {payee_id}."
    elif payee_name and expected_name and (expected_name in payee_name or payee_name in expected_name):
        payee_ok, detail = True, ""
    else:
        payee_ok, detail = None, "The receiver cannot be confirmed from the screenshot."
    checks.append(check("payee", "Paid to the right UPI ID", payee_ok, "" if payee_ok else detail))

    paid_on = _parse_date(read.get("paid_on"))
    paid_at = _parse_time(read.get("paid_at"))
    zone = ZoneInfo(settings.LOCAL_TIMEZONE)
    registered_day = registered_at.astimezone(zone).date()
    current = datetime.now(zone)
    if paid_on is None:
        date_ok, detail = None, "No payment date readable."
    elif paid_on < registered_day:
        date_ok, detail = False, f"Paid on {paid_on}, before this company registered ({registered_day})."
    elif paid_on > current.date():
        date_ok, detail = False, f"The date {paid_on} is in the future."
    elif paid_at and datetime.combine(paid_on, paid_at, zone) > current + CLOCK_SLACK:
        date_ok, detail = False, f"The time {paid_at:%H:%M} is later than now ({current:%H:%M}): the payment cannot have happened yet."
    else:
        date_ok, detail = True, ""
    checks.append(check("date", "Paid after registering", date_ok, detail))

    # The QR code puts this company's reference in the payment note; another company's reference is a reused proof
    expected = reference(organization_id)
    shown = {code.upper() for text in [read.get("note"), *(read.get("references") or [])]
             for code in REFERENCE_PATTERN.findall(str(text or ""))}
    if shown:
        checks.append(check("reference", f"Reference is {expected}", expected in shown,
                            "" if expected in shown else f"The screenshot shows {', '.join(sorted(shown))}."))

    signs = [str(s) for s in (read.get("signs_of_editing") or []) if str(s).strip()]
    checks.append(check("not_edited", "No signs of editing", None if signs else True, " ".join(signs[:4])[:600]))
    return checks


def read_screenshot(image: bytes, mime_type: str) -> dict:
    """What the model sees in the screenshot. Raises llm.LLMError when the model cannot be used."""
    today = datetime.now(ZoneInfo(settings.LOCAL_TIMEZONE)).date().isoformat()
    text = llm.generate_with_image(f"Today is {today}. Read this payment screenshot.", SYSTEM, image, mime_type)
    try:
        read = json.loads(text)
    except json.JSONDecodeError as e:
        raise llm.LLMError("The model's answer about the screenshot was not valid JSON.") from e
    if not isinstance(read, dict):
        raise llm.LLMError("The model's answer about the screenshot was not a JSON object.")
    return read


def verdict(checks: list[dict]) -> str:
    """'rejected' if any check failed, 'doubtful' if any could not be decided, otherwise 'passed'."""
    if any(c["ok"] is False for c in checks):
        return "rejected"
    if any(c["ok"] is None for c in checks):
        return "doubtful"
    return "passed"
