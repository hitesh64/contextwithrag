"""Breakdown history: single records and validated CSV/XLSX imports."""
import csv
import io
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from fastapi import APIRouter, Depends, File, HTTPException, Query, UploadFile, status
from fastapi.responses import PlainTextResponse
from openpyxl import load_workbook

from ..core.config import settings
from ..core.database import assets, breakdowns, next_number
from ..core.security import get_current_user, require_role
from ..core.utils import clean, now, oid, paginate
from ..schemas import BreakdownCreate, BreakdownUpdate
from ..services import audit_service
from .assets import get_asset

router = APIRouter(prefix="/breakdowns", tags=["breakdowns"])

COLUMNS = [
    "asset_code", "reported_at", "symptoms", "error_code", "downtime_minutes", "root_cause",
    "corrective_action", "parts_used", "resolution_status", "source_record_id",
]
REQUIRED = ["asset_code", "reported_at", "symptoms"]
STATUSES = ["open", "in_progress", "resolved"]
_DATE_FORMATS = [
    "%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%dT%H:%M:%S", "%Y-%m-%dT%H:%M", "%Y-%m-%d",
    "%d/%m/%Y %H:%M", "%d/%m/%Y", "%d-%m-%Y %H:%M", "%d-%m-%Y",
]
TEMPLATE = ",".join(COLUMNS) + "\nCNC-01,2026-01-15 09:30,Spindle overheating alarm,E-204,120,Coolant pump failed,Replaced coolant pump,Coolant pump CP-12,resolved,LOG-0001\n"


def _record(user: dict, asset: dict, **fields) -> dict:
    return {
        "organization_id": user["organization_id"],
        "record_no": f"BD-{next_number(user['organization_id'], 'breakdown'):04d}",
        "asset_id": str(asset["_id"]),
        "asset_code": asset["asset_code"],
        **fields,
        "created_by": user["id"],
        "created_at": now(),
    }


def _text(value) -> str | None:
    """A cell as text; an empty cell is None, so 'not recorded' stays distinguishable from a value."""
    if value is None:
        return None
    text = str(value).strip()
    return text or None


def _timestamp(value) -> datetime:
    """Times without a zone are taken as the factory's local time (LOCAL_TIMEZONE)."""
    if isinstance(value, datetime):
        parsed = value
    else:
        for fmt in _DATE_FORMATS:
            try:
                parsed = datetime.strptime(str(value).strip(), fmt)
                break
            except ValueError:
                continue
        else:
            raise ValueError("reported_at is not a date (use YYYY-MM-DD HH:MM or DD/MM/YYYY)")
    parsed = _aware(parsed)
    if parsed > now():
        raise ValueError("reported_at is in the future")
    return parsed


def _rows(filename: str, data: bytes) -> list[dict]:
    """The rows of a CSV or XLSX file as dicts keyed by the lower-case column name."""
    if filename.lower().endswith(".xlsx"):
        try:
            sheet = load_workbook(io.BytesIO(data), read_only=True, data_only=True).active
            table = [list(r) for r in sheet.iter_rows(values_only=True)]
        except Exception:
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "The file is not a valid .xlsx file.")
    elif filename.lower().endswith(".csv"):
        try:
            table = list(csv.reader(io.StringIO(data.decode("utf-8-sig"))))
        except (UnicodeDecodeError, csv.Error):
            raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "The file is not a valid UTF-8 .csv file.")
    else:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "Upload a .csv or .xlsx file.")

    table = [r for r in table if any(c not in (None, "") for c in r)]
    if not table:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "The file has no rows.")
    header = [str(c or "").strip().lower() for c in table[0]]
    missing = [c for c in REQUIRED if c not in header]
    if missing:
        raise HTTPException(
            status.HTTP_422_UNPROCESSABLE_CONTENT,
            f"Missing required column(s): {', '.join(missing)}. Download the template for the expected columns.",
        )
    if len(table) - 1 > settings.MAX_IMPORT_ROWS:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"At most {settings.MAX_IMPORT_ROWS} rows per import.")
    return [dict(zip(header, row)) for row in table[1:]]


def _validated(row: dict, by_code: dict[str, dict]) -> tuple[dict, dict]:
    """(asset, fields) of one import row; raises ValueError naming what is wrong with it."""
    code = (_text(row.get("asset_code")) or "").upper()
    if not code:
        raise ValueError("asset_code is empty")
    asset = by_code.get(code)
    if asset is None:
        raise ValueError(f"unknown asset_code {code}")
    if row.get("reported_at") in (None, ""):
        raise ValueError("reported_at is empty")
    symptoms = _text(row.get("symptoms"))
    if not symptoms:
        raise ValueError("symptoms is empty")

    downtime = _text(row.get("downtime_minutes"))
    if downtime is not None:
        try:
            downtime = int(float(downtime))
        except ValueError:
            raise ValueError("downtime_minutes is not a number")
        if downtime < 0:
            raise ValueError("downtime_minutes is negative")

    state = (_text(row.get("resolution_status")) or "open").lower().replace(" ", "_")
    if state not in STATUSES:
        raise ValueError(f"resolution_status must be one of: {', '.join(STATUSES)}")
    return asset, {
        "reported_at": _timestamp(row["reported_at"]),
        "symptoms": symptoms,
        "error_code": _text(row.get("error_code")),
        "downtime_minutes": downtime,
        "root_cause": _text(row.get("root_cause")),
        "corrective_action": _text(row.get("corrective_action")),
        "parts_used": _text(row.get("parts_used")),
        "resolution_status": state,
        "source_record_id": _text(row.get("source_record_id")),
    }


@router.get("/template", response_class=PlainTextResponse)
def import_template(_: dict = Depends(get_current_user)):
    return PlainTextResponse(TEMPLATE, media_type="text/csv", headers={
        "Content-Disposition": 'attachment; filename="breakdown_import_template.csv"'
    })


@router.post("/import")
def import_breakdowns(
    file: UploadFile = File(...),
    dry_run: bool = Query(False, description="Validate only; store nothing"),
    user: dict = Depends(require_role("maintenance_manager")),
):
    """Import the valid rows and report every rejected row with its reason.

    A row whose source_record_id was imported before is skipped, so importing a file twice is harmless.
    """
    org = user["organization_id"]
    data = file.file.read(settings.MAX_UPLOAD_MB * 1024 * 1024 + 1)
    if len(data) > settings.MAX_UPLOAD_MB * 1024 * 1024:
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, f"The file is larger than {settings.MAX_UPLOAD_MB} MB.")
    rows = _rows(file.filename or "", data)

    by_code = {a["asset_code"]: a for a in assets.find({"organization_id": org})}
    known = {
        b["source_record_id"]
        for b in breakdowns.find({"organization_id": org, "source_record_id": {"$ne": None}}, {"source_record_id": 1})
    }
    accepted, errors, duplicates = [], [], 0
    for line, row in enumerate(rows, start=2):
        try:
            asset, fields = _validated(row, by_code)
        except ValueError as e:
            errors.append({"row": line, "error": str(e)})
            continue
        if fields["source_record_id"] and fields["source_record_id"] in known:
            duplicates += 1
            continue
        if fields["source_record_id"]:
            known.add(fields["source_record_id"])
        accepted.append((asset, fields))

    if not dry_run and accepted:
        breakdowns.insert_many([_record(user, asset, **fields) for asset, fields in accepted])
        audit_service.record(
            user, "breakdown.import", "breakdown", detail=f"{len(accepted)} imported, {len(errors)} rejected from {file.filename}"
        )
    return {
        "dry_run": dry_run,
        "total_rows": len(rows),
        "imported": 0 if dry_run else len(accepted),
        "valid": len(accepted),
        "skipped_duplicates": duplicates,
        "rejected": len(errors),
        "errors": errors[:200],
    }


@router.get("")
def list_breakdowns(
    asset_id: str = "",
    status_: str = Query("", alias="status"),
    q: str = Query("", max_length=100, description="Words in symptoms, root cause or corrective action"),
    error_code: str = "",
    date_from: datetime | None = None,
    date_to: datetime | None = None,
    page: int = Query(1, ge=1),
    page_size: int = Query(50, ge=1, le=200),
    user: dict = Depends(get_current_user),
):
    query: dict = {"organization_id": user["organization_id"]}
    if asset_id:
        query["asset_id"] = asset_id
    if status_:
        query["resolution_status"] = status_
    if error_code:
        query["error_code"] = {"$regex": f"^{re.escape(error_code)}$", "$options": "i"}
    if q:
        pattern = {"$regex": re.escape(q), "$options": "i"}
        query["$or"] = [{f: pattern} for f in ("symptoms", "root_cause", "corrective_action", "error_code", "asset_code")]
    if date_from or date_to:
        query["reported_at"] = {
            **({"$gte": date_from} if date_from else {}), **({"$lte": date_to} if date_to else {}),
        }
    return paginate(breakdowns, query, page, page_size, [("reported_at", -1)])


@router.post("", status_code=status.HTTP_201_CREATED)
def create_breakdown(body: BreakdownCreate, user: dict = Depends(require_role("technician"))):
    asset = get_asset(user["organization_id"], body.asset_id)
    fields = body.model_dump(exclude={"asset_id"})
    fields["reported_at"] = _aware(fields["reported_at"])
    if fields["reported_at"] > now():
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_CONTENT, "reported_at is in the future")
    record = _record(user, asset, **{k: (v or None) if isinstance(v, str) else v for k, v in fields.items()}, source_record_id=None)
    record["_id"] = breakdowns.insert_one(record).inserted_id
    audit_service.record(user, "breakdown.create", "breakdown", str(record["_id"]), detail=asset["asset_code"])
    return clean(record)


def _aware(value: datetime) -> datetime:
    return value if value.tzinfo else value.replace(tzinfo=ZoneInfo(settings.LOCAL_TIMEZONE))


@router.patch("/{breakdown_id}")
def update_breakdown(breakdown_id: str, body: BreakdownUpdate, user: dict = Depends(require_role("technician"))):
    record = breakdowns.find_one({"_id": oid(breakdown_id), "organization_id": user["organization_id"]})
    if record is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Breakdown record not found")
    changes = body.model_dump(exclude_unset=True)
    if changes.get("symptoms") is None:
        changes.pop("symptoms", None)
    if changes.get("resolution_status") is None:
        changes.pop("resolution_status", None)
    # An emptied text field goes back to "not recorded"
    changes = {k: (v or None) if isinstance(v, str) else v for k, v in changes.items()}
    if changes:
        breakdowns.update_one({"_id": record["_id"]}, {"$set": changes})
        audit_service.record(user, "breakdown.update", "breakdown", breakdown_id, detail=", ".join(changes))
    return clean(breakdowns.find_one({"_id": record["_id"]}))
