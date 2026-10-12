# ContextBasedRAG

A maintenance assistant for small manufacturers. It answers questions from the factory's own
manuals, SOPs and breakdown records, shows the source of every statement, drafts work orders from
that evidence, and requires a manager's approval before a work order can be carried out.

## What works today

| Area | What it does |
|---|---|
| Factories and users | Each factory is its own workspace. Roles: viewer, technician, maintenance manager, administrator. |
| Assets | Create, search, edit and archive machines. Asset codes are unique inside a factory. |
| Documents | Upload PDF, DOCX, PPTX, TXT, MD. Files are validated, stored privately, chunked and indexed in the background. Statuses: queued, processing, ready, failed. Reprocess and delete. |
| Ask | Hybrid search (vectors + BM25) inside the user's own factory only. Answers cite numbered evidence; names, pages and record numbers in a citation come from stored data, not from the model. No evidence, or no valid citation, gives an explicit "not found" instead of an answer. |
| Breakdowns | Manual records and CSV/XLSX import with a per-row error report. Repeat-issue summary computed from the records, with the records that support each figure and the gaps (e.g. root cause not recorded). |
| Work orders | Drafts written by hand or generated from the asset's SOPs and history. Steps without a source, and steps touching safety, are flagged. `draft → pending_approval → approved → in_progress → completed`, plus rejected and cancelled, enforced by the backend. The author cannot approve their own work order unless `ALLOW_SELF_APPROVAL=true`. |
| Audit | Every create, edit, delete, import and transition (including refused ones) is recorded with who, when, what and a request id. |

## Not built yet

OCR for scanned documents, follow-up questions that remember the conversation, ERP/CMMS
integration, sensor data and anything predictive, production deployment with backups. The
system never controls a machine.

## Run it

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Fill in `GOOGLE_API_KEY` and `MONGO_URI` in `.env`, then:

```bash
uvicorn backend.app.main:app --port 8000
```

- Application: http://localhost:8000/app
- API reference: http://localhost:8000/docs
- Health: http://localhost:8000/health

Optional demo factory with invented sample data (server must be running):

```bash
python -m backend.scripts.seed_demo
```

Sign in as `admin@`, `manager@`, `technician@` or `viewer@demo-factory.example.com` with the
`DEMO_PASSWORD` from `.env`. The sample data in `data/sample/` is synthetic and must not be
presented as real factory records.

## Tests

```bash
python -m pytest backend/tests -q
```

The tests use an in-memory database, a temporary vector index and a fake model, so they need no
network, no database and no API quota. They cover login and roles, isolation between factories,
upload validation and failure handling, citation validation, imports, the approval rules and the
audit trail.

## Evaluation

```bash
python -m backend.eval.run_eval              # retrieval: Recall@1/3/6 (embedding calls only)
python -m backend.eval.run_eval --answers    # also citations, abstention, facts, latency
```

26 labelled questions in `backend/eval/questions.json` (direct, Hinglish, multi-source,
conflicting procedures, no answer, unknown asset, prompt injection, cross-factory). See
`docs/evaluation.md` for the current state of the measurements.

## Layout

```
backend/app/core        configuration, database, authentication and roles
backend/app/api         HTTP endpoints under /api/v1
backend/app/services    ingestion, retrieval, answering, factory context, work orders, audit
backend/tests           automated tests
backend/eval            labelled questions and the evaluation script
backend/scripts         sample data generator and demo seeding
frontend                landing page (index.html) and the application (app.html, js, css)
data/sample             synthetic sample dataset
```
