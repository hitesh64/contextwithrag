"""Deterministic comparison of the numeric instructions in the evidence of one question.

No model is involved. Every sentence of a retrieved document passage that states a quantity with a
unit ("wait 10 minutes", "180 bar") is a claim. Claims of different documents that are about the same
thing but give different values are reported, never settled: nothing here decides which source is right.

Outcomes: "conflict" (comparable instructions that disagree), "needs_review" (they may disagree but the
applicability is unclear) or nothing. Design and limits: docs/conflict-detection-design.md.
"""
import hashlib
import re

from ..core.config import settings
from .keyword_search import STOPWORDS

CONFLICT = "conflict"
NEEDS_REVIEW = "needs_review"

# Written by the backend, never by a model
CONFLICT_STATUS = "Status: Conflict unresolved."
CONFLICT_ACTION = (
    "Recommended action: Do not assume that either of these is the correct one. Have a qualified maintenance "
    "or safety supervisor confirm the approved, current procedure before proceeding."
)
REVIEW_STATUS = "Status: Review needed. These sources may disagree, but it is not clear that they apply to the same situation."
REVIEW_ACTION = (
    "Recommended action: Do not treat any of these values as the answer. Have a qualified maintenance or safety "
    "supervisor confirm which one applies before proceeding."
)

# alias -> (dimension, factor to the dimension's base unit, label shown)
UNITS: dict[str, tuple[str, float, str]] = {}


def _add(dimension: str, label: str, factor: float, aliases: list[str]) -> None:
    for alias in aliases:
        UNITS[alias] = (dimension, factor, label)


# Base units: minute, bar, N·m, degree C, mm, litre
_add("time", "seconds", 1 / 60, ["sec", "secs", "second", "seconds"])
_add("time", "minutes", 1, ["min", "mins", "minute", "minutes"])
_add("time", "hours", 60, ["h", "hr", "hrs", "hour", "hours"])
_add("time", "days", 1440, ["day", "days"])
_add("time", "weeks", 10080, ["week", "weeks"])
_add("pressure", "bar", 1, ["bar"])
_add("pressure", "psi", 0.0689476, ["psi"])
_add("pressure", "kPa", 0.01, ["kpa"])
_add("pressure", "MPa", 10, ["mpa"])
_add("torque", "Nm", 1, ["nm"])
_add("temperature", "°C", 1, ["°c", "degc", "celsius"])
_add("length", "mm", 1, ["mm"])
_add("length", "cm", 10, ["cm"])
_add("length", "m", 1000, ["metre", "metres", "meter", "meters"])
_add("volume", "ml", 0.001, ["ml"])
_add("volume", "litres", 1, ["l", "ltr", "litre", "litres", "liter", "liters"])
_add("speed", "rpm", 1, ["rpm"])
_add("mass", "kg", 1, ["kg"])

NUMBER_WORDS = {
    "one": 1, "two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
    "eleven": 11, "twelve": 12, "fifteen": 15, "twenty": 20, "thirty": 30, "forty": 40, "fifty": 50, "sixty": 60,
}
_NUM = r"\d+(?:[.,]\d+)*|" + "|".join(NUMBER_WORDS)
_UNIT = (
    r"°\s*c|(?:degrees?|deg)\s*(?:c|celsius)|n\s*[·.\-]?\s*m|"
    + "|".join(sorted((re.escape(u) for u in UNITS if u not in ("°c", "degc", "nm")), key=len, reverse=True))
)
_QUANTITY = re.compile(
    rf"(?<![\w.,])(?P<a>{_NUM})(?:\s*(?:-|–|—|to)\s*(?P<b>{_NUM}))?\s*(?P<unit>{_UNIT})(?![\w])", re.IGNORECASE
)
_SENTENCE_BREAK = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9\"'(])|[;\n]+")
_WORD = re.compile(r"[^\W_]+(?:[-./_][^\W_]+)*")

# Words that connect a claim to its subject carry no meaning of their own
_FILLER = frozenset(
    "must shall should never any all each every also only not no until before after then both about approximately "
    "least most more less than about around".split()
)

# Operating conditions that make two instructions apply to different situations: word -> (group, name)
QUALIFIERS = {
    "hydraulic": ("machine", "hydraulic"), "hydraulics": ("machine", "hydraulic"),
    "pneumatic": ("machine", "pneumatic"), "electric": ("machine", "electric"), "electrical": ("machine", "electric"),
    "hot": ("temperature", "hot"), "warm": ("temperature", "warm"), "cold": ("temperature", "cold"),
    "loaded": ("load", "loaded"), "unloaded": ("load", "unloaded"), "empty": ("load", "empty"), "full": ("load", "full"),
    "summer": ("season", "summer"), "winter": ("season", "winter"),
}


# What kind of quantity a question asks for. Without any of these cues every kind is compared.
_ASKS = {
    "time": r"\bhow long\b|\bhow (?:many|much) (?:more )?(?:seconds|minutes|mins|hours|days|weeks)\b|\b(?:seconds|minutes|mins|hours|days|weeks)\b|\bhow often\b|\binterval\b|\bduration\b",
    "pressure": r"\bwhat (?:\w+ ){0,2}pressure\b|\bhow much pressure\b|\bpressure (?:limit|setting|rating|reading)\b|\b(?:bar|psi|kpa|mpa)\b|\b(?:working|maximum|minimum|set|operating) pressure\b",
    "torque": r"\btorque\b|\bnm\b",
    "temperature": r"\btemperature\b|\bhow (?:hot|cold)\b|\bdegrees\b",
    "volume": r"\blit(?:re|er)s?\b|\bcapacity\b|\bhow much oil\b",
    "length": r"\bstroke\b|\bmm\b|\bmillimet(?:re|er)s?\b",
    "speed": r"\brpm\b|\bspeed\b",
    "mass": r"\bkg\b|\bweight\b",
}


def asked_dimensions(question: str) -> set[str]:
    return {d for d, pattern in _ASKS.items() if re.search(pattern, question.lower())}


def _stem(word: str) -> str:
    word = word.lower()
    for suffix in ("ing", "ed", "s"):
        if len(word) > 4 and word.endswith(suffix):
            word = word[: -len(suffix)]
            break
    return word[:-1] if len(word) > 4 and word.endswith("e") else word


def _number(text: str) -> float:
    text = text.lower()
    if text in NUMBER_WORDS:
        return float(NUMBER_WORDS[text])
    if re.fullmatch(r"\d{1,3}(,\d{3})+", text):
        return float(text.replace(",", ""))
    return float(text.replace(",", "."))


def _unit_key(raw: str) -> str:
    key = re.sub(r"\s+", "", raw.lower())
    if key.startswith("°") or "deg" in key:
        return "°c"
    if re.fullmatch(r"n[·.\-]?m", key):
        return "nm"
    return key


def _fmt(value: float) -> str:
    return f"{value:g}"


def extract_claims(text: str, question_stems: set[str]) -> list[dict]:
    """Quantities with a unit in the sentences of one passage, each with the words around it."""
    claims = []
    passage_stems = {_stem(w) for w in _WORD.findall(text.lower())}
    for sentence in _SENTENCE_BREAK.split(text):
        sentence = sentence.strip()
        if not sentence:
            continue
        words = [(m.start(), m.end(), m.group().lower()) for m in _WORD.finditer(sentence)]
        qualifiers = {QUALIFIERS[w][0]: QUALIFIERS[w][1] for _, _, w in words if w in QUALIFIERS}
        for match in _QUANTITY.finditer(sentence):
            unit = UNITS.get(_unit_key(match.group("unit")))
            if unit is None:
                continue
            dimension, factor, label = unit
            low = _number(match.group("a"))
            high = _number(match.group("b")) if match.group("b") else low
            if high < low:
                low, high = high, low
            if match.group("b") is None and low == 0:
                # "reads 0 bar" states a reading, not a limit to compare
                continue
            before = [w for s, e, w in words if e <= match.start()][-8:]
            after = [w for s, e, w in words if s >= match.end()][:8]
            anchor: dict[str, str] = {}
            for w in before + after:
                if w in QUALIFIERS or w in STOPWORDS or w in _FILLER or w in UNITS or _is_number(w):
                    continue
                anchor.setdefault(_stem(w), w)
            display = f"{_fmt(low)}" + (f"–{_fmt(high)}" if high != low else "") + f" {label}"
            claims.append({
                "dimension": dimension,
                "low": low * factor,
                "high": high * factor,
                "value": display,
                "sentence": sentence,
                "anchor": anchor,
                "qualifiers": qualifiers,
                "passage_stems": passage_stems,
                "relevance": len(question_stems & {_stem(w) for _, _, w in words}),
            })
    return claims


def _is_number(word: str) -> bool:
    return bool(re.fullmatch(r"\d[\d.,]*", word)) or word in NUMBER_WORDS


def _same_value(a: dict, b: dict) -> bool:
    def close(x: float, y: float) -> bool:
        return abs(x - y) <= 1e-9 + 0.005 * max(abs(x), abs(y))

    return close(a["low"], b["low"]) and close(a["high"], b["high"])


def _scopes_overlap(a: set[str], b: set[str]) -> bool:
    # An empty set is a general document: it applies to every machine
    return not a or not b or bool(a & b)


def _compare(a: dict, b: dict, question_qualifiers: dict[str, str]) -> tuple[str, list[str], float] | None:
    """How two claims of different documents relate: (outcome, differences, match) or None if they do not clash."""
    if a["dimension"] != b["dimension"] or _same_value(a, b):
        return None
    shared = set(a["anchor"]) & set(b["anchor"])
    smaller = min(len(a["anchor"]), len(b["anchor"]))
    match = len(shared) / smaller if smaller else 0.0
    if len(shared) < 2 or match < settings.CONFLICT_MATCH_REVIEW:
        return None

    issues: list[str] = []
    for group in set(a["qualifiers"]) | set(b["qualifiers"]):
        x, y = a["qualifiers"].get(group), b["qualifiers"].get(group)
        if x and y and x != y:
            issues.append(" vs ".join(sorted((x, y))))
        elif x or y:
            word, other = (x, b) if x else (y, a)
            if group not in question_qualifiers and not any(_stem(word) == s for s in other["passage_stems"]):
                issues.append(f"{word} is mentioned by one source only")
    if a["low"] <= b["high"] and b["low"] <= a["high"] and (a["low"] != a["high"] or b["low"] != b["high"]):
        issues.append("the values are overlapping ranges")

    strong = match >= settings.CONFLICT_MATCH_STRONG and len(shared) >= 3
    return (CONFLICT if strong and not issues else NEEDS_REVIEW), issues, match


def _fingerprint(dimension: str, claims: list[dict]) -> str:
    parts = sorted(f"{c['document_id']}:{c['low']:.6g}:{c['high']:.6g}" for c in claims)
    return hashlib.sha1(f"{dimension}|{'|'.join(parts)}".encode()).hexdigest()[:24]


def detect(evidence: list[dict], question: str, focus_asset_ids: list[str] | None = None, label_of=None) -> dict:
    """Findings among the document passages of one question's evidence.

    focus_asset_ids: machines the question is about; documents of other, specific machines are left out.
    Returns {"findings": [...], "superseded": [...]}; each finding has kind, topic, claims, differences, notes.
    """
    from .keyword_search import tokenize

    question_stems = {_stem(t) for t in tokenize(question) if not _is_number(t)}
    question_qualifiers = {
        QUALIFIERS[w][0]: QUALIFIERS[w][1] for w in _WORD.findall(question.lower()) if w in QUALIFIERS
    }
    focus = set(focus_asset_ids or [])
    # A sentence must share enough words with the question to count as an answer to it
    needed = max(2, min(3, len(question_stems)))
    # "At what pressure ...?" is not answered by a waiting time that happens to mention a valve
    asked = asked_dimensions(question)

    superseded, claims = [], []
    seen_superseded = set()
    for item in evidence:
        if item["type"] != "document":
            continue
        if item.get("superseded"):
            if item["document_id"] not in seen_superseded:
                seen_superseded.add(item["document_id"])
                superseded.append({"document_id": item["document_id"], "filename": item["filename"], "revision": item.get("revision")})
            continue
        assets = set(item.get("asset_ids") or [])
        if focus and assets and not (assets & focus):
            continue
        for claim in extract_claims(item["text"], question_stems):
            if claim["relevance"] < needed or (asked and claim["dimension"] not in asked):
                continue
            # A sentence for a situation the question rules out is not an alternative answer
            if any(g in claim["qualifiers"] and claim["qualifiers"][g] != q for g, q in question_qualifiers.items()):
                continue
            claim.update(
                n=item["n"], document_id=item["document_id"], filename=item["filename"], page=item.get("page"),
                section=item.get("section"), asset_ids=sorted(assets), revision=item.get("revision"),
                effective_date=item.get("effective_date"),
                source=label_of(item) if label_of else item["filename"],
            )
            key = (claim["document_id"], claim["sentence"].lower(), claim["value"])
            if key not in {(c["document_id"], c["sentence"].lower(), c["value"]) for c in claims}:
                claims.append(claim)

    # Edges between claims of different documents that clash; components of those edges are the findings
    edges: dict[int, set[int]] = {i: set() for i in range(len(claims))}
    outcome: dict[tuple[int, int], tuple[str, list[str]]] = {}
    for i, a in enumerate(claims):
        for j in range(i + 1, len(claims)):
            b = claims[j]
            if a["document_id"] == b["document_id"] or not _scopes_overlap(set(a["asset_ids"]), set(b["asset_ids"])):
                continue
            result = _compare(a, b, question_qualifiers)
            if result:
                edges[i].add(j)
                edges[j].add(i)
                outcome[(i, j)] = (result[0], result[1])

    findings, visited = [], set()
    for start in edges:
        if start in visited or not edges[start]:
            continue
        stack, component = [start], set()
        while stack:
            node = stack.pop()
            if node not in component:
                component.add(node)
                stack.extend(edges[node] - component)
        visited |= component
        pairs = [v for (i, j), v in outcome.items() if i in component and j in component]
        members = [claims[i] for i in sorted(component)]
        kind = CONFLICT if any(k == CONFLICT for k, _ in pairs) else NEEDS_REVIEW
        differences = sorted({d for _, ds in pairs for d in ds})
        shared = set.intersection(*(set(c["anchor"]) for c in members)) or set(members[0]["anchor"])
        topic = " ".join(w for s, w in members[0]["anchor"].items() if s in shared)
        notes = _notes(members)
        findings.append({
            "kind": kind,
            "topic": topic,
            "dimension": members[0]["dimension"],
            "claims": [
                {k: c[k] for k in ("n", "document_id", "filename", "page", "section", "sentence", "value", "source", "revision", "effective_date", "asset_ids")}
                for c in members
            ],
            "differences": differences,
            "notes": notes,
            "fingerprint": _fingerprint(members[0]["dimension"], members),
        })
    findings.sort(key=lambda f: (f["kind"] != CONFLICT, -len(f["claims"])))
    return {"findings": findings[:3], "superseded": superseded}


def _notes(members: list[dict]) -> list[str]:
    notes = []
    names = {c["document_id"]: c for c in members}.values()
    missing = [c["filename"] for c in names if not c["revision"]]
    if missing:
        notes.append(
            "Revision information is not recorded for " + ", ".join(f"\"{m}\"" for m in missing)
            + ", so it is unknown which is newer. Neither is assumed to be."
        )
    revisions = {c["revision"] for c in names if c["revision"]}
    if len(revisions) > 1 and not missing:
        notes.append("The sources carry different revisions, but none is marked as superseded, so neither is assumed to be current.")
    general = [c["filename"] for c in names if not c["asset_ids"]]
    specific = [c["filename"] for c in names if c["asset_ids"]]
    if general and specific:
        notes.append("A general document and a machine-specific document disagree; neither is assumed to take precedence.")
    return notes


def render(finding: dict, resolution: dict | None = None) -> str:
    """The text shown for one finding. Written entirely from stored document text and the status rules."""
    from string import ascii_uppercase

    head = "Conflicting instructions found" if finding["kind"] == CONFLICT else "Instructions that may conflict"
    lines = [f"{head}" + (f" about: {finding['topic']}" if finding["topic"] else "") + ".", ""]
    for letter, claim in zip(ascii_uppercase, finding["claims"]):
        revision = f", revision {claim['revision']}" if claim.get("revision") else ""
        quote = claim["sentence"] if len(claim["sentence"]) <= 220 else claim["sentence"][:220].rstrip() + "…"
        lines.append(f"Source {letter}: {claim['value']} [{claim['n']}] — {claim['source']}{revision}")
        lines.append(f"    \"{quote}\"")
    if finding["differences"]:
        lines += ["", "Differences in conditions: " + "; ".join(finding["differences"]) + "."]
    lines += [""] + [f"Note: {n}" for n in finding["notes"]]
    if resolution:
        when = resolution["resolved_at"].strftime("%Y-%m-%d")
        lines += [
            f"Status: Resolved by {resolution['resolved_by_name']} on {when}.",
            f"Decision: {DECISION_TEXT[resolution['decision']]}"
            + (f" ({resolution['document_name']})" if resolution.get("document_name") else ""),
            f"Note: {resolution['note']}",
            "This is a recorded decision, not a change to the documents. Check it against the approved procedure.",
        ]
    elif finding["kind"] == CONFLICT:
        lines += [CONFLICT_STATUS, CONFLICT_ACTION]
    else:
        lines += [REVIEW_STATUS, REVIEW_ACTION]
    return "\n".join(line for i, line in enumerate(lines) if line or (i and lines[i - 1]))


DECISION_TEXT = {
    "governs": "this document governs",
    "outdated": "this document is outdated",
    "both_apply": "both apply, under the conditions given in the note",
    "false_alarm": "not a real conflict",
}
