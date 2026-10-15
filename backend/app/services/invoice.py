"""The bill of a paid registration fee: a running bill number and a one-page PDF.

The number and the "billed to" details are fixed once, when the payment is first counted (or, for a payment made
before bills existed, when its bill is first asked for), so a bill downloaded later says the same as the mailed one.
"""
from html import escape
from zoneinfo import ZoneInfo

import pymupdf

from ..core.config import settings
from ..core.database import next_number, organizations, payments, users
from ..core.utils import oid

_ONES = ["", "One", "Two", "Three", "Four", "Five", "Six", "Seven", "Eight", "Nine", "Ten", "Eleven", "Twelve",
         "Thirteen", "Fourteen", "Fifteen", "Sixteen", "Seventeen", "Eighteen", "Nineteen"]
_TENS = ["", "", "Twenty", "Thirty", "Forty", "Fifty", "Sixty", "Seventy", "Eighty", "Ninety"]


def _below_hundred(n: int) -> str:
    return _ONES[n] if n < 20 else " ".join(w for w in (_TENS[n // 10], _ONES[n % 10]) if w)


def _below_thousand(n: int) -> str:
    hundreds, rest = divmod(n, 100)
    return " ".join(w for w in ((f"{_ONES[hundreds]} Hundred" if hundreds else ""), _below_hundred(rest)) if w)


def rupees_in_words(amount: int) -> str:
    """Whole rupees in words, the Indian way: 250000 -> 'Rupees Two Lakh Fifty Thousand Only'."""
    if amount == 0:
        return "Rupees Zero Only"
    parts = []
    for size, name in ((10_000_000, "Crore"), (100_000, "Lakh"), (1_000, "Thousand")):
        count, amount = divmod(amount, size)
        if count:
            parts.append(f"{_below_thousand(count) if count < 1000 else rupees_in_words(count)[7:-5]} {name}")
    if amount:
        parts.append(_below_thousand(amount))
    return f"Rupees {' '.join(parts)} Only"


def indian_money(amount: int) -> str:
    """2999 -> '2,999.00'; 250000 -> '2,50,000.00' (Indian digit grouping)."""
    digits = str(amount)
    head, tail = digits[:-3], digits[-3:]
    groups = []
    while len(head) > 2:
        groups.insert(0, head[-2:])
        head = head[:-2]
    return ",".join(([head] if head else []) + groups + [tail]) + ".00"


# Razorpay's method codes as people write them
_METHODS = {"upi": "UPI", "card": "Card", "netbanking": "Net banking", "wallet": "Wallet", "emi": "EMI",
            "paylater": "Pay later"}


def _local(value):
    return value.astimezone(ZoneInfo(settings.LOCAL_TIMEZONE))


def numbered(record: dict) -> dict:
    """The paid payment record with its bill number and billed-to details, giving it both the first time."""
    if record.get("status") != "paid" or record.get("invoice_number"):
        return record
    org = organizations.find_one({"_id": oid(record["organization_id"])}, {"name": 1}) or {}
    admin = users.find_one({"organization_id": record["organization_id"], "role": "admin"},
                           {"name": 1, "email": 1}, sort=[("created_at", 1)]) or {}
    number = f"{settings.INVOICE_PREFIX}-{_local(record['paid_at']).year}-{next_number('platform', 'invoice'):05d}"
    payments.update_one(
        {"_id": record["_id"], "invoice_number": {"$exists": False}},
        {"$set": {"invoice_number": number, "billed_to": {
            "company": org.get("name") or record.get("organization_name", ""),
            "name": admin.get("name", ""),
            "email": admin.get("email") or record.get("created_by_email", ""),
        }}},
    )
    return payments.find_one({"_id": record["_id"]})


def filename(record: dict) -> str:
    return f"Bill-{record['invoice_number']}.pdf"


_CSS = """
* { font-family: sans-serif; }
body { font-size: 10pt; color: #1a2233; }
.top { width: 100%; border-collapse: collapse; }
.top td { vertical-align: top; padding: 0; }
.brand { font-size: 20pt; font-weight: bold; color: #be123c; }
.title { font-size: 16pt; font-weight: bold; text-align: right; color: #0f172a; }
.muted { color: #5b6472; }
.right { text-align: right; }
.paid { color: #16a34a; font-weight: bold; }
.test { background-color: #fef3c7; color: #92400e; padding: 6px; font-weight: bold; text-align: center; }
h3 { font-size: 9pt; color: #5b6472; margin: 18px 0 4px 0; text-transform: uppercase; }
.items { width: 100%; border-collapse: collapse; margin-top: 16px; }
.items th { background-color: #f1f5f9; text-align: left; padding: 7px; font-size: 9pt; border-bottom: 1px solid #cbd5e1; }
.items td { padding: 8px 7px; border-bottom: 1px solid #e2e8f0; }
.items .total td { font-weight: bold; font-size: 11pt; border-bottom: 2px solid #0f172a; }
.facts { width: 100%; border-collapse: collapse; }
.facts td { padding: 3px 0; }
.facts td.label { width: 32%; color: #5b6472; }
.foot { margin-top: 30px; font-size: 8.5pt; color: #8b93a1; text-align: center; }
"""


def _body(record: dict) -> str:
    """The content of the bill of a numbered, paid payment record, shared by the PDF and the printable page."""
    e = lambda value: escape(str(value or ""))  # noqa: E731
    bill_to = record.get("billed_to", {})
    paid_at = _local(record["paid_at"])
    # The brand is printed above already; a different legal name of the seller goes under it
    seller = [] if settings.INVOICE_SELLER_NAME == settings.APP_NAME else [f"<b>{e(settings.INVOICE_SELLER_NAME)}</b>"]
    # A line break in the address may be written as \n in .env
    seller += [e(line) for line in settings.INVOICE_SELLER_ADDRESS.replace("\\n", "\n").splitlines() if line.strip()]
    if settings.INVOICE_SELLER_GSTIN:
        seller.append(f"GSTIN: {e(settings.INVOICE_SELLER_GSTIN)}")
    if settings.PLATFORM_OWNER_EMAIL:
        seller.append(e(settings.PLATFORM_OWNER_EMAIL))
    amount = indian_money(record["amount"])
    test = ('<p class="test">TEST PAYMENT: made with Razorpay test keys. No real money was charged.</p>'
            if record.get("test_mode") else "")
    return f"""
    <table class="top"><tr>
      <td><div class="brand">{e(settings.APP_NAME)}</div><div class="muted">{'<br>'.join(seller)}</div></td>
      <td class="right"><div class="title">BILL</div>
        <div>Bill no: <b>{e(record['invoice_number'])}</b></div>
        <div>Date: {paid_at:%d %b %Y}</div>
        <div class="paid">PAID</div></td>
    </tr></table>
    {test}
    <h3>Billed to</h3>
    <div><b>{e(bill_to.get('company'))}</b></div>
    <div>{e(bill_to.get('name'))}</div>
    <div class="muted">{e(bill_to.get('email'))}</div>
    <table class="items">
      <tr><th>#</th><th>Description</th><th class="right">Amount (Rs)</th></tr>
      <tr><td>1</td><td>One-time registration fee: {e(settings.APP_NAME)} workspace for {e(bill_to.get('company'))}</td>
        <td class="right">{amount}</td></tr>
      <tr class="total"><td></td><td class="right">Total paid</td><td class="right">Rs {amount}</td></tr>
    </table>
    <p class="muted">{e(rupees_in_words(record['amount']))}</p>
    <h3>Payment</h3>
    <table class="facts">
      <tr><td class="label">Paid on</td><td>{paid_at:%d %b %Y, %I:%M %p}</td></tr>
      <tr><td class="label">Method</td><td>{e(_METHODS.get(record.get('method'), record.get('method') or '-'))} (Razorpay)</td></tr>
      <tr><td class="label">Razorpay payment ID</td><td>{e(record.get('payment_id'))}</td></tr>
      <tr><td class="label">Razorpay order ID</td><td>{e(record.get('order_id'))}</td></tr>
    </table>
    <p class="foot">This is a computer-generated bill and needs no signature.</p>
    """


def pdf(record: dict) -> bytes:
    """The one-page A4 PDF bill: attached to the mails and downloaded."""
    doc = pymupdf.open()
    page = doc.new_page(width=595, height=842)  # A4
    page.insert_htmlbox(pymupdf.Rect(42, 42, 553, 800), _body(record), css=_CSS)
    doc.set_metadata({"title": f"Bill {record['invoice_number']}", "author": settings.INVOICE_SELLER_NAME,
                      "creator": settings.APP_NAME})
    data = doc.tobytes(garbage=3, deflate=True)
    doc.close()
    return data


# On screen the bill sits on a sheet like the PDF; printed, it fills an A4 page with the browser's own margins
_PAGE_CSS = """
html { background: #eef1f5; }
body { max-width: 680px; margin: 24px auto; padding: 44px 48px; background: #fff; box-shadow: 0 2px 14px rgba(15, 23, 42, .12); }
@media screen and (max-width: 600px) { body { margin: 0; padding: 18px 14px; box-shadow: none; } .brand { font-size: 15pt; } }
@page { size: A4; margin: 16mm; }
@media print {
  html { background: #fff; }
  body { margin: 0; padding: 0; max-width: none; box-shadow: none; }
  .test, .items th { -webkit-print-color-adjust: exact; print-color-adjust: exact; }
}
"""


def html_page(record: dict) -> str:
    """The same bill as a web page, to look at and print from the browser. Contains no scripts."""
    return (f'<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><title>Bill {escape(record["invoice_number"])}'
            f'</title><style>{_CSS}{_PAGE_CSS}</style></head><body>{_body(record)}</body></html>')
