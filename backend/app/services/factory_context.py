"""Factory context: connects a machine to its documents and its breakdown history.

Everything here is computed from stored records. No model is involved, so nothing can be invented.
"""
import re
from collections import defaultdict

from ..core.database import assets, breakdowns, documents
from .keyword_search import tokenize


def _norm(code: str) -> str:
    return re.sub(r"[^a-z0-9]", "", code.lower())


def detect_assets(organization_id: str, text: str) -> list[dict]:
    """The organization's assets whose code is written in the text ("CNC-01", "cnc 01" and "CNC01" all match)."""
    words = re.findall(r"[a-z0-9]+", text.lower())
    # One word, or two or three neighbouring words written as one: "cnc 01" -> "cnc01"
    candidates = {"".join(words[i:i + n]) for n in (1, 2, 3) for i in range(len(words) - n + 1)}
    return [
        a for a in assets.find({"organization_id": organization_id, "status": {"$ne": "archived"}})
        if _norm(a["asset_code"]) in candidates
    ]


def document_ids_for_asset(organization_id: str, asset_id: str) -> list[str]:
    """Ready documents linked to this asset, plus general ones that are linked to no asset at all."""
    query = {
        "organization_id": organization_id,
        "status": "ready",
        "$or": [{"asset_ids": asset_id}, {"asset_ids": []}],
    }
    return [str(d["_id"]) for d in documents.find(query, {"_id": 1})]


def relevant_breakdowns(organization_id: str, asset_id: str, text: str, limit: int) -> list[dict]:
    """Breakdown records of one asset, those sharing words with the text first, then the most recent."""
    records = list(
        breakdowns.find({"organization_id": organization_id, "asset_id": asset_id}).sort("reported_at", -1).limit(200)
    )
    wanted = set(tokenize(text))

    def overlap(record: dict) -> int:
        described = " ".join(
            str(record.get(f) or "") for f in ("symptoms", "error_code", "root_cause", "corrective_action", "parts_used")
        )
        return len(wanted & set(tokenize(described)))

    # sorted() is stable, so records with equal overlap stay newest first
    return sorted(records, key=overlap, reverse=True)[:limit]


def _normal_symptom(text: str) -> str:
    return " ".join(sorted(set(tokenize(text))))


def breakdown_summary(organization_id: str, asset_id: str) -> dict:
    """Recorded facts about one asset's breakdowns, each figure with the records that support it."""
    records = list(breakdowns.find({"organization_id": organization_id, "asset_id": asset_id}).sort("reported_at", -1))

    def ref(r: dict) -> dict:
        return {"id": str(r["_id"]), "record_no": r["record_no"], "reported_at": r["reported_at"]}

    def groups(label_of, key_of=str.lower) -> list[dict]:
        """Records grouped by key_of(label); the group is shown under the label of its newest record."""
        found: dict[str, list[dict]] = defaultdict(list)
        labels: dict[str, str] = {}
        for r in records:
            label = (label_of(r) or "").strip()
            if label and key_of(label):
                found[key_of(label)].append(r)
                labels.setdefault(key_of(label), label)
        return sorted(
            (
                {
                    "label": labels[k],
                    "count": len(rs),
                    "downtime_minutes": sum(r.get("downtime_minutes") or 0 for r in rs),
                    "records": [ref(r) for r in rs],
                }
                for k, rs in found.items() if len(rs) > 1
            ),
            key=lambda g: g["count"], reverse=True,
        )

    missing_downtime = [r for r in records if r.get("downtime_minutes") is None]
    unknown_cause = [r for r in records if not r.get("root_cause")]
    return {
        "total_records": len(records),
        "open_records": sum(1 for r in records if r["resolution_status"] != "resolved"),
        "total_downtime_minutes": sum(r.get("downtime_minutes") or 0 for r in records),
        "first_reported_at": records[-1]["reported_at"] if records else None,
        "last_reported_at": records[0]["reported_at"] if records else None,
        # Only what occurred more than once counts as a repeat issue
        "repeat_error_codes": groups(lambda r: r.get("error_code")),
        "repeat_root_causes": groups(lambda r: r.get("root_cause")),
        "repeat_symptoms": groups(lambda r: r.get("symptoms"), _normal_symptom),
        # Gaps are reported, never filled in
        "data_gaps": {
            "root_cause_not_recorded": [ref(r) for r in unknown_cause],
            "downtime_not_recorded": [ref(r) for r in missing_downtime],
        },
    }
