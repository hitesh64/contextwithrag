"""Authentication (bcrypt + server-side login sessions), roles and per-user permissions.

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
from .database import login_sessions, organizations, users
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


def get_signed_in_user(creds: HTTPAuthorizationCredentials | None = Depends(bearer)) -> dict:
    """The logged-in user, whether or not the company has paid. Only for signing out, /auth/me and the payment."""
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


def organization_status(organization_id: str) -> str:
    """'pending_payment', 'active' or 'rejected'. Companies created before the fee existed have no status: active."""
    org = organizations.find_one({"_id": ObjectId(organization_id)}, {"status": 1})
    return (org or {}).get("status", "active")


def get_current_user(user: dict = Depends(get_signed_in_user)) -> dict:
    """The logged-in user of a company that is active, i.e. whose registration fee was accepted."""
    if organization_status(user["organization_id"]) != "active":
        raise HTTPException(status.HTTP_402_PAYMENT_REQUIRED, "Your company's registration payment is not confirmed yet.")
    return user


def is_platform_owner(user: dict) -> bool:
    return bool(settings.PLATFORM_OWNER_EMAIL) and user["email"].lower() == settings.PLATFORM_OWNER_EMAIL


def require_platform_owner(user: dict = Depends(get_signed_in_user)) -> dict:
    if not is_platform_owner(user):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the owner of this platform may do this.")
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


# What a user can be allowed to do: key -> (group shown to the administrator, label, lowest role that has it by default).
# "<section>.view" decides whether the section is visible at all; the other keys are actions inside it.
PERMISSIONS = {
    "dashboard.view": ("Dashboard", "See the dashboard", "viewer"),
    "dashboard.unanswered": ("Dashboard", "See the questions the records could not answer", "maintenance_manager"),
    "chat.ask": ("Ask", "Ask questions", "viewer"),
    "assets.view": ("Assets", "See assets", "viewer"),
    "assets.manage": ("Assets", "Add, edit and archive assets", "maintenance_manager"),
    "documents.view": ("Documents", "See documents", "viewer"),
    "documents.manage": ("Documents", "Upload, reprocess and delete documents", "maintenance_manager"),
    "breakdowns.view": ("Breakdowns", "See breakdowns", "viewer"),
    "breakdowns.report": ("Breakdowns", "Report and update breakdowns", "technician"),
    "breakdowns.import": ("Breakdowns", "Import breakdowns from a file", "maintenance_manager"),
    "work_orders.view": ("Work orders", "See work orders", "viewer"),
    "work_orders.draft": ("Work orders", "Draft, edit and submit work orders", "technician"),
    "work_orders.approve": ("Work orders", "Approve, reject and cancel work orders", "maintenance_manager"),
    # The administrator answers for the factory and may approve alone; anyone else needs a second person unless
    # the administrator gives them this
    "work_orders.approve_own": ("Work orders", "Approve work orders they wrote themselves", "admin"),
    "work_orders.execute": ("Work orders", "Start and complete approved work orders", "technician"),
    "conflicts.view": ("Conflicts", "See conflicts", "viewer"),
    "conflicts.resolve": ("Conflicts", "Record the decision that closes a conflict", "maintenance_manager"),
    "audit.view": ("Audit history", "See the audit history", "maintenance_manager"),
}
# Managing users stays with the administrator role and cannot be handed out, so nobody can grant themselves more
ADMIN_ONLY = ["users.manage"]


def role_permissions(role: str) -> list[str]:
    """What a role may do when the administrator has not chosen permissions for the user."""
    if role == "admin":
        return [*PERMISSIONS, *ADMIN_ONLY]
    lowest = {key: needed for key, (_, _, needed) in PERMISSIONS.items()}
    lowest["conflicts.resolve"] = settings.CONFLICT_RESOLVE_ROLE
    return [key for key in PERMISSIONS if ROLES.index(role) >= ROLES.index(lowest[key])]


def with_implied(keys: list[str]) -> list[str]:
    """The chosen permissions in catalogue order; an action inside a section also makes that section visible."""
    chosen = set(keys)
    if "work_orders.approve_own" in chosen:
        chosen.add("work_orders.approve")
    chosen |= {f"{k.split('.')[0]}.view" for k in keys if f"{k.split('.')[0]}.view" in PERMISSIONS}
    return [key for key in PERMISSIONS if key in chosen]


def permissions_of(user: dict) -> list[str]:
    """The user's own list if the administrator set one, otherwise what the role gives. An administrator has everything."""
    custom = user.get("permissions")
    if user["role"] == "admin" or custom is None:
        return role_permissions(user["role"])
    return [key for key in custom if key in PERMISSIONS]


def has_permission(user: dict, *keys: str) -> bool:
    """True if the user holds at least one of the permissions."""
    held = permissions_of(user)
    return any(key in held for key in keys)


def permission_label(key: str) -> str:
    return PERMISSIONS[key][1]


def require_permission(*keys: str):
    """Dependency: the logged-in user, who must hold at least one of these permissions."""

    def dependency(user: dict = Depends(get_current_user)) -> dict:
        if not has_permission(user, *keys):
            wanted = " or ".join(f"'{permission_label(k)}'" for k in keys)
            raise HTTPException(
                status.HTTP_403_FORBIDDEN, f"You do not have the permission {wanted}. Ask an administrator for access."
            )
        return user

    return dependency
