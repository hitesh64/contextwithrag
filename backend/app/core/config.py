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

    LOGIN_EXPIRE_MINUTES = int(os.getenv("LOGIN_EXPIRE_MINUTES", "720"))
    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "10"))
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

    # Whether the person who wrote a work order may also approve it
    ALLOW_SELF_APPROVAL = _flag("ALLOW_SELF_APPROVAL")

    # Browser origins allowed to call the API. Empty: only the frontend served by this server.
    CORS_ORIGINS = [o.strip() for o in os.getenv("CORS_ORIGINS", "").split(",") if o.strip()]

    FRONTEND_DIR = BASE_DIR / "frontend"


settings = Settings()
