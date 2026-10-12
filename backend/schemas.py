import re
from datetime import datetime
from typing import Literal

from pydantic import BaseModel, EmailStr, Field, field_validator

from .config import settings


def _known_department(v: str | None) -> str | None:
    if v is not None and v not in settings.DEPARTMENTS:
        raise ValueError("Unknown department")
    return v


class RegisterIn(BaseModel):
    username: str = Field(pattern=r"^[A-Za-z0-9_]{3,30}$")
    email: EmailStr
    password: str = Field(min_length=8)
    department: str

    _department = field_validator("department")(_known_department)

    @field_validator("password")
    @classmethod
    def strong_password(cls, v: str) -> str:
        if len(v.encode()) > 72:
            raise ValueError("Password is too long (max 72 bytes)")
        missing = [
            name for name, pattern in (
                ("an uppercase letter", r"[A-Z]"),
                ("a lowercase letter", r"[a-z]"),
                ("a digit", r"\d"),
                ("a symbol", r"[^A-Za-z0-9\s]"),
            ) if not re.search(pattern, v)
        ]
        if missing:
            raise ValueError("Password must contain " + ", ".join(missing))
        return v


class LoginIn(BaseModel):
    username: str = Field(min_length=1, max_length=30)
    password: str = Field(min_length=1, max_length=200)


class UserOut(BaseModel):
    id: str
    username: str
    email: str
    is_active: bool
    created_at: datetime
    role: Literal["admin", "staff"]
    department: str


class UserPatch(BaseModel):
    role: Literal["admin", "staff"] | None = None
    department: str | None = None

    _department = field_validator("department")(_known_department)


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None
    # A photo of the problem, base64 encoded (the page shrinks it before sending)
    image: str | None = Field(default=None, max_length=6_000_000)
    image_type: Literal["image/jpeg", "image/png", "image/webp"] = "image/jpeg"

    @field_validator("message")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v


class Citation(BaseModel):
    """A passage the answer refers to as [number]."""
    number: int
    source: str
    page: int | None = None
    text: str
    category: str | None = None
    effective_date: str | None = None


class ChatOut(BaseModel):
    session_id: str
    answer: str
    # File names of the cited passages (also what chats saved before citations existed carry)
    sources: list[str]
    citations: list[Citation] = []
    # What was read from the attached photo, shown so the user can check it
    photo_reading: str | None = None


def user_out(user: dict) -> UserOut:
    return UserOut(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        is_active=user.get("is_active", True),
        created_at=user["created_at"],
        role=user["role"],
        department=user["department"],
    )


# ---- Banking operations module (self-contained demo records) ----

def _known_branch(v: str) -> str:
    if v not in {b["code"] for b in settings.BRANCHES}:
        raise ValueError("Unknown branch code")
    return v


class CustomerIn(BaseModel):
    full_name: str = Field(min_length=2, max_length=100)
    email: EmailStr
    phone: str = Field(pattern=r"^[0-9]{10}$")
    address: str = Field(min_length=5, max_length=300)
    branch_code: str

    _branch = field_validator("branch_code")(_known_branch)


class CustomerOut(BaseModel):
    id: str
    customer_code: str
    full_name: str
    email: str
    phone: str
    address: str
    branch_code: str
    kyc_status: Literal["pending", "verified"]
    created_at: datetime


class AccountIn(BaseModel):
    customer_id: str
    account_type: str
    branch_code: str
    opening_balance: float = Field(default=0, ge=0)

    _branch = field_validator("branch_code")(_known_branch)

    @field_validator("account_type")
    @classmethod
    def _known_account_type(cls, v: str) -> str:
        if v not in settings.ACCOUNT_TYPES:
            raise ValueError("Unknown account type")
        return v


class AccountOut(BaseModel):
    id: str
    account_number: str
    customer_id: str
    account_type: str
    balance: float
    currency: str
    status: Literal["active", "closed"]
    branch_code: str
    created_at: datetime


class TransactionIn(BaseModel):
    account_id: str
    type: Literal["deposit", "withdrawal", "transfer"]
    amount: float = Field(gt=0)
    to_account_id: str | None = None
    description: str | None = Field(default=None, max_length=200)

    @field_validator("to_account_id")
    @classmethod
    def _transfer_needs_target(cls, v, info):
        if info.data.get("type") == "transfer" and not v:
            raise ValueError("to_account_id is required for a transfer")
        return v


class TransactionOut(BaseModel):
    id: str
    account_id: str
    type: Literal["deposit", "withdrawal", "transfer"]
    direction: Literal["debit", "credit"]
    amount: float
    to_account_id: str | None = None
    balance_after: float
    description: str | None = None
    created_at: datetime
    created_by: str


class LoanIn(BaseModel):
    customer_id: str
    loan_type: str
    principal: float = Field(gt=0)
    interest_rate: float = Field(gt=0, le=36)
    tenure_months: int = Field(gt=0, le=360)

    @field_validator("loan_type")
    @classmethod
    def _known_loan_type(cls, v: str) -> str:
        if v not in settings.LOAN_TYPES:
            raise ValueError("Unknown loan type")
        return v


class LoanPatch(BaseModel):
    status: Literal["pending", "approved", "rejected", "closed"]


class LoanOut(BaseModel):
    id: str
    customer_id: str
    loan_type: str
    principal: float
    interest_rate: float
    tenure_months: int
    emi: float
    status: Literal["pending", "approved", "rejected", "closed"]
    created_at: datetime


class CardIn(BaseModel):
    account_id: str
    card_type: str

    @field_validator("card_type")
    @classmethod
    def _known_card_type(cls, v: str) -> str:
        if v not in settings.CARD_TYPES:
            raise ValueError("Unknown card type")
        return v


class CardPatch(BaseModel):
    status: Literal["active", "frozen", "blocked"]


class CardOut(BaseModel):
    id: str
    account_id: str
    card_type: str
    card_number: str
    expiry: str
    status: Literal["active", "frozen", "blocked"]
    created_at: datetime


def customer_out(c: dict) -> CustomerOut:
    return CustomerOut(
        id=str(c["_id"]), customer_code=c["customer_code"], full_name=c["full_name"], email=c["email"],
        phone=c["phone"], address=c["address"], branch_code=c["branch_code"], kyc_status=c["kyc_status"],
        created_at=c["created_at"],
    )


def account_out(a: dict) -> AccountOut:
    return AccountOut(
        id=str(a["_id"]), account_number=a["account_number"], customer_id=str(a["customer_id"]),
        account_type=a["account_type"], balance=a["balance"], currency=a["currency"], status=a["status"],
        branch_code=a["branch_code"], created_at=a["created_at"],
    )


def transaction_out(t: dict) -> TransactionOut:
    return TransactionOut(
        id=str(t["_id"]), account_id=str(t["account_id"]), type=t["type"], direction=t["direction"],
        amount=t["amount"], to_account_id=str(t["to_account_id"]) if t.get("to_account_id") else None,
        balance_after=t["balance_after"], description=t.get("description"), created_at=t["created_at"],
        created_by=t["created_by"],
    )


def loan_out(l: dict) -> LoanOut:
    return LoanOut(
        id=str(l["_id"]), customer_id=str(l["customer_id"]), loan_type=l["loan_type"], principal=l["principal"],
        interest_rate=l["interest_rate"], tenure_months=l["tenure_months"], emi=l["emi"], status=l["status"],
        created_at=l["created_at"],
    )


def card_out(c: dict) -> CardOut:
    return CardOut(
        id=str(c["_id"]), account_id=str(c["account_id"]), card_type=c["card_type"],
        card_number="**** **** **** " + c["card_number"][-4:], expiry=c["expiry"], status=c["status"],
        created_at=c["created_at"],
    )
