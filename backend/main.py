import mimetypes
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pymongo.errors import PyMongoError

from . import routes_auth, routes_chat, routes_files, vector_store
from .config import settings
from .database import init_db


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except PyMongoError as e:
        raise RuntimeError(f"Cannot connect to MongoDB at {settings.MONGO_URI}. Is it running?") from e
    vector_store.init()
    yield


app = FastAPI(title="CONTEXTWITHRAG", lifespan=lifespan)

# Auth uses Bearer tokens (not cookies), so allowing any origin lets index.html
# also work when opened directly from disk during development.
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

app.include_router(routes_auth.router)
app.include_router(routes_files.router)
app.include_router(routes_chat.router)


# Windows does not know the .webp type by default
mimetypes.add_type("image/webp", ".webp")
app.mount("/img", StaticFiles(directory=settings.IMG_DIR, check_dir=False), name="img")


@app.get("/api/health")
def health():
    return {
        "status": "ok",
        "llm_configured": bool(settings.GOOGLE_API_KEY),
        "max_upload_mb": settings.MAX_UPLOAD_MB,
    }


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(settings.INDEX_FILE, headers={"Cache-Control": "no-cache"})
