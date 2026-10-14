"""Outgoing mail over SMTP (a Gmail account with an app password works). Sent in the background: a mail server
that is slow or refuses never breaks the request that caused the mail.

Note: some hosts block outgoing SMTP ports (Render's support has said so for 25, 465 and 587). The failure is then
logged, and the rest of the application keeps working.
"""
import html
import logging
import smtplib
import threading
from email.message import EmailMessage

from ..core.config import settings

log = logging.getLogger(__name__)

RESULT = {True: "OK", False: "FAILED", None: "UNSURE"}


def configured() -> bool:
    return bool(settings.SMTP_USER and settings.SMTP_PASSWORD)


def _send_now(to: str, subject: str, text: str, html_body: str | None = None, attachment: tuple | None = None) -> bool:
    message = EmailMessage()
    message["From"] = f"{settings.APP_NAME} <{settings.MAIL_FROM}>"
    message["To"] = to
    message["Subject"] = subject
    message.set_content(text)
    if html_body:
        message.add_alternative(html_body, subtype="html")
    if attachment:
        data, media_type, filename = attachment
        maintype, subtype = media_type.split("/")
        message.add_attachment(data, maintype=maintype, subtype=subtype, filename=filename)
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


def send(to: str, subject: str, text: str, html_body: str | None = None, attachment: tuple | None = None) -> None:
    """Send one mail in the background: plain text, optionally an HTML version and one attachment
    (bytes, media type, file name). Does nothing, apart from a log line, when SMTP is not set up."""
    if not configured():
        log.warning("SMTP is not configured; mail to %s not sent: %s", to, subject)
        return
    threading.Thread(target=_send_now, args=(to, subject, text, html_body, attachment), daemon=True).start()


def company_registered(org: dict, admin: dict, payment: dict) -> None:
    send(
        admin["email"],
        f"Your company {org['name']} is registered on {settings.APP_NAME}",
        f"Hello {admin['name']},\n\n"
        f"Your company \"{org['name']}\" is now registered on the {settings.APP_NAME} system.\n\n"
        f"Registration fee: Rs {payment['amount']}\n"
        f"UPI transaction (UTR): {payment['utr']}\n"
        f"Administrator account: {admin['email']}\n\n"
        f"Sign in: {settings.APP_BASE_URL}/\n\n"
        "As the administrator you can now add your team, your assets and your manuals.\n\n"
        f"- {settings.APP_NAME}\n",
    )


def _button(href: str, text: str, colour: str) -> str:
    return (f'<a href="{html.escape(href)}" style="display:inline-block;padding:12px 26px;margin:0 8px 8px 0;'
            f'background:{colour};color:#ffffff;text-decoration:none;font-weight:bold;border-radius:8px">{text}</a>')


def payment_for_owner(org: dict, payment: dict, review_link: str, screenshot: bytes, media_type: str) -> None:
    """Ask the platform owner to confirm a payment: Accept / Reject buttons, and the screenshot attached."""
    if not settings.PLATFORM_OWNER_EMAIL:
        return
    reasons = "\n".join(f"  - {c['label']}: {RESULT[c['ok']]} {c['detail']}" for c in payment["checks"])
    rows = "".join(
        f"<li>{RESULT[c['ok']]}: {html.escape(c['label'])}"
        + (f" <span style='color:#6b7280'>({html.escape(c['detail'])})</span>" if c["detail"] else "") + "</li>"
        for c in payment["checks"]
    )
    verdict = "All checks passed." if payment.get("checks_passed") else "The check found problems: look carefully."
    company, utr = html.escape(org["name"]), html.escape(payment["utr"])
    accept, reject = review_link + "&action=accept", review_link + "&action=reject"
    send(
        settings.PLATFORM_OWNER_EMAIL,
        f"[{settings.APP_NAME}] Payment to confirm: {org['name']} (UTR {payment['utr']})"
        + ("" if payment.get("checks_passed") else " - check found problems"),
        f"Company: {org['name']}\nAmount: Rs {payment['amount']}\nUTR: {payment['utr']}\n{verdict}\n\nChecks:\n{reasons}\n\n"
        "Find this UTR and amount in your bank or UPI app first. Then:\n"
        f"Accept: {accept}\nReject: {reject}\n"
        "(Each link opens a page where you confirm. It works for 7 days, once.)\n",
        f"""<div style="font-family:Arial,sans-serif;font-size:15px;color:#111827;max-width:560px">
<h2 style="margin:0 0 12px">Payment to confirm</h2>
<p><b>{company}</b> paid the registration fee.<br>Amount: <b>Rs {payment['amount']}</b><br>UTR: <b>{utr}</b></p>
<p><b>{verdict}</b></p><ul>{rows}</ul>
<p style="background:#fef3c7;padding:10px 12px;border-radius:8px">Find this UTR and amount in your bank or UPI app
before you accept. The AI check reads only the screenshot (attached); it cannot see your bank account.</p>
<p>{_button(accept, "Accept payment", "#16a34a")}{_button(reject, "Reject", "#dc2626")}</p>
<p style="color:#6b7280;font-size:13px">Each button opens a page where you confirm with one more click.
The link works for 7 days, once.</p>
</div>""",
        (screenshot, media_type, f"payment-{payment['utr']}.{media_type.split('/')[1]}"),
    )


def payment_rejected(to: str, org_name: str, utr: str, note: str) -> None:
    send(
        to,
        f"{settings.APP_NAME}: registration payment of {org_name} not accepted",
        f"The registration payment with UTR {utr} for \"{org_name}\" was not accepted.\n"
        + (f"Reason: {note}\n" if note else "")
        + f"\nSign in to send a new proof of payment: {settings.APP_BASE_URL}/\n\n- {settings.APP_NAME}\n",
    )
