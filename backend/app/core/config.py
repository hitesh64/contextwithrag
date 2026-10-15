import os
from pathlib import Path

from dotenv import load_dotenv

# Repository root (backend/app/core/config.py -> three levels up)
BASE_DIR = Path(__file__).resolve().parents[3]
load_dotenv(BASE_DIR / ".env")


def _flag(name: str, default: str = "false") -> bool:
    return os.getenv(name, default).strip().lower() in ("1", "true", "yes")


class Settings:
    APP_NAME = "ContextBasedRAG"

    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    # Used when the quota of GEMINI_MODEL is used up (a free key allows it only 20 requests a day)
    GEMINI_BACKUP_MODEL = os.getenv("GEMINI_BACKUP_MODEL", "gemini-2.5-flash-lite").strip()
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001").strip()

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "contextbasedrag")

    # Vector index and the original uploaded files; both private, both outside git
    CHROMA_DIR = BASE_DIR / os.getenv("CHROMA_DIR", "chroma_data")
    STORAGE_DIR = BASE_DIR / os.getenv("STORAGE_DIR", "storage")

    # Where the original uploaded files are kept. "disk": STORAGE_DIR only. "database": also in MongoDB, for
    # hosts whose disk is wiped on every restart (free cloud plans); files are then put back on disk when needed.
    FILE_STORE = os.getenv("FILE_STORE", "disk").strip().lower()
    # Index again, at start-up, every document whose searchable chunks are gone. Needed on the same hosts,
    # because the vector index lives on that disk too. Costs embedding calls at every start.
    REINDEX_ON_START = _flag("REINDEX_ON_START")

    LOGIN_EXPIRE_MINUTES = int(os.getenv("LOGIN_EXPIRE_MINUTES", "720"))
    # Seconds a signed-in user's record and company status are kept in memory between requests, saving three database
    # round trips per page. Every request that changes something empties it, so a sign-out, a new permission or a
    # deactivation counts from the next request. 0 turns it off; the in-memory test database always has it off.
    AUTH_CACHE_SECONDS = 0 if MONGO_URI.startswith("mongomock://") else int(os.getenv("AUTH_CACHE_SECONDS", "15"))
    # How long the link in a "forgot password" mail can be used
    PASSWORD_RESET_MINUTES = int(os.getenv("PASSWORD_RESET_MINUTES", "30"))
    # A file kept in MongoDB must fit in one record (16 MB)
    MAX_UPLOAD_MB = min(int(os.getenv("MAX_UPLOAD_MB", "10")), 15 if FILE_STORE == "database" else 10_000)
    # Largest document (in chunks of ~1200 characters) that is indexed; bounds embedding cost
    MAX_FILE_CHUNKS = int(os.getenv("MAX_FILE_CHUNKS", "400"))
    MAX_IMPORT_ROWS = int(os.getenv("MAX_IMPORT_ROWS", "5000"))

    # Times in imported breakdown logs carry no zone; they are read as local time of the factory
    LOCAL_TIMEZONE = os.getenv("LOCAL_TIMEZONE", "Asia/Kolkata").strip()

    # Document passages and breakdown records given to the model per question
    RETRIEVAL_K = int(os.getenv("RETRIEVAL_K", "6"))
    BREAKDOWN_K = int(os.getenv("BREAKDOWN_K", "5"))

    # Model calls per user per minute, and login attempts per client per minute
    AI_RATE_PER_MINUTE = int(os.getenv("AI_RATE_PER_MINUTE", "10"))
    LOGIN_RATE_PER_MINUTE = int(os.getenv("LOGIN_RATE_PER_MINUTE", "10"))

    # Conflict detection: how alike (0-1) the words around two quantities must be for the sentences to count as
    # the same instruction (strong: a confirmed conflict is possible; review: only a review notice)
    CONFLICT_MATCH_STRONG = float(os.getenv("CONFLICT_MATCH_STRONG", "0.6"))
    CONFLICT_MATCH_REVIEW = float(os.getenv("CONFLICT_MATCH_REVIEW", "0.4"))
    # Lowest role that may close a conflict; "admin" for a stricter company policy
    CONFLICT_RESOLVE_ROLE = os.getenv("CONFLICT_RESOLVE_ROLE", "maintenance_manager").strip()

    # Whether the person who wrote a work order may also approve it
    ALLOW_SELF_APPROVAL = _flag("ALLOW_SELF_APPROVAL")

    # Registration fee of a new company, in whole rupees, paid through Razorpay Checkout. 0: no payment, a new
    # company is active at once. Test keys (rzp_test_...) take only test money: nothing is really charged.
    REGISTRATION_FEE = int(os.getenv("REGISTRATION_FEE", "2999"))
    RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "").strip()
    RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "").strip()
    # Optional: the secret of a webhook (Razorpay Dashboard -> Webhooks) to /api/v1/billing/webhook, for payments
    # whose browser closed before it reported back. Without it the payment page asks Razorpay itself.
    RAZORPAY_WEBHOOK_SECRET = os.getenv("RAZORPAY_WEBHOOK_SECRET", "").strip()
    # Sees every company's payment on the Payments page; the owner's own company never pays
    PLATFORM_OWNER_EMAIL = os.getenv("PLATFORM_OWNER_EMAIL", "").strip().lower()
    # The seller printed on the bill of every registration fee; bill numbers run PREFIX-YEAR-00001, 00002, ...
    INVOICE_PREFIX = os.getenv("INVOICE_PREFIX", "CBR").strip() or "CBR"
    INVOICE_SELLER_NAME = os.getenv("INVOICE_SELLER_NAME", "").strip() or APP_NAME
    INVOICE_SELLER_ADDRESS = os.getenv("INVOICE_SELLER_ADDRESS", "").strip()
    INVOICE_SELLER_GSTIN = os.getenv("INVOICE_SELLER_GSTIN", "").strip()

    # Outgoing mail (Gmail: smtp.gmail.com, 587, the account address and an app password). Empty SMTP_USER: no mail.
    SMTP_HOST = os.getenv("SMTP_HOST", "smtp.gmail.com").strip()
    SMTP_PORT = int(os.getenv("SMTP_PORT", "587"))
    SMTP_USER = os.getenv("SMTP_USER", "").strip()
    SMTP_PASSWORD = os.getenv("SMTP_PASSWORD", "").strip()
    MAIL_FROM = os.getenv("MAIL_FROM", "").strip() or SMTP_USER
    # Address of this application, for the sign-in link in mails
    APP_BASE_URL = os.getenv("APP_BASE_URL", "http://127.0.0.1:8000").strip().rstrip("/")

    # Browser origins allowed to call the API. Empty: only the frontend served by this server.
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

    FRONTEND_DIR = BASE_DIR / "frontend"


settings = Settings()
