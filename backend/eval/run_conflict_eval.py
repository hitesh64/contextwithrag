"""Measure conflict detection alone: how many known conflicts it finds and how often it flags nothing.

    python -m backend.eval.run_conflict_eval              the conflict corpus and the 26 regression questions
    python -m backend.eval.run_conflict_eval --fake-embeddings    no Gemini quota at all (bag-of-words vectors)
    python -m backend.eval.run_conflict_eval --only c07,n03

This measures the DETECTOR, not the whole assistant: no answer is generated and no generation quota
is used. Retrieval is real unless --fake-embeddings is given. The expected results live in
backend/eval/conflict_cases.json and are not to be edited to match a run.

Cases marked "out_of_scope_no_numbers" are disagreements stated in words. The detector compares
quantities, so it cannot see them; they are counted separately and never as detector misses.
"""
import argparse
import hashlib
import json
import math
import os
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CORPUS = HERE.parents[1] / "data" / "conflict_eval" / "corpus.json"
OUT_OF_SCOPE = "out_of_scope_no_numbers"


def fake_embed(texts: list[str], task: str) -> list[list[float]]:
    """The test suite's free, deterministic stand-in: texts sharing words are close."""
    from backend.app.services.keyword_search import tokenize

    vectors = []
    for text in texts:
        vector = [0.01] * 64
        for token in tokenize(text):
            vector[int(hashlib.md5(token.encode()).hexdigest(), 16) % 64] += 1.0
        norm = math.sqrt(sum(v * v for v in vector))
        vectors.append([v / norm for v in vector])
    return vectors


def check(finding_set: list[dict], superseded: list[dict], expect: dict) -> tuple[bool, list[str]]:
    """Does what was found match what the case expects? Returns (ok, reasons it does not)."""
    problems = []
    want = expect["status"]
    got = "none"
    if finding_set:
        got = "conflict" if any(f["kind"] == "conflict" for f in finding_set) else "needs_review"
    if got != want:
        problems.append(f"status {got}, expected {want}")

    if want != "none" and finding_set:
        files = {c["filename"] for f in finding_set for c in f["claims"]}
        missing = set(expect.get("sources", [])) - files
        extra = files - set(expect.get("sources", []))
        if missing:
            problems.append("sources not cited: " + ", ".join(sorted(missing)))
        if extra:
            problems.append("sources cited that the case does not list: " + ", ".join(sorted(extra)))
        text = "\n\n".join(f["report"] for f in finding_set)
        for value in expect.get("values", []):
            if value.lower() not in text.lower():
                problems.append(f"report does not contain {value!r}")

    reported = sorted(s["filename"] for s in superseded)
    if reported != sorted(expect.get("superseded", [])):
        problems.append(f"superseded reported as {reported or 'none'}, expected {expect.get('superseded') or 'none'}")
    return not problems, problems


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--fake-embeddings", action="store_true", help="no embedding calls; retrieval is then not realistic")
    parser.add_argument("--only", default="", help="comma-separated case ids")
    parser.add_argument("--skip-regression", action="store_true", help="only the conflict corpus")
    args = parser.parse_args()

    tmp = tempfile.mkdtemp(prefix="contextbasedrag_conflicteval_")
    os.environ.update(
        MONGO_URI="mongomock://conflicteval", MONGO_DB="conflicteval",
        CHROMA_DIR=os.path.join(tmp, "chroma"), STORAGE_DIR=os.path.join(tmp, "storage"),
        AI_RATE_PER_MINUTE="100000", LOGIN_RATE_PER_MINUTE="100000",
    )
    from fastapi.testclient import TestClient

    from backend.app.core.config import settings
    from backend.app.main import app
    from backend.app.services import answering, conflicts, llm

    if args.fake_embeddings:
        llm.embed = fake_embed

    spec = json.loads((HERE / "conflict_cases.json").read_text(encoding="utf-8"))
    corpus = json.loads(CORPUS.read_text(encoding="utf-8"))
    cases = spec["cases"]
    if args.only:
        cases = [c for c in cases if c["id"] in args.only.split(",")]

    rows: list[dict] = []
    with TestClient(app) as client:
        def register(name: str) -> tuple[str, dict]:
            body = {"organization_name": name, "name": "Eval", "email": f"ceval@{name}.example.com", "password": "eval-password-1"}
            org = client.post("/api/v1/auth/register", json=body).json()["organization_id"]
            token = client.post("/api/v1/auth/login", json={"email": body["email"], "password": body["password"]}).json()["access_token"]
            return org, {"Authorization": f"Bearer {token}"}

        org, headers = register("conflicteval")

        retrieved: list[str] = []

        def run(question: str, asset_id: str | None, org_id: str = org) -> tuple[list[dict], list[dict]]:
            """Retrieve evidence and run the detector on it. The model is never called."""
            asset = None
            if asset_id:
                from backend.app.api.assets import get_asset

                asset = get_asset(org_id, asset_id)
            evidence = answering.gather_evidence(org_id, question, asset)
            retrieved[:] = [e["filename"] for e in evidence if e["type"] == "document"]
            focus = [str(asset["_id"])] if asset else [
                str(a["_id"]) for a in __import__("backend.app.services.factory_context", fromlist=["x"]).detect_assets(org_id, question)
            ]
            found = conflicts.detect(evidence, question, focus, label_of=answering._source)
            for finding in found["findings"]:
                finding["report"] = conflicts.render(finding)
            return found["findings"], found["superseded"]

        # ---- the conflict corpus ----
        print(f"Loading the conflict corpus ({len(corpus['documents'])} documents)...")
        assets = {}
        for asset in corpus["assets"]:
            created = client.post("/api/v1/assets", headers=headers, json={"asset_code": asset["asset_code"], "name": asset["name"]})
            assets[asset["asset_code"]] = created.json()["id"]
        records = {}
        for doc in corpus["documents"]:
            uploaded = client.post(
                "/api/v1/documents", headers=headers,
                files={"file": (doc["filename"], doc["text"].encode())},
                data={"doc_type": doc["doc_type"], "asset_ids": ",".join(assets[c] for c in doc["asset_codes"])},
            )
            record = client.get(f"/api/v1/documents/{uploaded.json()['id']}", headers=headers).json()
            if record["status"] != "ready":
                raise SystemExit(f"{doc['filename']} was not processed: {record.get('error')}")
            records[doc["filename"]] = record
        # Version facts are recorded by a manager, exactly as in the application
        for doc in corpus["documents"]:
            fields = {k: doc[k] for k in ("revision", "effective_date", "lifecycle") if k in doc}
            if "supersedes" in doc:
                fields["supersedes_document_id"] = records[doc["supersedes"]]["id"]
            if fields:
                response = client.patch(f"/api/v1/documents/{records[doc['filename']]['id']}/version", headers=headers, json=fields)
                assert response.status_code == 200, response.text

        for case in cases:
            findings, superseded = run(case["question"], assets.get(case.get("asset_code", "")))
            ok, problems = check(findings, superseded, case["expect"])
            rows.append({
                "id": case["id"], "group": case["group"], "question": case["question"],
                "expected": case["expect"], "ok": ok, "problems": problems, "retrieved": list(retrieved),
                "found": [
                    {"kind": f["kind"], "topic": f["topic"], "differences": f["differences"],
                     "claims": [{"filename": c["filename"], "value": c["value"]} for c in f["claims"]], "report": f["report"]}
                    for f in findings
                ],
                "superseded": [s["filename"] for s in superseded],
            })
            # A word-only disagreement is outside what the detector compares; it is reported, not scored
            mark = "ok  " if ok else ("n/a " if case["group"] == OUT_OF_SCOPE else "FAIL")
            print(f"  {mark} {case['id']} {case['group']:<32} " + ("; ".join(problems) if problems else ""))

        # ---- the 26 labelled questions on the original sample dataset: nothing new may be flagged ----
        regression: list[dict] = []
        if not args.skip_regression:
            from backend.scripts import sample_loader

            print("\nLoading the original sample dataset in a second organization...")
            sample_org, sample_headers = register("sampleregression")
            loaded = sample_loader.load(client, sample_headers)
            expected = spec["regression"]["expected"]
            for q in json.loads((HERE / "questions.json").read_text(encoding="utf-8")):
                if q.get("other_organization"):
                    continue
                findings, superseded = run(q["question"], loaded["assets"].get(q.get("asset_code", "")), sample_org)
                want = expected.get(q["id"], {"status": "none"})
                ok, problems = check(findings, superseded, want)
                regression.append({
                    "id": q["id"], "kind": q["kind"], "question": q["question"], "expected": want,
                    "ok": ok, "problems": problems, "retrieved": list(retrieved),
                    "found": [
                        {"kind": f["kind"], "topic": f["topic"], "differences": f["differences"], "notes": f["notes"],
                         "claims": [{"filename": c["filename"], "value": c["value"]} for c in f["claims"]]}
                        for f in findings
                    ],
                })
                if not ok:
                    print(f"  FAIL {q['id']} {q['kind']:<18} " + "; ".join(problems))
            print(f"  {sum(1 for r in regression if r['ok'])}/{len(regression)} of the labelled questions unchanged")

    def group_of(row: dict) -> str:
        return row["group"]

    in_scope = [r for r in rows if group_of(r) != OUT_OF_SCOPE]
    positives = [r for r in in_scope if r["expected"]["status"] != "none"]
    negatives = [r for r in in_scope if r["expected"]["status"] == "none"]
    flagged_negatives = [r for r in negatives if r["found"]]
    superseded_cases = [r for r in in_scope if r["expected"].get("superseded")]
    out_of_scope = [r for r in rows if group_of(r) == OUT_OF_SCOPE]

    def tally(items: list[dict], key=lambda r: r["ok"]) -> dict | None:
        if not items:
            return None
        passed = sum(1 for r in items if key(r))
        return {"passed": passed, "of": len(items), "rate": round(passed / len(items), 3)}

    summary = {
        "embedding_model": "fake bag-of-words (no Gemini call)" if args.fake_embeddings else settings.EMBEDDING_MODEL,
        "retrieval_k": settings.RETRIEVAL_K,
        "match_thresholds": {"strong": settings.CONFLICT_MATCH_STRONG, "review": settings.CONFLICT_MATCH_REVIEW},
        "generation_model": "not used: the detector needs no model",
        "cases": len(rows),
        "conflict_recall": tally(positives),
        "conflict_recall_detail": {
            group: tally([r for r in positives if r["group"] == group])
            for group in sorted({r["group"] for r in positives})
        },
        "false_alarms": {"flagged": len(flagged_negatives), "of": len(negatives),
                         "rate": round(len(flagged_negatives) / len(negatives), 3) if negatives else None},
        "supersession_correct": tally(superseded_cases),
        "out_of_scope_word_conflicts": {"cases": len(out_of_scope), "found_by_detector": sum(1 for r in out_of_scope if r["found"]),
                                        "note": "not countable as detector recall; only the model's CONFLICT marker can find these"},
        "regression_unchanged": tally(regression) if regression else None,
    }
    report = {"summary": summary, "rows": rows, "regression": regression}
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / "conflict_latest.json").write_text(json.dumps(report, indent=2, default=str), encoding="utf-8")
    print("\nSUMMARY\n" + json.dumps(summary, indent=2))
    print(f"\nDetails: {out / 'conflict_latest.json'}")
    failures = [r["id"] for r in rows + regression if not r["ok"] and r.get("group") != OUT_OF_SCOPE]
    if failures:
        print("\nCases that did not match their expected result: " + ", ".join(failures))


if __name__ == "__main__":
    main()
