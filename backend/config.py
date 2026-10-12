import os
from pathlib import Path

from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / ".env")


class Settings:
    GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY", "").strip()
    GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
    # Used when the quota of GEMINI_MODEL is used up (a free key allows it only 20 requests a day)
    GEMINI_BACKUP_MODEL = os.getenv("GEMINI_BACKUP_MODEL", "gemini-2.5-flash-lite").strip()
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
    # Scanned pages of one PDF that are read with the vision model (each page is one API request)
    MAX_SCANNED_PAGES = int(os.getenv("MAX_SCANNED_PAGES", "10"))
    # Where a user works, and which departments a document can be restricted to
    DEPARTMENTS = [
        "Retail Banking", "Loans & Credit", "Compliance & Risk", "Operations", "Treasury", "Human Resources", "IT",
    ]
    CATEGORIES = ["Policy", "Circular", "Procedure (SOP)", "Operation manual", "Product note", "Form & checklist"]

    # Banking operations module (all self-contained demo records, never a real bank/payment API)
    ACCOUNT_TYPES = ["Savings", "Current", "Fixed Deposit"]
    LOAN_TYPES = ["Home", "Personal", "Auto", "Education", "Business"]
    CARD_TYPES = ["Debit", "Credit"]
    CURRENCY = "INR"
    BRANCHES = [
        {"code": "BR001", "name": "MG Road"},
        {"code": "BR002", "name": "Connaught Place"},
        {"code": "BR003", "name": "Bandra West"},
        {"code": "BR004", "name": "Koramangala"},
        {"code": "BR005", "name": "Salt Lake"},
    ]

    INDEX_FILE = BASE_DIR / "index.html"
    IMG_DIR = BASE_DIR / "img"


settings = Settings()
