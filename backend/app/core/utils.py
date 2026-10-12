import threading
import time
from collections import defaultdict, deque
from datetime import datetime, timezone

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException, status

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
