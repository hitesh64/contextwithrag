"""Audit trail: who did what to which record, and whether it worked.

Only identifiers and short facts are stored: never passwords, tokens or document contents.
"""
import contextvars

from ..core.database import audit_events
from ..core.utils import now

# Set per request by the middleware in main.py; ties log lines, audit events and API responses together
request_id: contextvars.ContextVar[str] = contextvars.ContextVar("request_id", default="")


def record(
    user: dict, action: str, resource_type: str, resource_id: str = "", result: str = "success", detail: str = ""
) -> None:
    audit_events.insert_one({
        "organization_id": user["organization_id"],
        "actor_id": user["id"],
        "actor_name": user["name"],
        "action": action,
        "resource_type": resource_type,
        "resource_id": resource_id,
        "detail": detail[:300],
        "request_id": request_id.get(),
        "result": result,
        "created_at": now(),
    })
