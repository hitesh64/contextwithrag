# Evaluation

## Status on 12 October 2026: first baseline measured

One run on the synthetic sample dataset (5 documents, 10 breakdown records, 26 labelled
questions), embedding model `gemini-embedding-001`, 6 passages retrieved per question.
This is a baseline on invented data, not evidence of accuracy on a real factory's records.

| Metric | Result | Questions |
|---|---|---|
| Recall@1 | 19 / 21 (90.5%) | 21 with labelled sources |
| Recall@3 | 21 / 21 | 21 |
| Recall@6 | 21 / 21 | 21 |
| Cross-factory retrieval blocked | 1 / 1 | 1 |
| Citation correct (every citation points at a labelled source) | 21 / 21 | 21 answered |
| All labelled sources cited | 20 / 21 | 21 |
| Expected facts present (keyword check) | 20 / 21 | 21 |
| Answers when an answer exists | 21 / 21 | 21 |
| Abstains when no answer exists | 5 / 5 | 4 no-answer / unknown-asset + 1 cross-factory |
| Prompt injection resisted | 1 / 1 | 1 |
| Latency, median / max | 2.1 s / 5.5 s (q01-q20), 3.4 s / 12.5 s (q21-q25) | 25 model calls |

### How the run was made

- Retrieval: all 26 questions in one run.
- Answers: the free key allows 20 generation requests a day per model, so the run was split:
  q01-q20 and q26 with `gemini-2.5-flash-lite`, q21-q25 with `gemini-2.5-flash`. The two
  parts are therefore not the same model, and the abstention and prompt-injection results
  come from the stronger one. Re-run all 26 on one model when quota allows.
- Each question was asked once. With 1 to 21 questions per metric, one different answer moves
  a figure by 5 to 100 points; none of these numbers is a stable percentage.

### What failed

- **q20 (conflicting procedures).** The press SOP and the general lockout SOP give different
  waiting times after opening the pressure release valve. The answer gave one of them
  ("10 minutes") with a valid citation and did not mention that the other document disagrees.
  For a safety step this is the most important finding of the run: the system does not yet
  surface conflicts between documents.
  **Changed the same day:** the model now reports a disagreement with a `CONFLICT` marker and
  the backend writes a fixed warning (each source with its value, "Status: Conflict unresolved."
  and an instruction to have a supervisor confirm); the chat response carries `conflict: true`.
  Re-check of q20 after the change: flagged correctly with `gemini-2.5-flash` (1 run, both
  sources listed). `gemini-2.5-flash-lite` found the conflict but wrote text before the marker;
  the parser was then made to accept that, which is covered by an automated test but could not
  be re-run on the real lite model because its daily quota was used up. One conflict question
  is not a measurement: add more conflict cases to `questions.json` before relying on this.
- **q12 and q20** found their labelled passage at rank 2 or 3, not rank 1.

### Reproduce

```bash
.venv\Scripts\python.exe -m backend.eval.run_eval
.venv\Scripts\python.exe -m backend.eval.run_eval --answers --delay 13
```

Per-question details of this run: `backend/eval/results/2026-10-12_*.json` (not in git).

## What the automated tests already establish

These hold regardless of the model, because the backend enforces them (42 tests, all passing):

- A user of one factory cannot read, cite, download, edit or delete another factory's assets,
  documents, breakdowns, work orders or audit events.
- A citation's file name, page, section and record number come from stored metadata. Citation
  numbers the model invents are removed.
- With no evidence the model is not called. An answer with no valid citation is replaced by an
  explicit "not found".
- A failed upload is never marked ready, and reprocessing never duplicates chunks.
- Work-order transitions follow the status table and the roles; refused attempts are audited.

## Limits of this evaluation

- The dataset is synthetic and small (5 documents, 10 breakdown records). Results on it say
  little about real manuals, which are longer, scanned, tabular and multilingual.
- "Expected facts present" is a keyword check, not a judgement of correctness.
- Thresholds should be set only after a baseline on real documents from a pilot factory.
