from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from pymongo.errors import DuplicateKeyError

from .database import users
from .schemas import LoginIn, RegisterIn, TokenOut, UserOut, user_out
from .security import create_access_token, get_current_user, hash_password, revoke_token, verify_password

router = APIRouter(prefix="/api", tags=["auth"])


@router.post("/auth/register", response_model=UserOut, status_code=status.HTTP_201_CREATED)
def register(body: RegisterIn):
    email = body.email.lower()
    if users.find_one({"email": email}):
        raise HTTPException(status.HTTP_409_CONFLICT, "An account with this email already exists")
    if users.find_one({"username": body.username}):
        raise HTTPException(status.HTTP_409_CONFLICT, "This username is already taken")

    user = {
        "username": body.username,
        "email": email,
        "password_hash": hash_password(body.password),
        "is_active": True,
        "created_at": datetime.now(timezone.utc),
    }
    try:
        user["_id"] = users.insert_one(user).inserted_id
    except DuplicateKeyError:
        raise HTTPException(status.HTTP_409_CONFLICT, "Email or username already in use")
    # No token here: the new user signs in on the login form
    return user_out(user)


@router.post("/auth/login", response_model=TokenOut)
def login(body: LoginIn):
    user = users.find_one({"username": body.username.strip()})
    if user is None or not verify_password(body.password, user["password_hash"]):
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, "Incorrect username or password")
    if not user.get("is_active", True):
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Account is deactivated")
    return TokenOut(access_token=create_access_token(str(user["_id"])), user=user_out(user))


@router.post("/auth/logout", status_code=status.HTTP_204_NO_CONTENT)
def logout(_: None = Depends(revoke_token)):
    return None


@router.get("/auth/me", response_model=UserOut)
def me(user: dict = Depends(get_current_user)):
    return user_out(user)

