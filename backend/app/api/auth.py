"""Sign-up of a factory, login, and the administrator's user management."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pymongo.errors import DuplicateKeyError

from ..core.config import settings
from ..core.database import organizations, users
from ..core.security import (
    PERMISSIONS, ROLES, create_access_token, get_signed_in_user, hash_password, is_platform_owner, permissions_of,
    require_role, revoke_token, revoke_user_tokens, role_permissions, verify_password, with_implied,
)
from ..core.utils import RateLimiter, clean, now, oid, paginate
from ..schemas import LoginIn, RegisterIn, UserCreate, UserUpdate
from ..services import audit_service
from .organization import logo_url

router = APIRouter(tags=["auth"])
login_limiter = RateLimiter(settings.LOGIN_RATE_PER_MINUTE)

# Compared against when the email is unknown, so a wrong email takes as long as a wrong password
_DUMMY_HASH = hash_password("not-a-real-password")


def _with_access(out: dict) -> dict:
    """A user record for the browser: what the user may do, and whether that differs from what the role gives."""
    out["custom_permissions"] = out["role"] != "admin" and out.get("permissions") is not None
    out["permissions"] = permissions_of(out)
    return out


def _chosen_permissions(role: str, keys: list[str]) -> list[str]:
    """A permission list from the browser, checked against the catalogue and completed with the sections it needs."""
    if role == "admin":
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "An administrator always has every permission.")
    unknown = sorted(set(keys) - set(PERMISSIONS))
    if unknown:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"Unknown permission: {', '.join(unknown)}")
    return with_implied(keys)


def _user_out(user: dict) -> dict:
    out = _with_access(clean(user))
    org = organizations.find_one({"_id": oid(user["organization_id"])}, {"name": 1, "status": 1, "logo.updated_at": 1})
    out["organization_name"] = org["name"] if org else ""
    # Until the registration fee is accepted the browser shows only the payment page
    out["organization_status"] = org.get("status", "active") if org else "active"
    out["organization_logo_url"] = logo_url(org) if org else None
    out["platform_owner"] = is_platform_owner(user)
    return out


def _new_user(
    organization_id: str, name: str, email: str, password: str, role: str, permissions: list[str] | None = None
) -> dict:
    user = {
        "organization_id": organization_id,
        "name": name,
        "email": email.lower(),
        "password_hash": hash_password(password),
        "role": role,
        "permissions": permissions,
        "is_active": True,
        "created_at": now(),
    }
    try:
        user["_id"] = users.insert_one(user).inserted_id
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, "This email is already registered.")
    user["id"] = str(user["_id"])
    return user


@router.post("/auth/register", status_code=status.HTTP_201_CREATED)
def register(body: RegisterIn, request: Request):
    """Create a new factory workspace; the person signing up becomes its administrator."""
    login_limiter.check(f"register:{request.client.host if request.client else ''}")
    if users.find_one({"email": body.email.lower()}):
        raise HTTPException(status.HTTP_409_CONFLICT, "This email is already registered.")
    # Active only after the registration fee is paid; the platform owner's own company never pays
    paid = settings.REGISTRATION_FEE <= 0 or body.email.lower() == settings.PLATFORM_OWNER_EMAIL
    org_id = organizations.insert_one({
        "name": body.organization_name, "status": "active" if paid else "pending_payment", "created_at": now(),
    }).inserted_id
    try:
        user = _new_user(str(org_id), body.name, body.email, body.password, "admin")
    except HTTPException:
        organizations.delete_one({"_id": org_id})
        raise
    audit_service.record(user, "organization.create", "organization", str(org_id))
    return _user_out(user)


@router.post("/auth/login")
def login(body: LoginIn, request: Request):
    login_limiter.check(f"login:{request.client.host if request.client else ''}:{body.email.lower()}")
    user = users.find_one({"email": body.email.lower()})
    if not verify_password(body.password, user["password_hash"] if user else _DUMMY_HASH) or user is None:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Wrong email or password.")
    if not user.get("is_active", True):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated")
    return {"access_token": create_access_token(str(user["_id"])), "token_type": "bearer", "user": _user_out(user)}


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_: None = Depends(revoke_token)):
    return None


@router.get("/auth/me")
def me(user: dict = Depends(get_signed_in_user)):
    return _user_out(user)


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), admin: dict = Depends(require_role("admin"))
):
    listed = paginate(users, {"organization_id": admin["organization_id"]}, page, page_size, [("created_at", 1)])
    listed["items"] = [_with_access(item) for item in listed["items"]]
    return listed


@router.get("/permissions")
def permission_catalogue(_: dict = Depends(require_role("admin"))):
    """Everything an administrator can allow or withhold, and what each role gets when nothing is chosen."""
    return {
        "permissions": [{"key": key, "group": group, "label": label} for key, (group, label, _) in PERMISSIONS.items()],
        "role_defaults": {role: role_permissions(role) for role in ROLES if role != "admin"},
    }


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, admin: dict = Depends(require_role("admin"))):
    chosen = None if body.permissions is None else _chosen_permissions(body.role, body.permissions)
    user = _new_user(admin["organization_id"], body.name, body.email, body.password, body.role, chosen)
    detail = f"role {body.role}" + ("" if chosen is None else f"; permissions: {', '.join(chosen) or 'none'}")
    audit_service.record(admin, "user.create", "user", user["id"], detail=detail)
    return _with_access(clean(user))


def _change_text(changes: dict) -> str:
    def text(key, value):
        if key != "permissions":
            return f"{key}={value}"
        return "permissions=role defaults" if value is None else f"permissions: {', '.join(value) or 'none'}"

    return "; ".join(text(k, v) for k, v in changes.items())


@router.patch("/users/{user_id}")
def update_user(user_id: str, body: UserUpdate, admin: dict = Depends(require_role("admin"))):
    changes = body.model_dump(exclude_none=True, exclude={"permissions"})
    target = users.find_one({"_id": oid(user_id), "organization_id": admin["organization_id"]})
    if target is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    if str(target["_id"]) == admin["id"] and (changes.get("is_active") is False or changes.get("role", "admin") != "admin"):
        # Otherwise the only administrator could lock the whole factory out
        raise HTTPException(status.HTTP_409_CONFLICT, "You cannot deactivate yourself or remove your own admin role.")
    role = changes.get("role", target["role"])
    if body.permissions is not None:
        changes["permissions"] = _chosen_permissions(role, body.permissions)
    elif "permissions" in body.model_fields_set or role != target["role"]:
        # Asked for, or the role changed: a list chosen for the old role would not describe the new one
        changes["permissions"] = None
    if changes:
        users.update_one({"_id": target["_id"]}, {"$set": changes})
        if changes.get("is_active") is False:
            revoke_user_tokens(str(target["_id"]))
        audit_service.record(admin, "user.update", "user", user_id, detail=_change_text(changes))
    return _with_access(clean(users.find_one({"_id": target["_id"]})))
