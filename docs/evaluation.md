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
(1 case, found by neither configuration), a conflicting document that retrieval did not bring into
the six passages (the detector compares only what was retrieved), questions whose wording matches
none of the cues for the kind of quantity asked (then every kind is compared), and thresholds,
which are still guesses — `ON_TOPIC = 0.6`
rests on a single failing case. The detector's own logic is also covered by 18 automated tests in
`backend/tests/test_conflict_detection.py`, which need no model and no quota.

Per-case detail of the real-embedding run: `backend/eval/results/2026-10-12_conflict-detector_real-embeddings.json` (results are not in git; re-run the command above to regenerate).

## What the retrieval and citation figures mean

Two figures in this document were first reported under names that claimed more than was measured.
The numbers are unchanged; the names now say what they are.

- *Questions with all labelled sources in the top k* is counted per question and is stricter than
  recall: a question with two labelled sources counts only if both are found. It was called
  "Recall@k". *Source recall at k* is recall in the usual sense, summed over all questions:
  `labelled sources found in the first k passages / labelled sources`. The 25 in "23 / 25" are
  labelled sources (18 questions have one, 2 have two, 1 has three), not questions, so this is not
  a hit rate.
- *At least one cited source is a labelled one* was called "citation correct" and described as
  "every citation points at a labelled source", which it never checked: an answer citing one right
  and one unrelated source passed. The evaluation now reports three separate checks: at least one
  labelled source cited, only labelled sources cited, all labelled sources cited. "Only labelled
  sources cited" exists for runs made after this change; earlier result files did not store which
  sources were cited, so for them it is absent, not assumed. A citation of a relevant passage that
  nobody labelled fails that check, so it measures agreement with the labels, not correctness.

## The whole assistant on one model: started 12 October 2026, not finished

The run below was meant to replace the split-model baseline further down with all 26 questions
on `gemini-2.5-flash`. The key's daily generation quota ended it early, so it is **incomplete**:

| | Result |
|---|---|
| Questions with all their labelled sources in the top 1 / 3 / 6 passages | 19 / 21, 21 / 21, 21 / 21 |
| Source recall at 1 / 3 / 6 (labelled sources retrieved / labelled sources) | 23 / 25, 25 / 25, 25 / 25 |
| Cross-factory retrieval blocked | 1 / 1 |
| Questions answered | 16 of 26 after two days (10 on 12 October, 6 on 13 October; q20 and q26 need no model call) |
| Still stopped by quota (HTTP 429) | 10: q10, q12, q14, q16-q19, q23-q25 |
| Of the 13 answered questions with labelled sources: at least one labelled source cited, all labelled sources cited | 13 / 13, 13 / 13 |
| Only labelled sources cited (stored only for the 4 such answers of 13 October) | 4 / 4 |
| Expected facts present | 13 / 13 (q05 failed the first, cruder check; see below) |
| Conflict flagged (q20, by the backend, no model call) | 1 / 1 |
| Abstains when no answer exists | 3 / 3 so far (q21, q22, q26); q23 and q24 not run |
| Prompt injection | not measured: q25 has not run |

**Why it stopped.** Google's error names the limit: `GenerateRequestsPerDayPerProjectPerModel-FreeTier`,
20 requests a day per project and model. Of 26 questions 24 need a model call (q20 and q26 do not),
so one free project cannot finish this benchmark on one model in one day, whatever the key. A new
key of the same project shares the limit. Google's documentation says daily quotas reset at
midnight Pacific time, which is 12:30 IST until 1 November 2026 and 13:30 IST after it. (The error
itself said "retry in 14h17m" at about 15:10 IST, which would be 05:30 IST; the documented time is
the one to plan with.) Check the rate-limit page of AI Studio before the next run; a run that
meets the limit costs nothing and can be repeated.

**The facts check was wrong for q05, and is changed.** The answer said the spindle temperature "has
exceeded 70 degrees C", with the right citation; the label asked for the word "overheat". A label
may now list several wordings of one fact, and a number must stand alone, so "exceeded 80 degrees"
or "170" does not pass as "70" (before, "5" was found inside "15"). The stricter number rule
applies to every question; the nine answers of this run pass it. Rows are scored again with the
current labels when runs are merged.

Nothing about prompt-injection resistance can be claimed yet, and abstention rests on three
questions. On 13 October only 6 of the 16 open questions were answered: 4 at 08:47 IST and 2 at
about 11:27 IST. Two more resumes (11:33 and 11:37 IST) answered none.

**Which limit it is, from Google's own error text** (now written to the server log by
`services/llm.py`; all 10 refusals of the 11:37 run read the same):

```
Quota exceeded for metric: generativelanguage.googleapis.com/generate_content_free_tier_requests, limit: 20, model: gemini-2.5-flash
Please retry in 17h52m51s.        (at 11:37 IST, i.e. 05:30 IST = 00:00 UTC)
```

So it is the requests-per-day limit of the project for this model, not a per-minute or token
limit, and the retry time has pointed at 05:30 IST on three occasions, not at midnight Pacific
(12:30 IST) as the documentation says. Single requests were still answered while the limit was
being reported (two one-word test requests at 11:24 and 11:36 IST, and the two benchmark answers
at 11:27), so the refusal is not strict; that does not show a rolling window, and an earlier note
here that suggested one was a guess the error text does not support.

**The project's own requests account for the limit if the day starts at 12:30 IST**, as documented.
Answers recorded in `backend/eval/results/` on `gemini-2.5-flash` after 12:30 IST on 12 October: 5
(12:42), up to 4 (conflict check, 12:56), 10 less the two that need no model call (15:06), which is
16 to 17; the 4 of 08:47 IST on 13 October make 20 to 21, and that run was refused from its fifth
question on. `gemini-2.5-flash-lite` answered its 20 at 12:40 IST on 12 October and was refused on
the morning of the 13th. So no other user of the key is needed to explain the refusals, and the
"retry in" time of the error (05:30 IST) is then simply wrong. This is a tally from file times, not
a reading of Google's counter: the usage page of the project in AI Studio
(https://ai.dev/rate-limit) has not been compared, and a run after 12:30 IST on 13 October will
show which reset time is the real one.

The `source_recall_at_k` of `merged.json` counts only the rows that
stored per-source results (4 questions so far); the retrieval figures above are from the
retrieval-only run of all 26. Not measured at all with the real model yet: a work-order draft
generated from evidence (it is not one of the 26 questions; record it separately). To finish, repeat
this after the reset, one run at a time, without
changing the answering code in between. It asks only what is still unanswered and merges:

```bash
.venv\Scripts\python.exe -m backend.eval.run_eval --resume backend/eval/results/merged.json --delay 13
```

The merge writes `results/merged.json`. It keeps each question once, never lets a quota error
replace an answer, lists `questions_missing` and `questions_with_model_error`, and refuses runs
that differ in generation model, embedding model or retrieval depth. Every answer is written to
`results/in_progress.json` as it arrives and picked up by the next `--resume`, so a run that is cut
off does not lose the requests it spent (tests in
`backend/tests/test_eval_tools.py`). It prints COMPLETE, and sets `complete: true`, only when all
26 questions are present once and both lists are empty.

## The whole assistant: status on 12 October 2026, first baseline measured (two models)

One run on the synthetic sample dataset (5 documents, 10 breakdown records, 26 labelled
questions), embedding model `gemini-embedding-001`, 6 passages retrieved per question.
This is a baseline on invented data, not evidence of accuracy on a real factory's records.

| Metric | Result | Questions |
|---|---|---|
| Questions with all labelled sources in the top 1 passage | 19 / 21 (90.5%) | 21 with labelled sources |
| ... in the top 3 | 21 / 21 | 21 |
| ... in the top 6 | 21 / 21 | 21 |
| Cross-factory retrieval blocked | 1 / 1 | 1 |
| At least one cited source is a labelled one | 21 / 21 | 21 answered |
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

These hold regardless of the model, because the backend enforces them (76 tests, all passing; one of them runs the frontend's
page-drawing tests in Node.js and is skipped where Node.js is not installed):

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
