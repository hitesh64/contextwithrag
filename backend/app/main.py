import logging
import uuid
from contextlib import asynccontextmanager

from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pymongo.errors import PyMongoError

from .api import assets, audit, auth, breakdowns, chat, documents, work_orders
from .core.config import settings
from .core.database import documents as document_records, init_db
from .services import audit_service, retrieval

log = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        init_db()
    except PyMongoError as e:
        raise RuntimeError("Cannot connect to MongoDB. Check MONGO_URI and that the database is reachable.") from e
    settings.STORAGE_DIR.mkdir(parents=True, exist_ok=True)
    retrieval.init()
    orphans = retrieval.reconcile()
    if orphans:
        log.warning("Removed indexed chunks of %d deleted document(s)", orphans)
    # A document caught mid-processing by a restart would otherwise stay "processing" for ever
    document_records.update_many(
        {"status": {"$in": ["queued", "processing"]}},
        {"$set": {"status": "failed", "error": "The server restarted during processing. Use Reprocess."}},
    )
    yield


app = FastAPI(title=settings.APP_NAME, version="1.0.0", lifespan=lifespan)


class RequestIdMiddleware:
    """Give every request an id: returned as X-Request-ID and stored with its audit events."""

    def __init__(self, app):
        self.app = app

    async def __call__(self, scope, receive, send):
        if scope["type"] != "http":
            return await self.app(scope, receive, send)
        request_id = uuid.uuid4().hex
        audit_service.request_id.set(request_id)

        async def send_with_id(message):
            if message["type"] == "http.response.start":
                message.setdefault("headers", []).append((b"x-request-id", request_id.encode()))
            await send(message)

        await self.app(scope, receive, send_with_id)


app.add_middleware(RequestIdMiddleware)
if settings.CORS_ORIGINS:
    app.add_middleware(CORSMiddleware, allow_origins=settings.CORS_ORIGINS, allow_methods=["*"], allow_headers=["*"])


@app.get("/health", tags=["health"])
def health():
    return {"status": "ok", "app": settings.APP_NAME, "llm_configured": bool(settings.GOOGLE_API_KEY)}


api = APIRouter(prefix="/api/v1")
for module in (auth, assets, documents, chat, breakdowns, work_orders, audit):
    api.include_router(module.router)
app.include_router(api)

app.mount("/static", StaticFiles(directory=settings.FRONTEND_DIR, check_dir=False), name="static")


@app.get("/", include_in_schema=False)
def index():
    return FileResponse(settings.FRONTEND_DIR / "index.html", headers={"Cache-Control": "no-cache"})


@app.get("/app", include_in_schema=False)
def application():
    """The application itself: sign-in, assets, documents, chat, breakdowns, work orders."""
    return FileResponse(settings.FRONTEND_DIR / "app.html", headers={"Cache-Control": "no-cache"})
