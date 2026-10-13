# Conflict detection: design and status

**Status (12 October 2026):** all four build steps are done. Measured results and the failures that
changed the design are in `docs/evaluation.md` ("Conflict detection"); the rules below reflect what
that evaluation forced, in particular that generic verbs ("wait", "open") do not make two sentences
the same instruction and that a disagreement must be about what the question asked.

Build steps 1-3 are implemented and tested (`services/conflicts.py`,
`services/conflict_service.py`, `api/conflicts.py`, `PATCH /documents/{id}/version`, 18 tests in
`backend/tests/test_conflict_detection.py`). Step 4 is done: 22 labelled cases
(`backend/eval/conflict_cases.json`, corpus in `data/conflict_eval/`) run by
`backend.eval.run_conflict_eval`, with conflict recall and false-alarm rate reported separately and
the 25 labelled questions of the main set as a regression check. The results are fitted to those
cases, because the detector was changed until they passed.

Differences between this design and the code: a claim must also be about the kind of quantity the
question asks for (a pressure question ignores waiting times), and share at least 2-3 words with the
question. Without those two filters a pressure question about the compressor was flagged because of
the press/lockout waiting times.

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
   number plus a unit from a fixed list (the table `UNITS` in `services/conflicts.py` is the
   authority): time (seconds, minutes, hours, days, weeks), pressure (bar, psi, kPa, MPa), torque
   (Nm), temperature (degrees C), length (mm, cm, metres written out), volume (ml, litres), speed
   (rpm), mass (kg). Not read: months and years (no fixed length), a bare "m" or "s" (too easily a
   word), degrees F, and number words other than one to twenty and the tens up to ninety. Units are
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

## Decisions (confirmed 12 October 2026)

1. **General vs machine-specific disagreement is a `conflict`.** The backend never makes one
   source the winner. When applicability or conditions are unclear the outcome is `needs_review`,
   never a confirmed conflict.
2. **Resolution: supervisor and admin.** In this code base "supervisor" is the existing role
   `maintenance_manager` (roles: viewer < technician < maintenance_manager < admin). Operators
   (technician, viewer) can see conflicts, not resolve or override them. A stricter company
   policy is one setting: `CONFLICT_RESOLVE_ROLE=admin`. Every resolution stores approver,
   timestamp, decision, note and the source documents, and writes an audit event; a refused
   attempt is audited as `denied`.
3. **A confirmed `conflict` and a `needs_review` are answered by the backend alone.** The model
   is not called and cannot rewrite the report. The report gives values, units, document names,
   the sentence each value comes from, revision information, the differing conditions and the
   unresolved status. A `needs_review` is never shown as a final fact.

Implementation rules that follow from these:

- **`superseded` needs proof.** A document counts as superseded only if a manager marked it
  `lifecycle = superseded`, or another document names it in `supersedes_document_id`. Never from
  a file name, an upload date or from which value looks newer. Missing revision metadata stays
  "unknown", and unknown is never "current and approved".
- Because of that rule, two documents without version metadata that disagree are a `conflict`
  (not a guess that one is old). The report then adds a note that revision information is
  missing. This replaces the earlier idea of downgrading such pairs to `needs_review`.
- **Qualifiers.** The conditions lexicon is small and fixed (hydraulic / pneumatic / electric,
  hot / warm / cold, loaded / unloaded / empty / full, summer / winter). A claim whose qualifier
  contradicts one the question itself states is not compared (asking about a hydraulic machine
  ignores a pneumatic-only sentence). Opposed qualifiers, or a qualifier that the other source
  never mentions and the question does not state, give `needs_review`.
- **Ranges.** "5-10 minutes" is compared as a range; different but overlapping ranges are
  `needs_review`.
- Two passages of the same document are never compared with each other in v1.
- A resolved conflict shows the recorded decision to everyone; it reopens when any involved
  document's version metadata changes or the document is replaced.

## Changes to the plan above

- Test 4 now expects `conflict` (with the missing-revision note), not `needs_review`.
- Test 10 becomes "the model is not called and the response is flagged".
