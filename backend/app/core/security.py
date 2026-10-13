"""Authentication (bcrypt + server-side login sessions) and role checks.

On login the server creates a random token and stores only its SHA-256 hash in MongoDB with
an expiry. Logging out or deactivating a user invalidates the token immediately.

The organization a request may touch always comes from the logged-in user's own record,
never from anything the browser sends.
"""
import hashlib
import secrets
from datetime import timedelta

import bcrypt
from bson import ObjectId
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from .config import settings
from .database import login_sessions, users
from .utils import now

bearer = HTTPBearer(auto_error=False)

# Each role may do everything the roles before it may do
ROLES = ["viewer", "technician", "maintenance_manager", "admin"]


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
    created = now()
    login_sessions.insert_one({
        "token_hash": _token_hash(token),
        "user_id": user_id,
        "created_at": created,
        "expires_at": created + timedelta(minutes=settings.LOGIN_EXPIRE_MINUTES),
    })
    return token


def revoke_token(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> None:
    if creds is not None:
        login_sessions.delete_one({"token_hash": _token_hash(creds.credentials)})


def revoke_user_tokens(user_id: str) -> None:
    login_sessions.delete_many({"user_id": user_id})


def get_current_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    unauthorized = HTTPException(
        status.HTTP_401_UNAUTHORIZED, "Invalid or expired login", headers={"WWW-Authenticate": "Bearer"}
    )
    if creds is None:
        raise unauthorized
    session = login_sessions.find_one({"token_hash": _token_hash(creds.credentials)})
    if session is None or session["expires_at"] <= now():
        raise unauthorized
    user = users.find_one({"_id": ObjectId(session["user_id"])})
    if user is None:
        raise unauthorized
    if not user.get("is_active", True):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated")
    user["id"] = str(user["_id"])
    return user


def has_role(user: dict, minimum: str) -> bool:
    return ROLES.index(user["role"]) >= ROLES.index(minimum)


def require_role(minimum: str):
    """Dependency: the logged-in user, who must hold at least this role."""

    def dependency(user: dict = Depends(get_current_user)) -> dict:
        if not has_role(user, minimum):
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, f"This needs the role '{minimum}' or higher; yours is '{user['role']}'."
            )
        return user

    return dependency
