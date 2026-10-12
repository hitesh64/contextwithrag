# Conflict detection: design (not yet implemented)

## Why

Today a conflict between two documents is noticed only if the model writes the `CONFLICT`
marker (`answering.py`). The backend then renders a fixed warning, but it never looks for a
conflict itself. If the model answers with one value (as it did for q20 before the prompt
change) the user never learns that another document says something else. For safety steps
(waiting times, pressures, torques) that is the failure to remove.

Goal: the backend compares the retrieved evidence itself. The model may add a flag, but it can
no longer remove one. Nothing is ever resolved automatically.

## What the system knows today (and does not)

| Needed to compare | Available now |
|---|---|
| Which machine a document is about | Yes: `asset_ids` on the document; empty means "applies to all" |
| Document type (manual, SOP, ...) | Yes: `doc_type` |
| Page / section of a passage | Yes |
| Revision, effective date, current / superseded | **No.** Only free text inside the file ("Revision 1, effective 10 January 2024") |
| Operating condition of an instruction | **No.** Only free text in the sentence |

So version-aware comparison needs a small data-model addition (below). Without it the
detector can still do scope and value comparison, and says so.

## Pipeline

Runs in `gather_evidence` output, before the model's answer is trusted.

1. **Extract claims.** Split each document passage into sentences. A claim is a sentence with a
   number plus a unit from a fixed list: time (s, min, h, day, week, month), pressure (bar, psi,
   kPa, MPa), torque (Nm), temperature (°C), length (mm, m), volume (l, ml). Units are
   normalised to one base unit per dimension ("1 hour" = 60 min). Breakdown records are
   history, not procedure, and are not compared.
2. **Pick claims relevant to the question.** Keep a claim only if its sentence shares enough
   content words with the question (stop words removed). This keeps unrelated numbers in the
   same passage from raising alarms.
3. **Pair claims from different sources** (different document, or two revisions of one
   document) with the same dimension and a high word overlap between the two sentences
   (the "same thing" test, e.g. "open the pressure release valve and wait").
4. **Compare scope.** Two documents are comparable when their asset sets overlap, or one is
   general (empty set). Documents for two different specific machines are never compared
   (CNC-01 vs COMP-03). A general document against a machine-specific one *is* compared; the
   system does not decide that the specific one wins, a person does.
5. **Compare values** after normalisation, with a small tolerance (rounding, "about").
6. **Classify each pair:**

| Outcome | Condition | What the user sees |
|---|---|---|
| `none` | no comparable pair, or values equal | normal answer |
| `conflict` | scope overlaps, same dimension, strong sentence match, values differ, no differing qualifier, both sources current or version unknown | fixed warning, both sources with their exact values, "Status: Conflict unresolved." |
| `needs_review` | a pair looks related but is uncertain: medium sentence match, different qualifiers (see below), missing version info where documents look like revisions of each other | fixed notice: "These sources may disagree; a supervisor should check", values shown, no claim that it is a confirmed conflict |
| `superseded` | one source is marked superseded | normal answer from the current source, with a note naming the superseded one |

**Qualifiers** that turn a `conflict` into `needs_review`: different condition words in the
two sentences ("hydraulic" vs "pneumatic", "hot" vs "cold", "when", "if", "unless", "for
<model number>", "ISO VG 32" vs "ISO VG 46"). Better a review notice than a false conflict,
and better a review notice than silence.

7. **Merge with the model.** `conflict` / `needs_review` from the backend always wins over an
   ordinary answer. If the model also wrote `CONFLICT`, the two are merged (the backend list of
   claims is used for the text, the model's list is only a fallback). The model's wording never
   replaces the backend's values.

When the outcome is `conflict`, the chat response sets `conflict: true`; for `needs_review`
it sets `review_required: true`. Both come with the list of sources. Either is also recorded
(next section).

## Human resolution

Only a person with the supervisor or admin role may close a conflict. New collection
`conflicts` (every record carries `organization_id`, as everywhere):

`{ organization_id, status: open | resolved | dismissed, kind: conflict | needs_review,
topic, claims[{document_id, page, section, value, unit, sentence}], first_seen_at,
resolved_by, resolved_at, decision: "document <id> governs" | "both apply, conditions: ..." |
"document <id> is outdated" , note }`

- Detected conflicts are de-duplicated by (topic, document pair) and listed for reviewers.
- Resolving writes an audit event (existing audit service) and requires a note.
- A resolved conflict does not silence the warning for operators. The answer shows the
  approved decision with who approved it and when, next to both original sources. If a
  document changes after the decision (re-upload, new revision), the record reopens.

## Data-model additions

Optional fields on a document, set at upload or later: `revision` (string),
`effective_date`, `status` (`current` default, `superseded`), `supersedes_document_id`.
Absent fields mean "unknown", never "current and approved".

## Error budget and what could still go wrong

- The extractor reads numbers with units only. A conflict stated in words ("lock the
  isolator" vs "do not lock") is not found by this layer; the model's `CONFLICT` marker is the
  only net for that.
- Tables and scanned pages flatten badly in extraction; claims inside them may be missed or
  mis-paired.
- Hindi/Marathi documents: numbers and units in Devanagari are not handled in v1.
- Thresholds (sentence match, tolerance) are guesses until measured. They go in config, and
  the evaluation below sets them; they are not tuned on the sample set alone.

## Tests (written before the thresholds are fixed)

Automated, no model needed (the detector is deterministic):

1. Two-way conflict: q20 sample (10 min vs 5 min, press SOP vs general lockout SOP) -> `conflict`.
2. Three-way conflict: three documents, three values -> `conflict` listing all three.
3. Old vs new revision: same document family, one `superseded` -> `superseded`, no conflict.
4. Same two revisions, no version metadata -> `needs_review`.
5. Different machines (CNC-01 vs COMP-03) with different values -> `none`.
6. Different conditions ("hydraulic: 5 min", "pneumatic: vent the line") -> `none`;
   "hot oil: 10 min" vs "cold oil: 5 min" -> `needs_review`.
7. Equal values in different units (1 h vs 60 min) -> `none`.
8. Unrelated number in a retrieved passage (page number, part number) -> `none`.
9. Another organization's document with a different value is never compared (isolation).
10. Model answers a single value, never writes `CONFLICT` -> response is still flagged.
11. Model writes `CONFLICT` but backend finds none -> existing behaviour kept (needs two real sources).
12. Reviewer role can resolve; operator role gets 403; refused attempt is audited.

Model evaluation (needs quota, run once on one model with one configuration): add to
`questions.json` the same cases as labelled questions, plus at least 5 false-conflict
questions (different machines, different conditions, equal values) so false alarms are
measured as well as misses. Report conflict recall and false-alarm rate separately.

## Build order

1. Data fields + extractor + comparator + tests 1-9 (no API, no model).
2. Wire into `answering.answer` + response fields + tests 10-11.
3. `conflicts` collection, reviewer endpoints, audit, test 12.
4. Evaluation questions and one same-model run.

## Decisions needed before step 1

- Should a general-vs-specific disagreement (the q20 case) always be `conflict`, or `needs_review`?
  This design says `conflict`: the stricter safety value is waiting for the supervisor.
- Which roles may resolve: supervisor and admin only, or admin only?
- Does a confirmed `conflict` skip the model call entirely (cheaper, fully deterministic) or
  does the model still write the answer text? This design: the backend report is the answer.
