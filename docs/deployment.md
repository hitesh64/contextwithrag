# Deployment on Render (free plan)

**Status, 13 October 2026: deployed.** `https://contextwithrag.onrender.com` runs this application
since `main` was merged at `33048fd`; the build took about five minutes. Checked from outside,
without signing in: `/health` answers `ok`, the address serves the sign-in page, the API lists 32 paths including the conflict endpoints, and `/api/v1/documents` and
`/api/v1/conflicts` refuse a request without a login (401).

**Not checked yet on the deployed service:** registering and signing in, uploading and indexing a
document, an answer from the model, that `MONGO_DB` is `contextbasedrag` and not the banking
database, and above all the restart test in step 5 below. Memory use on the 512 MB plan is unknown.
The storage behaviour itself is covered by tests in `backend/tests/test_deployment_storage.py`.

## What is different on a free cloud plan

| Local | Render free plan | What the app does about it |
|---|---|---|
| Uploaded files stay in `storage/` | The disk is emptied on every restart, and the service restarts whenever it wakes from sleep (after about 15 idle minutes) | `FILE_STORE=database` keeps a copy of every upload in MongoDB (`stored_files`) and puts it back on disk when it is needed |
| The vector index stays in `chroma_data/` | Lost with the disk | `REINDEX_ON_START=true` indexes every "ready" document again in the background when the server starts |
| One user | Anyone with the address | Sign-in is required for everything except the sign-in page itself and `/health`; anyone can still register a factory of their own |

Consequences to expect, none of them measured yet:

- The first request after sleep waits for the server to start (about a minute), and search finds
  nothing until re-indexing has finished. With the five sample documents that is seconds; with a
  real library it is minutes and embedding calls at every wake-up.
- A file kept in MongoDB must fit in one record, so uploads are limited to 15 MB in this mode. The
  free Atlas tier holds 512 MB in total.
- If re-indexing meets the embedding quota, the affected documents become "failed" and need
  Reprocess. Documents uploaded before `FILE_STORE=database` was set have no copy and become
  "failed" with "The original file is no longer in storage".
- 512 MB of memory for ChromaDB and PDF parsing together is untested.
- The generation limit is 20 requests a day per Google project and model on a free key. A deployed
  app and a benchmark that share a project share that limit. Use a key of a separate project here.

This is enough for a demonstration. It is not a production setup: no backups, no persistent disk,
no monitoring. A paid disk (mount it and point `CHROMA_DIR` and `STORAGE_DIR` at it, with
`FILE_STORE=disk` and `REINDEX_ON_START=false`) removes the re-indexing.

## Before deploying

1. Rotate the credentials that were in the shared ZIP: Gemini key, MongoDB password, demo password.
2. MongoDB Atlas, Network Access: Render's free plan has no fixed address, so `0.0.0.0/0` is
   needed there. The database password is then the only protection: make it long and random.
3. Decide what happens to the banking version. Deploying this replaces it at the same address. Its
   data (database `nexus_ai`) is not touched and not read: this app uses `contextbasedrag`.

## Deploying

The service deploys from `main` automatically. The new application is on `factory-rebuild`.

1. In the Render dashboard, set the environment of the service to what `render.yaml` lists
   (an existing service does not pick up new variables from the file by itself): `MONGO_DB`,
   `FILE_STORE`, `REINDEX_ON_START`, `GEMINI_BACKUP_MODEL`, and the new `GOOGLE_API_KEY` and
   `MONGO_URI`. (`DEMO_PASSWORD` is not needed on the server: the seeding script reads it on the
   machine it is run from.) Change the start command to
   `uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT` and the health check path to `/health`.
2. Merge `factory-rebuild` into `main` and push. Render builds and starts it.
3. Check `https://<address>/health` (`"status": "ok"`), then open `https://<address>`.
4. Optional sample factory, from your own machine; the four demo users get the `DEMO_PASSWORD` of
   your own `.env`:

   ```bash
   .venv\Scripts\python.exe -m backend.scripts.seed_demo https://<address>
   ```

5. Ask the two questions of the demo (alarm E-204; waiting time after the pressure release valve).
   Then restart the service from the dashboard and ask again after a minute: the documents must
   still be "ready" and both answers must come back. That restart is the real test of this page.

## Registration fee, mail and logo

A new company pays `REGISTRATION_FEE` (₹2999) by UPI before it can use the application. Set in the
Render dashboard:

- `UPI_ID` and `UPI_PAYEE_NAME`: where the money goes; the QR code is made from them.
- `PLATFORM_OWNER_EMAIL`: the account that sees the **Payments** page and reviews the payments the AI
  check could not confirm. That account's own company never pays.
- `SMTP_USER` (the Gmail address) and `SMTP_PASSWORD` (a Gmail **app password**), and `APP_BASE_URL`
  (`https://<address>`), for the "your company is registered" mail.

The check reads the payer's screenshot and rejects a wrong or reused proof by itself. It cannot see
the bank account and a made-up screenshot can pass it, so no payment is accepted automatically: the
owner finds the UTR in the bank or UPI app and accepts it. The owner's mail for each waiting payment has
the screenshot attached and Accept / Reject buttons; each opens a page where one more click decides
(mail scanners open links by themselves, so opening a link changes nothing). A link works once, for 7
days. The Payments page does the same. Rejecting an accepted payment locks that company again. Each proof costs one Gemini call (free key: ~20 a day).

Render's support has said outgoing SMTP ports are blocked on its services. If the log shows
`Mail to … could not be sent`, mail works only from a machine that allows SMTP, or through an
HTTP mail API (not built yet). Registration and payment keep working without mail.

Companies created before the fee existed have no status and stay active.

## Going back

Revert the merge on `main` and push; set the start command back to
`uvicorn backend.main:app --host 0.0.0.0 --port $PORT`, the health check to `/api/health` and
`MONGO_DB` to `nexus_ai`. The banking version is `main` at `32f6db1` on GitHub as long as nothing
is merged into it.
