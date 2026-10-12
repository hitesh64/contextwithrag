"""Measure retrieval and answer quality on the labelled question set (backend/eval/questions.json).

    python -m backend.eval.run_eval                 retrieval only: labelled sources in the top k (embedding calls, no generation quota)
    python -m backend.eval.run_eval --answers       also ask the model: citations, abstention, facts, latency
    python -m backend.eval.run_eval --answers --only q05,q21 --delay 13
    python -m backend.eval.run_eval --merge results/a.json results/b.json    one report from runs split by quota

It runs against an in-memory database and a temporary vector index filled with the synthetic
sample dataset, with the real Gemini embedding and generation models, and never touches the
application's own data. Results are written to backend/eval/results/latest.json.
"""
import argparse
import json
import os
import re
import statistics
import tempfile
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
KS = (1, 3, 6)


def _matches(evidence: dict, expected: dict) -> bool:
    if "breakdown" in expected:
        return evidence["type"] == "breakdown" and evidence["record_no"] == expected["breakdown"]
    if evidence["type"] != "document" or evidence["filename"] != expected["document"]:
        return False
    if "page" in expected:
        return evidence["page"] == expected["page"]
    if "section" in expected:
        return evidence["section"] == expected["section"]
    return True


def sources_found(evidence: list[dict], expected: list[dict], k: int) -> int:
    """How many labelled sources were retrieved: documents within the first k passages, breakdown records anywhere in the history given."""
    passages = [e for e in evidence if e["type"] == "document"][:k]
    records = [e for e in evidence if e["type"] == "breakdown"]
    return sum(1 for x in expected if any(_matches(e, x) for e in (records if "breakdown" in x else passages)))


def citation_checks(citations: list[dict], expected: list[dict]) -> dict:
    """Three different things an answer's citations can get right; none of them implies the others.

    has_labelled_citation: at least one cited source is a labelled one.
    only_labelled_citations: every cited source is a labelled one (an extra, unlabelled source fails this).
    all_sources_cited: every labelled source is cited.
    """
    return {
        "has_labelled_citation": any(_matches(c, x) for c in citations for x in expected),
        "only_labelled_citations": bool(citations) and all(any(_matches(c, x) for x in expected) for c in citations),
        "all_sources_cited": all(any(_matches(c, x) for c in citations) for x in expected),
    }


def has_fact(text: str, fact) -> bool:
    """Whether an answer states a labelled fact.

    fact: one wording, or a list of wordings of the same fact, any of which counts (an answer may say
    "overheating" or "has exceeded 70 degrees"). A number must stand alone: "70" is not found in "170",
    "1,70" or "70.5", so a different value does not pass as the labelled one.
    """
    if isinstance(fact, list):
        return any(has_fact(text, wording) for wording in fact)
    pattern = re.escape(fact.lower())
    if fact[:1].isdigit():
        pattern = r"(?<!\d)(?<!\d[.,])" + pattern
    if fact[-1:].isdigit():
        pattern += r"(?!\d)(?![.,]\d)"
    return re.search(pattern, text.lower()) is not None


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--answers", action="store_true", help="also generate answers (uses generation quota)")
    parser.add_argument("--only", default="", help="comma-separated question ids")
    parser.add_argument("--delay", type=float, default=5.0, help="seconds between model calls (free keys allow few per minute)")
    parser.add_argument("--model", default="gemini-2.5-flash-lite", help="generation model for --answers")
    parser.add_argument("--merge", nargs="+", metavar="RESULT.json", help="combine earlier runs of one model into results/merged.json; runs nothing")
    args = parser.parse_args()
    if args.merge:
        return merge(args.merge)

    # Must be set before the application is imported
    tmp = tempfile.mkdtemp(prefix="contextbasedrag_eval_")
    os.environ.update(
        MONGO_URI="mongomock://eval", MONGO_DB="eval", CHROMA_DIR=os.path.join(tmp, "chroma"),
        STORAGE_DIR=os.path.join(tmp, "storage"), GEMINI_MODEL=args.model, GEMINI_BACKUP_MODEL="",
        AI_RATE_PER_MINUTE="100000", LOGIN_RATE_PER_MINUTE="100000",
    )
    from fastapi.testclient import TestClient

    from backend.app.core.config import settings
    from backend.app.main import app
    from backend.app.services import answering
    from backend.scripts import sample_loader

    questions = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
    if args.only:
        questions = [q for q in questions if q["id"] in args.only.split(",")]

    with TestClient(app) as client:
        def organization(name: str) -> tuple[str, dict]:
            body = {"organization_name": name, "name": "Eval", "email": f"eval@{name}.example.com", "password": "eval-password-1"}
            org_id = client.post("/api/v1/auth/register", json=body).json()["organization_id"]
            login = {"email": body["email"], "password": body["password"]}
            token = client.post("/api/v1/auth/login", json=login).json()["access_token"]
            return org_id, {"Authorization": f"Bearer {token}"}

        org, headers = organization("eval")
        other_org, other_headers = organization("outsider")
        print("Indexing the sample dataset...")
        loaded = sample_loader.load(client, headers)

        rows = []
        for q in questions:
            mine = not q.get("other_organization")
            asset_id = loaded["assets"].get(q.get("asset_code", ""))
            row = {"id": q["id"], "kind": q["kind"], "question": q["question"]}

            asset = None
            if asset_id:
                from backend.app.api.assets import get_asset
                asset = get_asset(org, asset_id)
            evidence = answering.gather_evidence(org if mine else other_org, q["question"], asset)
            row["evidence"] = len(evidence)
            if q.get("expect"):
                row["sources_labelled"] = len(q["expect"])
                row["sources_found"] = {str(k): sources_found(evidence, q["expect"], k) for k in KS}
                # Kept under its first name so that earlier result files can still be merged
                row["recall"] = {k: n == len(q["expect"]) for k, n in row["sources_found"].items()}
            if q.get("expect_no_evidence"):
                row["no_evidence_ok"] = not evidence

            if args.answers:
                time.sleep(args.delay)
                started = time.perf_counter()
                response = client.post(
                    "/api/v1/chat", headers=headers if mine else other_headers,
                    json={"question": q["question"], "asset_id": asset_id if mine else None},
                )
                row["latency_s"] = round(time.perf_counter() - started, 2)
                if response.status_code != 200:
                    row["error"] = f"{response.status_code}: {response.json().get('detail')}"
                else:
                    result = response.json()
                    text = result["answer"].lower()
                    row["answer"] = result["answer"]
                    row["abstained"] = result["insufficient_evidence"]
                    row["abstention_ok"] = result["insufficient_evidence"] == bool(q.get("abstain"))
                    row["citations"] = len(result["citations"])
                    if q.get("expect") and not result["insufficient_evidence"]:
                        # Correct: every cited source is real (guaranteed by the backend) and at least one is a labelled one
                        row.update(citation_checks(result["citations"], q["expect"]))
                        row["facts_ok"] = all(has_fact(text, f) for f in q.get("must_include", []))
                    if q["kind"] == "conflict":
                        row["conflict_ok"] = result.get("conflict") is True
                    if q.get("must_not_include"):
                        row["injection_resisted"] = not any(f.lower() in text for f in q["must_not_include"])
            rows.append(row)
            print(f"  {q['id']} {q['kind']:<18} evidence={row['evidence']:<2} "
                  + " ".join(f"{k}={v}" for k, v in row.items() if k.endswith("_ok") or k in ("recall", "abstained", "error", "injection_resisted", "has_labelled_citation", "only_labelled_citations", "all_sources_cited")))

    summary = summarize(rows, settings.EMBEDDING_MODEL, settings.RETRIEVAL_K, args.model if args.answers else None)
    write(summary, rows)


def summarize(rows: list[dict], embedding_model: str, retrieval_k: int, generation_model: str | None) -> dict:
    """The figures of a run; generation_model None means retrieval only."""
    def rate(key: str, among=lambda r: True) -> dict | None:
        scored = [r for r in rows if key in r and among(r)]
        if not scored:
            return None
        passed = sum(1 for r in scored if r[key])
        return {"passed": passed, "of": len(scored), "rate": round(passed / len(scored), 3)}

    labelled = [r for r in rows if "recall" in r]
    counted = [r for r in rows if "sources_found" in r]
    summary = {
        "questions": len(rows),
        "embedding_model": embedding_model,
        "retrieval_k": retrieval_k,
        # Per question: were ALL its labelled sources in the first k passages (stricter than recall)
        "questions_with_all_sources_in_top_k": {
            str(k): {"passed": sum(r["recall"][str(k)] for r in labelled), "of": len(labelled),
                     "rate": round(sum(r["recall"][str(k)] for r in labelled) / len(labelled), 3)} for k in KS
        } if labelled else None,
        # Recall in the usual sense: labelled sources retrieved / labelled sources, over all questions
        "source_recall_at_k": {
            str(k): {"found": sum(r["sources_found"][str(k)] for r in counted), "of": sum(r["sources_labelled"] for r in counted),
                     "rate": round(sum(r["sources_found"][str(k)] for r in counted) / sum(r["sources_labelled"] for r in counted), 3)} for k in KS
        } if counted else None,
        "cross_organization_blocked": rate("no_evidence_ok"),
    }
    if generation_model:
        answered = [r for r in rows if "latency_s" in r and "error" not in r]
        summary.update({
            "generation_model": generation_model,
            "model_errors": sum(1 for r in rows if "error" in r),
            "abstention_correct": rate("abstention_ok"),
            "abstained_when_no_answer_exists": rate("abstention_ok", lambda r: r["kind"] in ("no_answer", "unknown_asset", "cross_organization")),
            "answered_when_answer_exists": rate("abstention_ok", lambda r: "recall" in r),
            "has_labelled_citation": rate("has_labelled_citation"),
            "only_labelled_citations": rate("only_labelled_citations"),
            "all_labelled_sources_cited": rate("all_sources_cited"),
            "expected_facts_present": rate("facts_ok"),
            "prompt_injection_resisted": rate("injection_resisted"),
            "conflict_flagged": rate("conflict_ok"),
            "latency_seconds": {
                "median": round(statistics.median(r["latency_s"] for r in answered), 2),
                "max": max(r["latency_s"] for r in answered),
            } if answered else None,
        })
    return summary


def write(summary: dict, rows: list[dict], name: str = "latest.json") -> None:
    out = HERE / "results"
    out.mkdir(exist_ok=True)
    (out / name).write_text(json.dumps({"summary": summary, "rows": rows}, indent=2, default=str), encoding="utf-8")
    print("\nSUMMARY\n" + json.dumps(summary, indent=2))
    print(f"\nDetails: {out / name}")


def combine(runs: list[dict], questions: list[dict]) -> list[dict]:
    """The rows of several runs of one model as one run: every question once, in the order of its id.

    Per question the first answer without a model error is kept, in the order the runs are given; an
    error never replaces an answer. "Expected facts" is scored again from the stored answer with the
    current labels, so that all rows of the merged report are judged by one rule.
    """
    for key in ("generation_model", "embedding_model", "retrieval_k"):
        values = {run["summary"].get(key) for run in runs}
        if len(values) != 1:
            raise SystemExit(f"These runs differ in {key} ({', '.join(map(str, values))}) and cannot be merged into one benchmark.")
    rows: dict[str, dict] = {}
    for run in runs:
        for row in run["rows"]:
            kept = rows.get(row["id"])
            if kept is None or ("error" in kept and "error" not in row):
                rows[row["id"]] = dict(row)
    labels = {q["id"]: q for q in questions}
    for row in rows.values():
        # Result files written before the citation checks were named precisely
        if "citation_ok" in row:
            row["has_labelled_citation"] = row.pop("citation_ok")
        if "facts_ok" in row and "answer" in row and row["id"] in labels:
            row["facts_ok"] = all(has_fact(row["answer"], f) for f in labels[row["id"]].get("must_include", []))
    return sorted(rows.values(), key=lambda r: r["id"])


def merge(paths: list[str]) -> None:
    """One report (results/merged.json) from several runs, e.g. when a daily quota ended a run early."""
    runs = [json.loads(Path(p).read_text(encoding="utf-8")) for p in paths]
    questions = json.loads((HERE / "questions.json").read_text(encoding="utf-8"))
    rows = combine(runs, questions)
    first = runs[0]["summary"]
    summary = summarize(rows, first["embedding_model"], first["retrieval_k"], first.get("generation_model"))
    summary["merged_from"] = [Path(p).name for p in paths]
    missing = sorted({q["id"] for q in questions} - {r["id"] for r in rows})
    summary["questions_missing"] = missing
    summary["questions_with_model_error"] = [r["id"] for r in rows if "error" in r]
    write(summary, rows, "merged.json")


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Imported only here: importing the application before main() sets the environment
        # would connect it to the real database in .env instead of the in-memory one
        from backend.app.services.llm import LLMError

        if not isinstance(e, (LLMError, RuntimeError)):
            raise
        raise SystemExit(f"Evaluation stopped: {e}")
