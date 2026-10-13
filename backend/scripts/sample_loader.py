"""Load the synthetic sample dataset (data/sample/) into one organization through the real API."""
import json
import time
from pathlib import Path

SAMPLE_DIR = Path(__file__).resolve().parents[2] / "data" / "sample"
API = "/api/v1"


def _ok(response, expected: int):
    if response.status_code != expected:
        raise RuntimeError(f"{response.request.method} {response.request.url.path} -> {response.status_code}: {response.text}")
    return response.json()


def load(client, headers: dict, strict: bool = True) -> dict:
    """Create the sample assets, upload and process the documents, import the breakdowns.

    client: a fastapi TestClient, or an httpx.Client pointed at a running server.
    strict: raise if a document fails processing; otherwise its record carries the error.
    Returns {"assets": {code: id}, "documents": {filename: record}}.
    """
    if not SAMPLE_DIR.is_dir():
        raise RuntimeError("data/sample is missing. Run: python -m backend.scripts.make_sample_data")
    assets = {}
    for asset in json.loads((SAMPLE_DIR / "assets.json").read_text(encoding="utf-8")):
        assets[asset["asset_code"]] = _ok(client.post(f"{API}/assets", headers=headers, json=asset), 201)["id"]

    documents = {}
    for doc in json.loads((SAMPLE_DIR / "documents.json").read_text(encoding="utf-8")):
        uploaded = _ok(client.post(
            f"{API}/documents", headers=headers,
            files={"file": (doc["filename"], (SAMPLE_DIR / doc["filename"]).read_bytes())},
            data={"doc_type": doc["doc_type"], "asset_ids": ",".join(assets[c] for c in doc["asset_codes"])},
        ), 202)
        record = uploaded
        for _ in range(120):
            record = _ok(client.get(f"{API}/documents/{uploaded['id']}", headers=headers), 200)
            if record["status"] not in ("queued", "processing"):
                break
            time.sleep(1)
        if strict and record["status"] != "ready":
            raise RuntimeError(f"{doc['filename']} was not processed: {record['error']}")
        documents[doc["filename"]] = record

    report = _ok(client.post(
        f"{API}/breakdowns/import", headers=headers,
        files={"file": ("breakdowns.csv", (SAMPLE_DIR / "breakdowns.csv").read_bytes())},
    ), 200)
    if report["rejected"]:
        raise RuntimeError(f"Sample breakdowns were rejected: {report['errors']}")
    return {"assets": assets, "documents": documents}
