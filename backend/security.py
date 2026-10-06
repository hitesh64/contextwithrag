"""Authentication (bcrypt + server-side login sessions).

No JWT: on login the server creates a random token, stores only its SHA-256 hash in
MongoDB with an expiry, and FastAPI's HTTPBearer reads it back on every request.
Logging out invalidates the token immediately.
"""
import hashlib
import secrets
from datetime import datetime, timedelta, timezone

import bcrypt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings
from .database import login_sessions, users

bearer = HTTPBearer(auto_error=False)


def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()


def verify_password(password: str, hashed: str) -> bool:
    try:
        return bcrypt.checkpw(password.encode(), hashed.encode())
    except ValueError:
        return False


def _token_hash(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def create_access_token(user_id: str) -> str:
    token = secrets.token_urlsafe(32)
    now = datetime.now(timezone.utc)
    login_sessions.insert_one({
        "token_hash": _token_hash(token),
        "user_id": user_id,
        "created_at": now,
        "expires_at": now + timedelta(minutes=settings.LOGIN_EXPIRE_MINUTES),
    })
    return token


def revoke_token(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> None:
    if creds is not None:
        login_sessions.delete_one({"token_hash": _token_hash(creds.credentials)})


def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED,
        "Invalid or expired login",
        headers={"WWW-Authenticate": "Bearer"},
    )
    if creds is None:
        raise unauthorized
    session = login_sessions.find_one({"token_hash": _token_hash(creds.credentials)})
    if session is None or session["expires_at"] <= datetime.now(timezone.utc):
        raise unauthorized

    user = users.find_one({"_id": ObjectId(session["user_id"])})
    if user is None:
        raise unauthorized
    if not user.get("is_active", True):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated")
    user["id"] = str(user["_id"])
    return user

