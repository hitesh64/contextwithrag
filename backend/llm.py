"""Google Gemini client: answers, reading of photos and scanned pages, and embeddings."""
import time
from functools import lru_cache

from google import genai
from google.genai import errors, types

from .config import settings

SYSTEM_PROMPT = """You are the internal knowledge assistant of a bank. Employees ask you about the bank's own policies, circulars, procedures and operation manuals, and you answer from those documents (DOCUMENT CONTEXT).

RULES:
1. Answer only from DOCUMENT CONTEXT and the conversation. If they do not contain the answer, say clearly that the bank's documents available to the user do not cover it and that they should ask the responsible department. Never fill a gap from general banking knowledge: a rule of another bank or regulator presented as this bank's rule is a compliance risk.
2. Be exact: quote limits, amounts, deadlines, form numbers and approval levels as the documents write them. Give a procedure as a numbered list in its order.
3. Each passage states its document type and, when known, the date it took effect. If two passages disagree, the one with the later effective date applies; say that the older one is superseded and cite both.
4. Answer in the language of the user's question, whatever language the documents are written in.
5. Use RECENT CONVERSATION to resolve follow-up questions, and LONG-TERM MEMORY only when it is relevant to the question.
6. The passages in DOCUMENT CONTEXT are numbered [1], [2], ... Right after every statement taken from a passage, write that passage's number in square brackets, e.g. "Cash deposits above 50,000 need a PAN [2]." Cite only passages you actually used, never a number that is not in DOCUMENT CONTEXT, and do not cite the conversation or the memory.
7. PHOTO READING, when present, is what was read from a picture the user attached (a form, a cheque, a screen); the picture itself is attached as well. Say what you identified in it before answering.
8. Do not give customers' personal data, legal advice or investment advice; explain what the bank's documents say.
"""

PHOTO_PROMPT = """This picture was attached by a bank employee: a form, a cheque, a document or a screen. Report only what is visible, in at most 120 words:
1. What kind of document or screen it is.
2. Every relevant text, code and number exactly as written (form number, error message, fields filled in or left empty).
3. Anything visibly missing or irregular (no signature, overwriting, a field left blank).
Say so if something cannot be read. Give no advice and do not judge whether it is valid."""

PAGE_PROMPT = """Transcribe all text of this page exactly, in reading order and in its original language. Write tables as rows with " | " between the cells. Describe a diagram in one line inside square brackets. Output only the transcription; if the page has no text, output (blank)."""

_SKIP = ("image", "tts", "live", "embedding", "audio")
# A free API key allows only a few requests per minute; reading many scanned pages waits for the next minute
PAGE_QUOTA_WAITS = (20, 30, 30)


class LLMError(Exception):
    pass


class QuotaError(LLMError):
    pass


@lru_cache
def _client():
    return genai.Client(api_key=settings.GOOGLE_API_KEY)


@lru_cache
def _fallback_model() -> str:
    """Pick an available text model (Flash for speed, then Pro) if the configured one is gone."""
    names = [
        m.name for m in _client().models.list()
        if "generateContent" in (m.supported_actions or []) and not any(s in m.name for s in _SKIP)
    ]
    if not names:
        raise LLMError("No Gemini text model is available for this API key.")
    return next((n for n in names if "flash" in n), next((n for n in names if "pro" in n), names[0]))


def _generate(model: str, contents, system: str | None) -> str:
    config = types.GenerateContentConfig(system_instruction=system, temperature=0.3)
    # Gemini occasionally answers 503 "high demand"; retry a couple of times before giving up
    for attempt in range(3):
        try:
            response = _client().models.generate_content(model=model, contents=contents, config=config)
            break
        except errors.ServerError:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    if not response.text:
        raise LLMError("The model returned an empty response (it may have been blocked by safety filters).")
    return response.text


# Texts per embedding request, and the stored vector size
EMBED_BATCH = 50
EMBED_DIMENSIONS = 768
# A free API key allows roughly 100 texts per minute; when that is used up, wait and continue
EMBED_QUOTA_WAITS = (15, 25, 30)


def _embed_batch(texts: list[str], task: str) -> list[list[float]]:
    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIMENSIONS)
    for wait in (*EMBED_QUOTA_WAITS, None):
        try:
            result = _client().models.embed_content(model=settings.EMBEDDING_MODEL, contents=texts, config=config)
            return [e.values for e in result.embeddings]
        except errors.APIError as e:
            if wait is None or e.code not in (429, 500, 503):
                if e.code == 429:
                    raise LLMError("The embedding quota of the Gemini API key is used up. Try again in a minute.") from e
                raise LLMError(f"Gemini API error ({e.code}): {e.message}") from e
            time.sleep(wait)


def embed(texts: list[str], task: str) -> list[list[float]]:
    """Vectors for texts. task: RETRIEVAL_DOCUMENT for stored text, RETRIEVAL_QUERY for a question."""
    if not settings.GOOGLE_API_KEY:
        raise LLMError("GOOGLE_API_KEY is not configured. Add it to the .env file and restart the server.")
    vectors = []
    for i in range(0, len(texts), EMBED_BATCH):
        vectors.extend(_embed_batch(texts[i:i + EMBED_BATCH], task))
    return vectors


def embed_query(text: str) -> list[float]:
    return embed([text], "RETRIEVAL_QUERY")[0]


def generate(prompt: str, image: tuple[bytes, str] | None = None, system: str | None = SYSTEM_PROMPT) -> str:
    """image: (bytes, mime type) of a picture the model should look at together with the prompt."""
    if not settings.GOOGLE_API_KEY:
        raise LLMError("GOOGLE_API_KEY is not configured. Add it to the .env file and restart the server.")
    contents = [types.Part.from_bytes(data=image[0], mime_type=image[1]), prompt] if image else prompt
    try:
        try:
            return _generate(settings.GEMINI_MODEL, contents, system)
        except errors.ClientError as e:
            if e.code == 429 and settings.GEMINI_BACKUP_MODEL not in ("", settings.GEMINI_MODEL):
                return _generate(settings.GEMINI_BACKUP_MODEL, contents, system)
            if e.code != 404:
                raise
            return _generate(_fallback_model(), contents, system)
    except errors.APIError as e:
        if e.code == 429:
            raise QuotaError("The request quota of the Gemini API key is used up. Try again in a minute.") from e
        raise LLMError(f"Gemini API error ({e.code}): {e.message}") from e


def read_photo(image: bytes, mime: str) -> str:
    """What a technician's photo shows: the codes and text on it, the part, its visible condition."""
    return generate(PHOTO_PROMPT, (image, mime), system=None).strip()


def read_page(image: bytes, mime: str) -> str:
    """The text of a scanned page or a photographed document ("" for a blank page)."""
    for wait in (*PAGE_QUOTA_WAITS, None):
        try:
            text = generate(PAGE_PROMPT, (image, mime), system=None).strip()
            return "" if text == "(blank)" else text
        except QuotaError:
            if wait is None:
                raise
            time.sleep(wait)
