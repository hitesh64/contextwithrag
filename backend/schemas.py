import re
from datetime import datetime

from pydantic import BaseModel, EmailStr, Field, field_validator


class RegisterIn(BaseModel):
    username: str = Field(pattern=r"^[A-Za-z0-9_]{3,30}$")
    email: EmailStr
    password: str = Field(min_length=8)

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


class TokenOut(BaseModel):
    access_token: str
    token_type: str = "bearer"
    user: UserOut


class ChatIn(BaseModel):
    message: str = Field(min_length=1, max_length=4000)
    session_id: str | None = None

    @field_validator("message")
    @classmethod
    def not_blank(cls, v: str) -> str:
        v = v.strip()
        if not v:
            raise ValueError("Message cannot be empty")
        return v


class ChatOut(BaseModel):
    session_id: str
    answer: str
    sources: list[str]


def user_out(user: dict) -> UserOut:
    return UserOut(
        id=str(user["_id"]),
        username=user["username"],
        email=user["email"],
        is_active=user.get("is_active", True),
        created_at=user["created_at"],
    )
