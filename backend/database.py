"""MongoDB: users, the document library, SHORT-TERM chat memory, the lasting copy of long-term memory
and the audit log."""
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
# Every remembered exchange with its vector; ChromaDB is refilled from here (see vector_store)
memories = db["memories"]
# Who asked what and which documents answered it. Never expires, unlike the chats themselves
audit = db["audit"]

# Banking operations module: self-contained demo records (never a real bank/payment API)
customers = db["customers"]
accounts = db["accounts"]
transactions = db["transactions"]
loans = db["loans"]
cards = db["cards"]


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
    files.create_index([("uploaded_at", DESCENDING)])
    audit.create_index([("answered", ASCENDING), ("created_at", DESCENDING)])
    sessions.create_index([("user_id", ASCENDING), ("updated_at", DESCENDING)])
    messages.create_index([("session_id", ASCENDING), ("created_at", ASCENDING)])
    customers.create_index("customer_code", unique=True)
    accounts.create_index("account_number", unique=True)
    accounts.create_index("customer_id")
    transactions.create_index([("account_id", ASCENDING), ("created_at", DESCENDING)])
    loans.create_index("customer_id")
    cards.create_index("account_id")
    memories.create_index([("user_id", ASCENDING), ("session_id", ASCENDING)])

    # Data from before roles and departments existed: documents become readable by everyone,
    # users become staff, and the oldest account administers the system
    files.update_many(
        {"departments": {"$exists": False}},
        {"$set": {"departments": [], "category": "Operation manual", "effective_date": None}},
    )
    users.update_many({"role": {"$exists": False}}, {"$set": {"role": "staff", "department": settings.DEPARTMENTS[0]}})
    if not users.find_one({"role": "admin"}):
        oldest = users.find_one(sort=[("created_at", ASCENDING)])
        if oldest:
            users.update_one({"_id": oldest["_id"]}, {"$set": {"role": "admin"}})

    # Short-term memory expires automatically
    ttl = settings.SHORT_TERM_TTL_HOURS * 3600
    _ttl_index(sessions, "updated_at", ttl)
    _ttl_index(messages, "created_at", ttl)
