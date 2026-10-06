import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "gemini-embedding-001").strip()

    # How long a login stays valid
    LOGIN_EXPIRE_MINUTES = int(os.getenv("LOGIN_EXPIRE_MINUTES", "720"))

    MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
    MONGO_DB = os.getenv("MONGO_DB", "nexus_ai")
    # Short-term memory: chat messages expire from MongoDB after this many hours
    SHORT_TERM_TTL_HOURS = int(os.getenv("SHORT_TERM_TTL_HOURS", "24"))
    # How many recent messages of the current chat are sent to the model
    SHORT_TERM_TURNS = int(os.getenv("SHORT_TERM_TURNS", "10"))

    CHROMA_DIR = BASE_DIR / os.getenv("CHROMA_DIR", "chroma_data")

    MAX_UPLOAD_MB = int(os.getenv("MAX_UPLOAD_MB", "5"))
    # Largest file (in chunks of ~1200 characters) that is indexed; keeps embedding time and memory bounded
    MAX_FILE_CHUNKS = int(os.getenv("MAX_FILE_CHUNKS", "400"))
    INDEX_FILE = BASE_DIR / "index.html"
    IMG_DIR = BASE_DIR / "img"


settings = Settings()
