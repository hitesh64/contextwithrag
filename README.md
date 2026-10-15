# ContextBasedRAG

A maintenance assistant for small manufacturers. It answers questions from the factory's own
manuals, SOPs and breakdown records, shows the source of every statement, drafts work orders from
that evidence, and requires a manager's approval before a work order can be carried out.

## What works today

| Area | What it does |
|---|---|
| Factories and users | Each factory is its own workspace. Roles: viewer, technician, maintenance manager, administrator. A role gives a standard set of access; under Users → Access the administrator can choose for one user which sections are visible and what that user may do (for example who may approve work orders or close conflicts). The backend enforces the same list, so a hidden section is also refused by the API. Managing users stays with the administrator. |
| Assets | Create, search, edit and archive machines. Asset codes are unique inside a factory. |
| Documents | Upload PDF, DOCX, PPTX, XLSX, CSV, TXT, MD. An Excel or CSV file is read row by row: every row is written out with its column names and cited by sheet and row numbers. Files are validated, stored privately, chunked and indexed in the background. Statuses: queued, processing, ready, failed. Reprocess and delete. |
| Ask | Hybrid search (vectors + BM25) inside the user's own factory only. Answers cite numbered evidence; names, pages and record numbers in a citation come from stored data, not from the model. No evidence, or no valid citation, gives an explicit "not found" instead of an answer. |
| Conflicts | When two documents give different values for the same instruction (10 minutes in the press SOP, 5 in the general lockout SOP), the backend reports both and picks neither; the model is not asked. Conflicts are listed on their own page. A maintenance manager or administrator records the decision with a reason; a change to either document reopens it. A document counts as superseded only when a manager records that. |
| Breakdowns | Manual records and CSV/XLSX import with a per-row error report. Repeat-issue summary computed from the records, with the records that support each figure and the gaps (e.g. root cause not recorded). |
| Work orders | Drafts written by hand or generated from the asset's SOPs and history. Steps without a source, and steps touching safety, are flagged. `draft → pending_approval → approved → in_progress → completed`, plus rejected and cancelled, enforced by the backend. The author cannot approve their own work order, except an administrator, a user the administrator has given that access, or everyone when `ALLOW_SELF_APPROVAL=true`; such an approval is marked in the audit history. |
| Export | Assets, breakdowns (with the filters of the list) and work orders download as Excel files. |
| Audit | Every create, edit, delete, import, export and transition (including refused ones) is recorded with who, when, what and a request id. |

## Not built yet

OCR for scanned documents, follow-up questions that remember the conversation, ERP/CMMS
integration, sensor data and anything predictive, production deployment with backups (a
demonstration deployment is prepared, see Deployment). The
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

- Application: http://localhost:8000
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
upload validation and failure handling, citation validation, conflict detection and who may close
a conflict, imports, the approval rules, the audit trail, and the evaluation's own scoring. One test
runs `node --test frontend/tests/latest.test.js` (the page shown is the page the user is on, however slowly an
earlier page answers) and is skipped if Node.js is not installed.

## Evaluation

```bash
python -m backend.eval.run_eval              # retrieval: labelled sources in the top 1/3/6 (embedding calls only)
python -m backend.eval.run_eval --answers    # also citations, abstention, facts, latency
python -m backend.eval.run_eval --merge a.json b.json    # one report from runs split by the daily quota
python -m backend.eval.run_conflict_eval --fake-embeddings    # conflict detection alone; needs no key
```

26 labelled questions in `backend/eval/questions.json` (direct, Hinglish, multi-source,
conflicting procedures, no answer, unknown asset, prompt injection, cross-factory). See
`docs/evaluation.md` for the current state of the measurements.

## Deployment

A demonstration runs on Render's free plan at https://contextwithrag.onrender.com (see
`render.yaml` and `docs/deployment.md` for what was and was not checked there). That plan
empties the disk on every restart, so uploads are also kept in MongoDB (`FILE_STORE=database`) and
indexed again at start-up (`REINDEX_ON_START=true`).

## Sharing the project

Do not zip the folder: `.env` (API key, database password), `.venv`, `storage/` and `chroma_data/`
would go with it, because `.gitignore` only applies to git. Export what is committed instead:

```bash
git archive --format=zip -o ../ContextBasedRAG.zip HEAD
```

## Layout

```
backend/app/core        configuration, database, authentication and roles
backend/app/api         HTTP endpoints under /api/v1
backend/app/services    ingestion, retrieval, answering, factory context, work orders, audit
backend/tests           automated tests
backend/eval            labelled questions and the evaluation script
backend/scripts         sample data generator and demo seeding
frontend                the application (app.html, js, css, img), served at /
frontend/tests          browser-free test of the page-drawing helper (Node.js)
data/sample             synthetic sample dataset
data/conflict_eval      labelled corpus for the conflict-detection evaluation
docs                    design, deployment and evaluation notes
```
