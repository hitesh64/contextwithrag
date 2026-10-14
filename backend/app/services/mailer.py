"""Outgoing mail over SMTP (a Gmail account with an app password works). Sent in the background: a mail server
that is slow or refuses never breaks the request that caused the mail.

Note: some hosts block outgoing SMTP ports (Render's support has said so for 25, 465 and 587). The failure is then
logged, and the rest of the application keeps working.
"""
import logging
import smtplib
import threading
from email.message import EmailMessage

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


def company_registered(org: dict, admin: dict, payment: dict) -> None:
    send(
        admin["email"],
        f"Your company {org['name']} is registered on {settings.APP_NAME}",
        f"Hello {admin['name']},\n\n"
        f"Your company \"{org['name']}\" is now registered on the {settings.APP_NAME} system.\n\n"
        f"Registration fee: Rs {payment['amount']}\n"
        f"Razorpay payment: {payment['payment_id']}\n"
        f"Administrator account: {admin['email']}\n\n"
        f"Sign in: {settings.APP_BASE_URL}/\n\n"
        "As the administrator you can now add your team, your assets and your manuals.\n\n"
        f"- {settings.APP_NAME}\n",
    )
