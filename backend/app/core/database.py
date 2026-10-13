"""MongoDB: every business record. Each one carries the organization_id it belongs to."""
from pymongo import ASCENDING, DESCENDING, MongoClient, ReturnDocument

from .config import settings

if settings.MONGO_URI.startswith("mongomock://"):
    # In-memory database for the automated tests
    import mongomock

    client = mongomock.MongoClient(tz_aware=True)
else:
    client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000, tz_aware=True)
db = client[settings.MONGO_DB]

organizations = db["organizations"]
users = db["users"]
login_sessions = db["login_sessions"]
assets = db["assets"]
documents = db["documents"]
breakdowns = db["breakdowns"]
work_orders = db["work_orders"]
audit_events = db["audit_events"]
chat_logs = db["chat_logs"]
conflicts = db["conflicts"]
# Original uploaded files, only when FILE_STORE=database
stored_files = db["stored_files"]
counters = db["counters"]


def init_db() -> None:
    client.admin.command("ping")
    users.create_index("email", unique=True)
    users.create_index("organization_id")
    login_sessions.create_index("token_hash", unique=True)
    # Expired logins are removed by MongoDB at their expires_at time
    login_sessions.create_index("expires_at", expireAfterSeconds=0)
    assets.create_index([("organization_id", ASCENDING), ("asset_code", ASCENDING)], unique=True)
    documents.create_index([("organization_id", ASCENDING), ("created_at", DESCENDING)])
    documents.create_index([("organization_id", ASCENDING), ("file_hash", ASCENDING)])
    breakdowns.create_index([("organization_id", ASCENDING), ("asset_id", ASCENDING), ("reported_at", DESCENDING)])
    breakdowns.create_index([("organization_id", ASCENDING), ("source_record_id", ASCENDING)])
    work_orders.create_index([("organization_id", ASCENDING), ("status", ASCENDING), ("created_at", DESCENDING)])
    audit_events.create_index([("organization_id", ASCENDING), ("created_at", DESCENDING)])
    chat_logs.create_index([("organization_id", ASCENDING), ("created_at", DESCENDING)])
    conflicts.create_index([("organization_id", ASCENDING), ("fingerprint", ASCENDING)], unique=True)
    conflicts.create_index([("organization_id", ASCENDING), ("status", ASCENDING), ("last_seen_at", DESCENDING)])


def next_number(organization_id: str, kind: str) -> int:
    """The next running number of one kind (work orders, breakdowns) inside one organization."""
    doc = counters.find_one_and_update(
        {"_id": f"{organization_id}:{kind}"}, {"$inc": {"value": 1}}, upsert=True, return_document=ReturnDocument.AFTER
    )
    return doc["value"]
