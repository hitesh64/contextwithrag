"""The company's logo, shown in its header and dashboard."""
from bson import Binary
from fastapi import APIRouter, Depends, File, HTTPException, Response, UploadFile, status

from ..core.database import organizations
from ..core.security import get_signed_in_user
from ..core.utils import now, oid, read_image
from ..services import audit_service

router = APIRouter(tags=["organization"])

LOGO_KB = 512


def logo_url(org: dict) -> str | None:
    """Where the browser loads the logo; the version in the address makes a changed logo show at once."""
    logo = org.get("logo")
    if not logo:
        return None
    return f"/api/v1/organizations/{org['_id']}/logo?v={int(logo['updated_at'].timestamp())}"


def _admin(user: dict) -> dict:
    # Allowed before the fee is paid: the logo is chosen while registering
    if user["role"] != "admin":
        raise HTTPException(status.HTTP_403_FORBIDDEN, "Only the administrator may change the company logo.")
    return user


@router.put("/organization/logo")
def upload_logo(file: UploadFile = File(...), user: dict = Depends(get_signed_in_user)):
    _admin(user)
    data, kind = read_image(file, LOGO_KB)
    org_id = oid(user["organization_id"])
    organizations.update_one({"_id": org_id}, {"$set": {"logo": {"data": Binary(data), "content_type": kind, "updated_at": now()}}})
    audit_service.record(user, "organization.logo", "organization", user["organization_id"], detail=f"{kind}, {len(data)} bytes")
    return {"logo_url": logo_url(organizations.find_one({"_id": org_id}, {"logo.updated_at": 1}))}


@router.delete("/organization/logo", status_code=status.HTTP_204_NO_CONTENT)
def remove_logo(user: dict = Depends(get_signed_in_user)):
    _admin(user)
    organizations.update_one({"_id": oid(user["organization_id"])}, {"$unset": {"logo": ""}})
    audit_service.record(user, "organization.logo_remove", "organization", user["organization_id"])


@router.get("/organizations/{organization_id}/logo")
def logo(organization_id: str):
    """Public: an <img> cannot send the login token, and a company logo is not a secret."""
    org = organizations.find_one({"_id": oid(organization_id)}, {"logo": 1})
    if not org or not org.get("logo"):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "No logo")
    return Response(
        bytes(org["logo"]["data"]), media_type=org["logo"]["content_type"],
        headers={"Cache-Control": "public, max-age=86400", "X-Content-Type-Options": "nosniff"},
    )
