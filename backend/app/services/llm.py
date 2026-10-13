"""Google Gemini client: text generation and embeddings. The API key never leaves the server."""
import logging
import time
from functools import lru_cache

from google import genai
from google.genai import errors, types

from ..core.config import settings

log = logging.getLogger(__name__)

# Texts per embedding request, and the stored vector size
EMBED_BATCH = 50
EMBED_DIMENSIONS = 768
# A free API key allows roughly 100 texts per minute; when that is used up, wait and continue
EMBED_QUOTA_WAITS = (15, 25, 30)


class LLMError(Exception):
    """The model service could not be used; the message is safe to show to the user."""


class QuotaError(LLMError):
    pass


@lru_cache
def _client():
    return genai.Client(api_key=settings.GOOGLE_API_KEY)


def _require_key() -> None:
    if not settings.GOOGLE_API_KEY:
        raise LLMError("GOOGLE_API_KEY is not configured. Add it to the .env file and restart the server.")


def _generate(model: str, prompt: str, system: str, json_output: bool) -> str:
    config = types.GenerateContentConfig(
        system_instruction=system,
        temperature=0.1,
        response_mime_type="application/json" if json_output else None,
    )
    # Gemini occasionally answers 503 "high demand"; retry a couple of times before giving up
    for attempt in range(3):
        try:
            response = _client().models.generate_content(model=model, contents=prompt, config=config)
            break
        except errors.ServerError:
            if attempt == 2:
                raise
            time.sleep(2 * (attempt + 1))
    if not response.text:
        raise LLMError("The model returned an empty response (it may have been blocked by safety filters).")
    return response.text


def generate(prompt: str, system: str, json_output: bool = False) -> str:
    _require_key()
    try:
        try:
            return _generate(settings.GEMINI_MODEL, prompt, system, json_output)
        except errors.ClientError as e:
            if e.code == 429 and settings.GEMINI_BACKUP_MODEL not in ("", settings.GEMINI_MODEL):
                log.warning("Gemini refused %s (429), trying %s: %s", settings.GEMINI_MODEL, settings.GEMINI_BACKUP_MODEL, e.message)
                return _generate(settings.GEMINI_BACKUP_MODEL, prompt, system, json_output)
            raise
    except errors.APIError as e:
        if e.code == 429:
            # Google's own text names the limit (per minute, per day, tokens) and when to retry; the user gets less
            log.warning("Gemini quota refusal (429): %s", e.message)
            raise QuotaError("The request quota of the Gemini API key is used up. Try again later.") from e
        raise LLMError(f"Gemini API error ({e.code}): {e.message}") from e


def _embed_batch(texts: list[str], task: str) -> list[list[float]]:
    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIMENSIONS)
    for wait in (*EMBED_QUOTA_WAITS, None):
        try:
            result = _client().models.embed_content(model=settings.EMBEDDING_MODEL, contents=texts, config=config)
            return [e.values for e in result.embeddings]
        except errors.APIError as e:
            if wait is None or e.code not in (429, 500, 503):
                if e.code == 429:
                    raise QuotaError("The embedding quota of the Gemini API key is used up. Try again in a minute.") from e
                raise LLMError(f"Gemini API error ({e.code}): {e.message}") from e
            time.sleep(wait)


def embed(texts: list[str], task: str) -> list[list[float]]:
    """Vectors for texts. task: RETRIEVAL_DOCUMENT for stored text, RETRIEVAL_QUERY for a question."""
    _require_key()
    vectors = []
    for i in range(0, len(texts), EMBED_BATCH):
        vectors.extend(_embed_batch(texts[i:i + EMBED_BATCH], task))
    return vectors
