import io
import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone
from zoneinfo import ZoneInfo

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, Response, status
from openpyxl import Workbook
from openpyxl.styles import Font
from openpyxl.utils import get_column_letter

from .config import settings

# Never sent to a browser
_PRIVATE_FIELDS = ("password_hash", "storage_key")


def now() -> datetime:
    return datetime.now(timezone.utc)


def oid(value: str) -> ObjectId:
    """An id from a URL or request body; a malformed one is simply a record that does not exist."""
    try:
        return ObjectId(value)
    except (InvalidId, TypeError):
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Not found")


def clean(doc: dict) -> dict:
    """A database record as it is returned by the API."""
    out = {k: v for k, v in doc.items() if k not in _PRIVATE_FIELDS and k != "_id"}
    out["id"] = str(doc["_id"])
    return out


def paginate(collection, query: dict, page: int, page_size: int, sort: list) -> dict:
    cursor = collection.find(query).sort(sort).skip((page - 1) * page_size).limit(page_size)
    return {
        "items": [clean(d) for d in cursor],
        "total": collection.count_documents(query),
        "page": page,
        "page_size": page_size,
    }


EXPORT_LIMIT = 20_000


def xlsx_download(filename: str, columns: list[tuple[str, str]], records) -> Response:
    """An Excel file of records for download. columns: (heading, field name); at most EXPORT_LIMIT rows."""
    zone = ZoneInfo(settings.LOCAL_TIMEZONE)
    book = Workbook()
    sheet = book.active
    sheet.append([heading for heading, _ in columns])
    for cell in sheet[1]:
        cell.font = Font(bold=True)
    for record in records:
        row = []
        for _, field in columns:
            value = record.get(field)
            if isinstance(value, datetime):
                # Excel has no time zones: the factory's local time, as everywhere else in the application
                value = value.astimezone(zone).replace(tzinfo=None, microsecond=0) if value.tzinfo else value
            elif isinstance(value, (list, dict)):
                value = ", ".join(str(v) for v in value) if isinstance(value, list) else str(value)
            row.append(value)
        sheet.append(row)
        for cell in sheet[sheet.max_row]:
            if isinstance(cell.value, str):
                cell.data_type = "s"  # text typed by a user stays text, even when it starts with "="
    for index, (heading, _) in enumerate(columns, start=1):
        sheet.column_dimensions[get_column_letter(index)].width = max(12, min(48, len(heading) + 6))
    sheet.freeze_panes = "A2"
    data = io.BytesIO()
    book.save(data)
    return Response(
        data.getvalue(),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )


class RateLimiter:
    """At most `limit` events per key in any 60 seconds. Kept in memory: enough for one server process."""

    def __init__(self, limit: int):
        self.limit = limit
        self._events: dict[str, deque] = defaultdict(deque)
        self._lock = threading.Lock()

    def check(self, key: str) -> None:
        cutoff = time.monotonic() - 60
        with self._lock:
            events = self._events[key]
            while events and events[0] < cutoff:
                events.popleft()
            if len(events) >= self.limit:
                raise HTTPException(
                    status.HTTP_429_TOO_MANY_REQUESTS,
                    "Too many requests. Wait a minute and try again.",
                    headers={"Retry-After": "60"},
                )
            events.append(time.monotonic())

    def reset(self) -> None:
        with self._lock:
            self._events.clear()
