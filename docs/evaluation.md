# Evaluation

Two separate measurements, which must not be mixed:

1. **The conflict detector** (below, "Conflict detection"). Deterministic, no model, so it can be
   re-run at any time without quota.
2. **The whole assistant** (retrieval + Gemini answers; the sections after it). Needs generation
   quota, and its numbers are from one run per question on one small synthetic dataset.

## Conflict detection, 12 October 2026

22 labelled cases on a second synthetic corpus (26 documents, `data/conflict_eval/`) plus the 25
own-organization questions of the main set as a regression check. The detector compares the
retrieved passages itself; no answer is generated.

```bash
.venv\Scripts\python.exe -m backend.eval.run_conflict_eval                     # real embeddings
.venv\Scripts\python.exe -m backend.eval.run_conflict_eval --fake-embeddings   # no quota at all
```

| Metric | Real embeddings | Fake embeddings | Cases |
|---|---|---|---|
| Conflicts found (two-way, three-way, paraphrased, unit-converted, conditions) | 11 / 11 | 11 / 11 | 11 |
| False alarms (unrelated dimension, other machines, equal values, unrelated procedure, condition stated in the question) | 0 / 10 | 0 / 10 | 10 |
| Old revision reported as superseded, and only on explicit metadata | 2 / 2 | 2 / 2 | 2 |
| Labelled questions of the main set unchanged (q20 flagged, nothing else) | 25 / 25 | 25 / 25 | 25 |
| Word-only disagreement found (outside what the detector compares) | 0 / 1 | 0 / 1 | 1 |

**These numbers are fitted, not an independent measurement.** The cases and their expected results
were written before the first run, but the detector was then changed until they passed, so the only
honest reading is "it handles the 22 situations we thought of". The first run scored 5/11 recall and
3/10 false alarms; what the failures showed, and what was changed:

- `every 500 operating hours` was not read at all: the quantity had to be next to its unit. A
  quantity may now be up to two words from its unit — which first introduced a worse bug, reading
  `wait 10 minutes until` as 10 litres, because the pattern split the word "until".
- `degrees` and `C` counted as part of what a sentence was about, so a temperature disagreement
  looked off-topic. Words belonging to the unit are now excluded.
- Unrelated procedures were compared because they shared only generic verbs: a dryer cover and a
  gearbox drain plug both "wait" and "open". Those verbs no longer make two sentences the same
  instruction, and one shared word is enough only when it is the whole subject of the shorter one.
- A question about an air filter was answered with a conflict about running the compressor before
  shutdown. What two sources disagree about must now be mostly what the question asked about.
- A question about cooling a furnace named an old pump revision, because that revision also
  mentions cooling. An old revision is now named only where it answers the same question.

What this measurement does not cover: real manuals (these are short, clean, invented text), tables
and scanned pages, Hindi or Marathi quantities, disagreements stated in words rather than numbers
(1 case, found by neither configuration), and thresholds, which are still guesses — `ON_TOPIC = 0.6`
rests on a single failing case. The detector's own logic is also covered by 17 automated tests in
`backend/tests/test_conflict_detection.py`, which need no model and no quota.

Per-case detail of the real-embedding run: `backend/eval/results/2026-10-12_conflict-detector_real-embeddings.json` (results are not in git; re-run the command above to regenerate).

## The whole assistant on one model: started 12 October 2026, not finished

The run below was meant to replace the split-model baseline further down with all 26 questions
on `gemini-2.5-flash`. The key's daily generation quota ended it early, so it is **incomplete**:

| | Result |
|---|---|
| Retrieval (all 26, no generation needed): Recall@1 / @3 / @6 | 19 / 21, 21 / 21, 21 / 21 |
| Cross-factory retrieval blocked | 1 / 1 |
| Questions answered | 10 of 26 (8 by the model; q20 and q26 need no model call) |
| Stopped by quota (HTTP 429) | 16: q06, q08, q10, q12-q19, q21-q25 |
| Of the 9 answered questions with labelled sources: citation correct, all sources cited | 9 / 9, 9 / 9 |
| Expected facts present | 9 / 9 (8 / 9 under the first, cruder check; see below) |
| Conflict flagged (q20, by the backend, no model call) | 1 / 1 |
| Abstention, prompt injection | not measured: q21-q25 never ran |

**Why it stopped.** Google's error names the limit: `GenerateRequestsPerDayPerProjectPerModel-FreeTier`,
20 requests a day per project and model. Of 26 questions 24 need a model call (q20 and q26 do not),
so one free project cannot finish this benchmark on one model in one day, whatever the key. A new
key of the same project shares the limit; it resets about 14 hours after the run (early morning IST).

**The facts check was wrong for q05, and is changed.** The answer said the spindle temperature "has
exceeded 70 degrees C", with the right citation; the label asked for the word "overheat". A label
may now list several wordings of one fact, and a number must stand alone, so "exceeded 80 degrees"
or "170" does not pass as "70" (before, "5" was found inside "15"). The stricter number rule
applies to every question; the nine answers of this run pass it. Rows are scored again with the
current labels when runs are merged.

Nothing about abstention or prompt-injection resistance can be claimed from this run. To finish
it, run the 16 missing questions on the same model after the quota resets, without changing the
answering code in between, and merge:

```bash
.venv\Scripts\python.exe -m backend.eval.run_eval --answers --delay 13 --model gemini-2.5-flash --only q06,q08,q10,q12,q13,q14,q15,q16,q17,q18,q19,q21,q22,q23,q24,q25
.venv\Scripts\python.exe -m backend.eval.run_eval --merge backend/eval/results/2026-10-12_flash_single-model_partial.json backend/eval/results/latest.json
```

The merge writes `results/merged.json`. It keeps each question once, never lets a quota error
replace an answer, lists `questions_missing` and `questions_with_model_error`, and refuses runs
that differ in generation model, embedding model or retrieval depth (5 tests in
`backend/tests/test_eval_tools.py`). The benchmark is complete only when both lists are empty.

## The whole assistant: status on 12 October 2026, first baseline measured (two models)

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

These hold regardless of the model, because the backend enforces them (64 tests, all passing):

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
