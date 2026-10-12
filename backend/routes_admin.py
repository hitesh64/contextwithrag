"""Administration: who works where, and the record of what was asked."""
from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status

from .database import audit, users
from .schemas import UserPatch, user_out
from .security import require_admin

router = APIRouter(prefix="/api/admin", tags=["admin"], dependencies=[Depends(require_admin)])

AUDIT_PAGE = 200


@router.get("/users")
def list_users():
    return [user_out(u) for u in users.find().sort("created_at", 1)]


@router.patch("/users/{user_id}")
def update_user(user_id: str, body: UserPatch, admin: dict = Depends(require_admin)):
    if not ObjectId.is_valid(user_id):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    # Otherwise the last administrator could lock everyone out of administration
    if user_id == admin["id"] and body.role == "staff":
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "You cannot remove your own administrator role.")
    changes = body.model_dump(exclude_none=True)
    user = users.find_one_and_update({"_id": ObjectId(user_id)}, {"$set": changes}, return_document=True)
    if user is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "User not found")
    return user_out(user)


@router.get("/audit")
def audit_log(unanswered: bool = False):
    """The latest questions. unanswered: only those no document could answer, i.e. what the library lacks."""
    wanted = {"answered": False} if unanswered else {}
    return [
        {
            "username": a["username"], "department": a["department"], "question": a["question"],
            "answered": a["answered"], "citations": a["citations"], "created_at": a["created_at"],
        }
        for a in audit.find(wanted).sort("created_at", -1).limit(AUDIT_PAGE)
    ]


@router.get("/stats")
def stats():
    total = audit.count_documents({})
    return {
        "questions": total,
        "unanswered": audit.count_documents({"answered": False}),
        "users": users.count_documents({}),
    }
