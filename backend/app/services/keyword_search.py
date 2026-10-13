"""Keyword half of hybrid search: BM25 ranking and the fusion of two rankings.

Vector search finds text that means the same as the question, but it is weak on exact strings
such as part numbers, error codes and function names ("E-204", "6205-2RS", "get_user_by_id").
BM25 ranks by the words themselves, so the two are run side by side and merged.
"""
import math
import re
from collections import Counter, defaultdict

# BM25 constants: K1 limits how much a repeated word keeps adding, B how strongly long chunks are penalised
K1 = 1.5
B = 0.75
# Reciprocal rank fusion constant; 60 is the value from the original paper
RRF_C = 60

STOPWORDS = frozenset(
    "a an and are as at be but by can do does for from how i if in into is it its me my of on or our "
    "so than that the their them then there these they this to was we were what when where which who "
    "why will with you your".split()
)

# A word, or words joined by - . / _ with nothing between them (E-204, 6205-2RS, get_user_by_id, v1.2)
_WORD = re.compile(r"[^\W_]+(?:[-./_][^\W_]+)*")
_JOINT = re.compile(r"[-./_]")
# Japanese and Chinese are written without spaces, so a run of these characters is not one word
_CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff]+")


def _pairs(match: re.Match) -> str:
    """油圧ポンプ -> 油圧 圧ポ ポン ンプ: overlapping character pairs stand in for the words."""
    run = match.group()
    return " " + " ".join(run[i:i + 2] for i in range(max(len(run) - 1, 1))) + " "


def tokenize(text: str) -> list[str]:
    tokens = []
    for word in _WORD.findall(_CJK.sub(_pairs, text.lower())):
        parts = _JOINT.split(word)
        if len(parts) > 1:
            # Written together as well, so "E204" in a question finds "E-204" in a manual and the reverse
            tokens.append("".join(parts))
        tokens.extend(parts)
    return [t for t in tokens if t not in STOPWORDS and (len(t) > 1 or not t.isascii() or t.isdigit())]


class KeywordIndex:
    """BM25 over a fixed list of texts; results are positions in that list."""

    def __init__(self, texts: list[str]):
        counts = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(c.values()) for c in counts]
        self.average = sum(self.lengths) / len(texts) if texts else 0.0
        # term -> [(position, how often the term occurs there)]
        self.postings: dict[str, list[tuple[int, int]]] = defaultdict(list)
        for position, count in enumerate(counts):
            for term, frequency in count.items():
                self.postings[term].append((position, frequency))
        self.total = len(texts)

    def search(self, query: str, k: int) -> list[int]:
        """Positions of the k best texts, best first. Texts sharing no word with the query are left out."""
        scores: dict[int, float] = defaultdict(float)
        for term in set(tokenize(query)):
            found = self.postings.get(term)
            if not found:
                continue
            idf = math.log(1 + (self.total - len(found) + 0.5) / (len(found) + 0.5))
            for position, frequency in found:
                length = 1 - B + B * self.lengths[position] / self.average
                scores[position] += idf * frequency * (K1 + 1) / (frequency + K1 * length)
        return sorted(scores, key=scores.get, reverse=True)[:k]


def fuse(rankings: list[list[str]], k: int) -> list[str]:
    """Reciprocal rank fusion: merge rankings of ids into one, best first.

    Only positions are used, never the scores, because a cosine distance and a BM25 score
    are not on the same scale. An id ranked high in both lists beats one ranked top in a single list.
    """
    scores: dict[str, float] = defaultdict(float)
    for ranking in rankings:
        for rank, id_ in enumerate(ranking, start=1):
            scores[id_] += 1 / (RRF_C + rank)
    return sorted(scores, key=scores.get, reverse=True)[:k]
