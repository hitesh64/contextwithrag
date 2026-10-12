"""Banking operations: customers, accounts, transactions, loans and cards.

Every record here is self-contained demo data owned by this app (seeded or created through
these endpoints) -- there is no connection to any real bank, payment network or core banking
system, and no real money ever moves. Any authenticated staff member can look up records and
record day-to-day transactions; only an administrator can approve/reject loans or change a
card's status, the same admin/staff split already used elsewhere (see security.require_admin).
"""
import random
import string
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone

from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import OperationFailure

from .config import settings
from .database import accounts, cards, client, customers, loans, transactions
from .schemas import (
    AccountIn, AccountOut, CardIn, CardOut, CardPatch, CustomerIn, CustomerOut, LoanIn, LoanOut, LoanPatch,
    TransactionIn, TransactionOut, account_out, card_out, customer_out, loan_out, transaction_out,
)
from .security import get_current_user, require_admin

router = APIRouter(prefix="/api/banking", tags=["banking"])

LIST_PAGE = 200


def _oid(id_: str, not_found: str) -> ObjectId:
    if not ObjectId.is_valid(id_):
        raise HTTPException(status.HTTP_404_NOT_FOUND, not_found)
    return ObjectId(id_)


def next_customer_code() -> str:
    last = customers.find_one(sort=[("customer_code", -1)])
    n = int(last["customer_code"][4:]) + 1 if last else 1
    return f"CUST{n:05d}"


def new_account_number() -> str:
    while True:
        number = "".join(random.choices(string.digits, k=12))
        if not accounts.find_one({"account_number": number}):
            return number


def new_card_number() -> str:
    while True:
        number = "".join(random.choices(string.digits, k=16))
        if not cards.find_one({"card_number": number}):
            return number


def emi(principal: float, annual_rate: float, months: int) -> float:
    r = annual_rate / 12 / 100
    if r == 0:
        return round(principal / months, 2)
    return round(principal * r * (1 + r) ** months / ((1 + r) ** months - 1), 2)


# ---- Customers ----

@router.get("/customers")
def list_customers(q: str = "", _: dict = Depends(get_current_user)):
    query = {}
    if q:
        query = {"$or": [
            {"full_name": {"$regex": q, "$options": "i"}},
            {"customer_code": {"$regex": q, "$options": "i"}},
            {"email": {"$regex": q, "$options": "i"}},
            {"phone": {"$regex": q, "$options": "i"}},
        ]}
    return [customer_out(c) for c in customers.find(query).sort("created_at", -1).limit(LIST_PAGE)]


@router.post("/customers", status_code=status.HTTP_201_CREATED)
def create_customer(body: CustomerIn, _: dict = Depends(get_current_user)):
    if customers.find_one({"email": body.email}):
        raise HTTPException(status.HTTP_409_CONFLICT, "A customer with this email already exists.")
    doc = {
        **body.model_dump(),
        "customer_code": next_customer_code(),
        "kyc_status": "pending",
        "created_at": datetime.now(timezone.utc),
    }
    doc["_id"] = customers.insert_one(doc).inserted_id
    return customer_out(doc)


@router.get("/customers/{customer_id}")
def get_customer(customer_id: str, _: dict = Depends(get_current_user)):
    oid = _oid(customer_id, "Customer not found")
    customer = customers.find_one({"_id": oid})
    if customer is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    with ThreadPoolExecutor(max_workers=2) as pool:
        f_accounts = pool.submit(lambda: list(accounts.find({"customer_id": oid})))
        f_loans = pool.submit(lambda: list(loans.find({"customer_id": oid})))
        return {
            "customer": customer_out(customer),
            "accounts": [account_out(a) for a in f_accounts.result()],
            "loans": [loan_out(l) for l in f_loans.result()],
        }


# ---- Accounts ----

@router.get("/accounts")
def list_accounts(customer_id: str = "", _: dict = Depends(get_current_user)):
    query = {}
    if customer_id:
        query["customer_id"] = _oid(customer_id, "Customer not found")
    return [account_out(a) for a in accounts.find(query).sort("created_at", -1).limit(LIST_PAGE)]


@router.post("/accounts", status_code=status.HTTP_201_CREATED)
def create_account(body: AccountIn, _: dict = Depends(get_current_user)):
    customer_oid = _oid(body.customer_id, "Customer not found")
    if not customers.find_one({"_id": customer_oid}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    doc = {
        "account_number": new_account_number(),
        "customer_id": customer_oid,
        "account_type": body.account_type,
        "balance": body.opening_balance,
        "currency": settings.CURRENCY,
        "status": "active",
        "branch_code": body.branch_code,
        "created_at": datetime.now(timezone.utc),
    }
    doc["_id"] = accounts.insert_one(doc).inserted_id
    return account_out(doc)


@router.get("/accounts/{account_id}/transactions")
def account_transactions(account_id: str, _: dict = Depends(get_current_user)):
    oid = _oid(account_id, "Account not found")
    if not accounts.find_one({"_id": oid}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    # Each leg of a transfer is written as its own document with account_id = that leg's own
    # account (see create_transaction), so filtering on account_id alone is correct and avoids
    # double-counting the same transfer when to_account_id also happens to equal this account.
    cursor = transactions.find({"account_id": oid}).sort("created_at", -1).limit(LIST_PAGE)
    return [transaction_out(t) for t in cursor]


# ---- Transactions ----

@router.post("/transactions", status_code=status.HTTP_201_CREATED)
def create_transaction(body: TransactionIn, user: dict = Depends(get_current_user)):
    account_oid = _oid(body.account_id, "Account not found")
    account = accounts.find_one({"_id": account_oid})
    if account is None or account["status"] != "active":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found or closed")

    now = datetime.now(timezone.utc)

    if body.type == "deposit":
        account = accounts.find_one_and_update(
            {"_id": account_oid}, {"$inc": {"balance": body.amount}}, return_document=True,
        )
        doc = {
            "account_id": account_oid, "type": "deposit", "direction": "credit", "amount": body.amount,
            "to_account_id": None, "balance_after": account["balance"], "description": body.description,
            "created_at": now, "created_by": user["username"],
        }
        doc["_id"] = transactions.insert_one(doc).inserted_id
        return transaction_out(doc)

    if body.type == "withdrawal":
        if account["balance"] < body.amount:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient balance")
        account = accounts.find_one_and_update(
            {"_id": account_oid, "balance": {"$gte": body.amount}},
            {"$inc": {"balance": -body.amount}}, return_document=True,
        )
        if account is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient balance")
        doc = {
            "account_id": account_oid, "type": "withdrawal", "direction": "debit", "amount": body.amount,
            "to_account_id": None, "balance_after": account["balance"], "description": body.description,
            "created_at": now, "created_by": user["username"],
        }
        doc["_id"] = transactions.insert_one(doc).inserted_id
        return transaction_out(doc)

    # transfer
    to_oid = _oid(body.to_account_id, "Destination account not found")
    if to_oid == account_oid:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Cannot transfer to the same account")
    to_account = accounts.find_one({"_id": to_oid})
    if to_account is None or to_account["status"] != "active":
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Destination account not found or closed")
    if account["balance"] < body.amount:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient balance")

    def _do_transfer(session=None):
        src = accounts.find_one_and_update(
            {"_id": account_oid, "balance": {"$gte": body.amount}},
            {"$inc": {"balance": -body.amount}}, return_document=True, session=session,
        )
        if src is None:
            raise HTTPException(status.HTTP_400_BAD_REQUEST, "Insufficient balance")
        dst = accounts.find_one_and_update(
            {"_id": to_oid}, {"$inc": {"balance": body.amount}}, return_document=True, session=session,
        )
        out_doc = {
            "account_id": account_oid, "type": "transfer", "direction": "debit", "amount": body.amount,
            "to_account_id": to_oid, "balance_after": src["balance"], "description": body.description,
            "created_at": now, "created_by": user["username"],
        }
        in_doc = {
            "account_id": to_oid, "type": "transfer", "direction": "credit", "amount": body.amount,
            "to_account_id": account_oid, "balance_after": dst["balance"], "description": body.description,
            "created_at": now, "created_by": user["username"],
        }
        out_doc["_id"] = transactions.insert_one(out_doc, session=session).inserted_id
        transactions.insert_one(in_doc, session=session)
        return out_doc

    try:
        with client.start_session() as session:
            with session.start_transaction():
                result = _do_transfer(session)
    except OperationFailure:
        # Standalone MongoDB (no replica set) cannot run multi-document transactions; fall back
        # to sequential updates -- still correct for this single-process demo app.
        result = _do_transfer()
    return transaction_out(result)


# ---- Loans ----

@router.get("/loans")
def list_loans(customer_id: str = "", _: dict = Depends(get_current_user)):
    query = {}
    if customer_id:
        query["customer_id"] = _oid(customer_id, "Customer not found")
    return [loan_out(l) for l in loans.find(query).sort("created_at", -1).limit(LIST_PAGE)]


@router.post("/loans", status_code=status.HTTP_201_CREATED)
def create_loan(body: LoanIn, _: dict = Depends(get_current_user)):
    customer_oid = _oid(body.customer_id, "Customer not found")
    if not customers.find_one({"_id": customer_oid}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Customer not found")
    doc = {
        "customer_id": customer_oid, "loan_type": body.loan_type, "principal": body.principal,
        "interest_rate": body.interest_rate, "tenure_months": body.tenure_months,
        "emi": emi(body.principal, body.interest_rate, body.tenure_months),
        "status": "pending", "created_at": datetime.now(timezone.utc),
    }
    doc["_id"] = loans.insert_one(doc).inserted_id
    return loan_out(doc)


@router.patch("/loans/{loan_id}")
def update_loan(loan_id: str, body: LoanPatch, _: dict = Depends(require_admin)):
    oid = _oid(loan_id, "Loan not found")
    loan = loans.find_one_and_update({"_id": oid}, {"$set": {"status": body.status}}, return_document=True)
    if loan is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Loan not found")
    return loan_out(loan)


# ---- Cards ----

@router.get("/cards")
def list_cards(account_id: str = "", _: dict = Depends(get_current_user)):
    query = {}
    if account_id:
        query["account_id"] = _oid(account_id, "Account not found")
    return [card_out(c) for c in cards.find(query).sort("created_at", -1).limit(LIST_PAGE)]


@router.post("/cards", status_code=status.HTTP_201_CREATED)
def create_card(body: CardIn, _: dict = Depends(get_current_user)):
    account_oid = _oid(body.account_id, "Account not found")
    if not accounts.find_one({"_id": account_oid}):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Account not found")
    now = datetime.now(timezone.utc)
    expiry = f"{now.month:02d}/{(now.year + 4) % 100:02d}"
    doc = {
        "account_id": account_oid, "card_type": body.card_type, "card_number": new_card_number(),
        "expiry": expiry, "status": "active", "created_at": now,
    }
    doc["_id"] = cards.insert_one(doc).inserted_id
    return card_out(doc)


@router.patch("/cards/{card_id}")
def update_card(card_id: str, body: CardPatch, _: dict = Depends(require_admin)):
    oid = _oid(card_id, "Card not found")
    card = cards.find_one_and_update({"_id": oid}, {"$set": {"status": body.status}}, return_document=True)
    if card is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Card not found")
    return card_out(card)


# ---- Dashboard stats ----

@router.get("/stats")
def stats(_: dict = Depends(get_current_user)):
    month_start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0)

    # Each of these is a separate round trip to MongoDB; firing them concurrently instead of
    # one after another turns ~5 round trips of latency into ~1 on a remote (Atlas) cluster.
    with ThreadPoolExecutor(max_workers=5) as pool:
        f_customers = pool.submit(customers.count_documents, {})
        f_accounts = pool.submit(lambda: list(accounts.aggregate([
            {"$facet": {
                "count": [{"$count": "n"}],
                "total": [{"$group": {"_id": None, "total": {"$sum": "$balance"}}}],
            }},
        ]))[0])
        f_loans = pool.submit(lambda: list(loans.aggregate([{"$group": {"_id": "$status", "count": {"$sum": 1}}}])))
        f_transactions = pool.submit(transactions.count_documents, {"created_at": {"$gte": month_start}})
        f_cards = pool.submit(cards.count_documents, {})
        accounts_facet = f_accounts.result()
        by_status = f_loans.result()
        results = {
            "customers": f_customers.result(),
            "accounts": accounts_facet["count"][0]["n"] if accounts_facet["count"] else 0,
            "total_balance": accounts_facet["total"][0]["total"] if accounts_facet["total"] else 0,
            "transactions_this_month": f_transactions.result(),
            "loans_by_status": {row["_id"]: row["count"] for row in by_status},
            "cards": f_cards.result(),
        }
    return results
