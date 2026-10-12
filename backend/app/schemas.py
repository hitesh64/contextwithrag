"""Request bodies. Unknown fields are rejected, so a browser cannot slip in organization_id or status."""
import re
from datetime import date, datetime
from typing import Literal

from pydantic import BaseModel, ConfigDict, EmailStr, Field, field_validator

Role = Literal["viewer", "technician", "maintenance_manager", "admin"]
Criticality = Literal["low", "medium", "high", "critical"]
AssetStatus = Literal["active", "under_maintenance", "inactive"]
Priority = Literal["low", "medium", "high", "critical"]
ResolutionStatus = Literal["open", "in_progress", "resolved"]
DocType = Literal["manual", "sop", "spare_parts", "other"]

ASSET_CODE_PATTERN = r"^[A-Z0-9][A-Z0-9\-_/]{1,29}$"


class Body(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class RegisterIn(Body):
    organization_name: str = Field(min_length=2, max_length=100)
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)


class LoginIn(Body):
    email: EmailStr
    password: str = Field(min_length=1, max_length=128)


class UserCreate(Body):
    name: str = Field(min_length=2, max_length=80)
    email: EmailStr
    password: str = Field(min_length=8, max_length=128)
    role: Role


class UserUpdate(Body):
    name: str | None = Field(None, min_length=2, max_length=80)
    role: Role | None = None
    is_active: bool | None = None


class AssetCreate(Body):
    asset_code: str
    name: str = Field(min_length=2, max_length=120)
    asset_type: str = Field("", max_length=60)
    manufacturer: str = Field("", max_length=80)
    model: str = Field("", max_length=80)
    serial_number: str = Field("", max_length=80)
    location: str = Field("", max_length=120)
    criticality: Criticality = "medium"
    status: AssetStatus = "active"

    @field_validator("asset_code")
    @classmethod
    def code(cls, value: str) -> str:
        value = value.strip().upper()
        if not re.match(ASSET_CODE_PATTERN, value):
            raise ValueError("2-30 characters: letters, digits, '-', '_' or '/', starting with a letter or digit")
        return value


class AssetUpdate(Body):
    """The asset code is the machine's identity across documents and records, so it cannot be changed."""
    name: str | None = Field(None, min_length=2, max_length=120)
    asset_type: str | None = Field(None, max_length=60)
    manufacturer: str | None = Field(None, max_length=80)
    model: str | None = Field(None, max_length=80)
    serial_number: str | None = Field(None, max_length=80)
    location: str | None = Field(None, max_length=120)
    criticality: Criticality | None = None
    status: AssetStatus | None = None


class ChatIn(Body):
    question: str = Field(min_length=2, max_length=2000)
    asset_id: str | None = None
    document_id: str | None = None


class BreakdownCreate(Body):
    asset_id: str
    reported_at: datetime
    symptoms: str = Field(min_length=3, max_length=2000)
    error_code: str | None = Field(None, max_length=60)
    downtime_minutes: int | None = Field(None, ge=0, le=1_000_000)
    root_cause: str | None = Field(None, max_length=1000)
    corrective_action: str | None = Field(None, max_length=2000)
    parts_used: str | None = Field(None, max_length=500)
    resolution_status: ResolutionStatus = "open"


class BreakdownUpdate(Body):
    symptoms: str | None = Field(None, min_length=3, max_length=2000)
    error_code: str | None = Field(None, max_length=60)
    downtime_minutes: int | None = Field(None, ge=0, le=1_000_000)
    root_cause: str | None = Field(None, max_length=1000)
    corrective_action: str | None = Field(None, max_length=2000)
    parts_used: str | None = Field(None, max_length=500)
    resolution_status: ResolutionStatus | None = None


class ChecklistItemIn(Body):
    step: str = Field(min_length=1, max_length=500)
    sources: list[int] = []


class WorkOrderCreate(Body):
    asset_id: str
    title: str = Field(min_length=3, max_length=200)
    description: str = Field("", max_length=5000)
    priority: Priority = "medium"
    checklist: list[ChecklistItemIn] = Field(default_factory=list, max_length=30)


class WorkOrderGenerate(Body):
    asset_id: str
    problem: str = Field(min_length=5, max_length=2000)


class WorkOrderUpdate(Body):
    title: str | None = Field(None, min_length=3, max_length=200)
    description: str | None = Field(None, max_length=5000)
    priority: Priority | None = None
    checklist: list[ChecklistItemIn] | None = Field(None, max_length=30)


class TransitionIn(Body):
    to: Literal["pending_approval", "approved", "rejected", "draft", "in_progress", "completed", "cancelled"]
    comment: str = Field("", max_length=1000)


class CommentIn(Body):
    comment: str = Field("", max_length=1000)


class DocumentVersionUpdate(Body):
    """Version facts about a document. Left out means unchanged; they are never guessed from the file."""
    revision: str | None = Field(None, max_length=40)
    effective_date: date | None = None
    lifecycle: Literal["current", "superseded"] | None = None
    supersedes_document_id: str | None = Field(None, max_length=40)


class ConflictResolveIn(Body):
    decision: Literal["governs", "outdated", "both_apply", "false_alarm"]
    document_id: str | None = Field(None, max_length=40, description="The document the decision is about (governs / outdated)")
    note: str = Field(min_length=10, max_length=1000)
