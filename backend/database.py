"""MongoDB: users, uploaded-file metadata and SHORT-TERM chat memory."""
from pymongo import ASCENDING, DESCENDING, MongoClient
from pymongo.errors import OperationFailure

from .config import settings

client = MongoClient(settings.MONGO_URI, serverSelectionTimeoutMS=5000, tz_aware=True)
db = client[settings.MONGO_DB]

users = db["users"]
files = db["files"]
sessions = db["sessions"]
messages = db["messages"]
login_sessions = db["login_sessions"]


def _ttl_index(coll, field, seconds):
    name = f"{field}_ttl"
    try:
        coll.create_index(field, name=name, expireAfterSeconds=seconds)
    except OperationFailure:
        # Index already exists with a different TTL -> update it in place
        db.command("collMod", coll.name, index={"name": name, "expireAfterSeconds": seconds})


def init_db():
    client.admin.command("ping")
    users.create_index("email", unique=True)
    users.create_index("username", unique=True)
    login_sessions.create_index("token_hash", unique=True)
    # Expired logins are removed by MongoDB at their expires_at time
    _ttl_index(login_sessions, "expires_at", 0)
    files.create_index([("user_id", ASCENDING), ("uploaded_at", DESCENDING)])
    sessions.create_index([("user_id", ASCENDING), ("updated_at", DESCENDING)])
    messages.create_index([("session_id", ASCENDING), ("created_at", ASCENDING)])

    # Short-term memory expires automatically
    ttl = settings.SHORT_TERM_TTL_HOURS * 3600
    _ttl_index(sessions, "updated_at", ttl)
    _ttl_index(messages, "created_at", ttl)
