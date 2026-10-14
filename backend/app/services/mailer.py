"""Outgoing mail over SMTP (a Gmail account with an app password works). Sent in the background: a mail server
that is slow or refuses never breaks the request that caused the mail.

Note: some hosts block outgoing SMTP ports (Render's support has said so for 25, 465 and 587). The failure is then
logged, and the rest of the application keeps working.
"""
import logging
import smtplib
import threading
from email.message import EmailMessage
from zoneinfo import ZoneInfo

from ..core.config import settings

log = logging.getLogger(__name__)


def configured() -> bool:
    return bool(settings.SMTP_USER and settings.SMTP_PASSWORD)


def _send_now(to: str, subject: str, text: str) -> bool:
    message = EmailMessage()
    message["From"] = f"{settings.APP_NAME} <{settings.MAIL_FROM}>"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(text)
    try:
        with smtplib.SMTP(settings.SMTP_HOST, settings.SMTP_PORT, timeout=20) as server:
            server.starttls()
            server.login(settings.SMTP_USER, settings.SMTP_PASSWORD)
            server.send_message(message)
        log.info("Mail sent to %s: %s", to, subject)
        return True
    except (OSError, smtplib.SMTPException) as e:
        log.error("Mail to %s could not be sent (%s): %s", to, type(e).__name__, e)
        return False


def send(to: str, subject: str, text: str) -> None:
    """Send one plain-text mail in the background. Does nothing, apart from a log line, when SMTP is not set up."""
    if not configured():
        log.warning("SMTP is not configured; mail to %s not sent: %s", to, subject)
        return
    threading.Thread(target=_send_now, args=(to, subject, text), daemon=True).start()


def _when(value) -> str:
    return value.astimezone(ZoneInfo(settings.LOCAL_TIMEZONE)).strftime("%d %b %Y, %I:%M %p") if value else "-"


def _tag(record: dict) -> str:
    """Test payments say so in the subject, so nobody mistakes them for money received."""
    return "[TEST] " if record.get("test_mode") else ""


def _admin_line(admin: dict | None) -> str:
    return f"Administrator: {admin['name']} <{admin['email']}>\n" if admin else ""


def _lines(*rows: tuple[str, object]) -> str:
    return "".join(f"{label}: {value}\n" for label, value in rows)


def payment_succeeded(org: dict, admin: dict | None, record: dict) -> None:
    """Registration fee paid: a receipt to the company's administrator, a notice to the platform owner."""
    facts = _lines(
        ("Company", org["name"]),
        ("Amount", f"Rs {record['amount']}"),
        ("Paid on", _when(record.get("paid_at"))),
        ("Method", record.get("method") or "-"),
        ("Razorpay payment ID", record["payment_id"]),
        ("Razorpay order ID", record["order_id"]),
    ) + ("Test mode: no real money was charged.\n" if record.get("test_mode") else "")
    if admin:
        send(
            admin["email"],
            f"{_tag(record)}Payment received: {org['name']} is registered on {settings.APP_NAME}",
            f"Hello {admin['name']},\n\n"
            f"We received your registration payment. Your company \"{org['name']}\" is now active on {settings.APP_NAME}.\n\n"
            f"{facts}\n"
            f"Sign in: {settings.APP_BASE_URL}/\n\n"
            "As the administrator you can now add your team, your assets and your manuals.\n\n"
            f"- {settings.APP_NAME}\n",
        )
    if settings.PLATFORM_OWNER_EMAIL:
        send(
            settings.PLATFORM_OWNER_EMAIL,
            f"{_tag(record)}[{settings.APP_NAME}] New company paid: {org['name']} (Rs {record['amount']})",
            f"A new company paid the registration fee and is now active.\n\n{facts}{_admin_line(admin)}\n"
            f"Payments page: {settings.APP_BASE_URL}/#/payments\n",
        )


def payment_failed(org: dict, admin: dict | None, record: dict, payment_id: str, reason: str) -> None:
    """A payment attempt that did not go through: the company may try again; the owner is told too."""
    facts = _lines(
        ("Company", org["name"]),
        ("Amount", f"Rs {record['amount']}"),
        ("Tried on", _when(record.get("failed_at"))),
        ("Method", record.get("failed_method") or "-"),
        ("Reason", reason),
        ("Razorpay payment ID", payment_id),
    ) + ("Test mode: no real money was involved.\n" if record.get("test_mode") else "")
    if admin:
        send(
            admin["email"],
            f"{_tag(record)}Payment not completed: {org['name']} on {settings.APP_NAME}",
            f"Hello {admin['name']},\n\n"
            f"Your registration payment for \"{org['name']}\" did not go through.\n\n{facts}\n"
            "Nothing was charged. If money did leave your account, your bank returns it automatically.\n"
            f"Sign in to try again: {settings.APP_BASE_URL}/\n\n"
            f"- {settings.APP_NAME}\n",
        )
    if settings.PLATFORM_OWNER_EMAIL:
        send(
            settings.PLATFORM_OWNER_EMAIL,
            f"{_tag(record)}[{settings.APP_NAME}] Payment failed: {org['name']}",
            f"A registration payment did not go through. The company is still waiting for payment.\n\n"
            f"{facts}{_admin_line(admin)}\n"
            f"Payments page: {settings.APP_BASE_URL}/#/payments\n",
        )
