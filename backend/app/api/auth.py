"""Sign-up of a factory, login, and the administrator's user management."""
from fastapi import APIRouter, Depends, HTTPException, Query, Request, status
from pymongo.errors import DuplicateKeyError

from ..core.config import settings
from ..core.database import organizations, users
from ..core.security import (
    create_access_token, get_current_user, hash_password, require_role, revoke_token, revoke_user_tokens,
    verify_password,
)
from ..core.utils import RateLimiter, clean, now, oid, paginate
from ..schemas import LoginIn, RegisterIn, UserCreate, UserUpdate
from ..services import audit_service

router = APIRouter(tags=["auth"])
login_limiter = RateLimiter(settings.LOGIN_RATE_PER_MINUTE)

# Compared against when the email is unknown, so a wrong email takes as long as a wrong password
_DUMMY_HASH = hash_password("not-a-real-password")


def _user_out(user: dict) -> dict:
    out = clean(user)
    org = organizations.find_one({"_id": oid(user["organization_id"])})
    out["organization_name"] = org["name"] if org else ""
    return out


def _new_user(organization_id: str, name: str, email: str, password: str, role: str) -> dict:
    user = {
        "organization_id": organization_id,
        "name": name,
        "email": email.lower(),
        "password_hash": hash_password(password),
        "role": role,
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
    org_id = organizations.insert_one({"name": body.organization_name, "created_at": now()}).inserted_id
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
def me(user: dict = Depends(get_current_user)):
    return _user_out(user)


@router.get("/users")
def list_users(
    page: int = Query(1, ge=1), page_size: int = Query(50, ge=1, le=100), admin: dict = Depends(require_role("admin"))
):
    return paginate(users, {"organization_id": admin["organization_id"]}, page, page_size, [("created_at", 1)])


@router.post("/users", status_code=status.HTTP_201_CREATED)
def create_user(body: UserCreate, admin: dict = Depends(require_role("admin"))):
    user = _new_user(admin["organization_id"], body.name, body.email, body.password, body.role)
    audit_service.record(admin, "user.create", "user", user["id"], detail=f"role {body.role}")
    return clean(user)


@router.patch("/users/{user_id}")
def update_user(user_id: str, body: UserUpdate, admin: dict = Depends(require_role("admin"))):
    changes = body.model_dump(exclude_none=True)
    target = users.find_one({"_id": oid(user_id), "organization_id": admin["organization_id"]})
    if target is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")
    if str(target["_id"]) == admin["id"] and (changes.get("is_active") is False or changes.get("role", "admin") != "admin"):
        # Otherwise the only administrator could lock the whole factory out
        raise HTTPException(status.HTTP_409_CONFLICT, "You cannot deactivate yourself or remove your own admin role.")
    if changes:
        users.update_one({"_id": target["_id"]}, {"$set": changes})
        if changes.get("is_active") is False:
            revoke_user_tokens(str(target["_id"]))
        audit_service.record(admin, "user.update", "user", user_id, detail=", ".join(f"{k}={v}" for k, v in changes.items()))
    return clean(users.find_one({"_id": target["_id"]}))
