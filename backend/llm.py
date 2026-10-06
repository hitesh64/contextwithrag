"""Google Gemini client."""
import time
from functools import lru_cache

from google import genai
from google.genai import errors, types

from .config import settings

SYSTEM_PROMPT = """You are 'Repo-Sensei', a Senior Software Architect and Technical Lead.
Analyze the provided context (which may include source code, requirements, or documentation) to answer the user's question.

RULES:
1. Use professional technical language.
2. Use markdown code blocks for any code snippets.
3. If the answer isn't in the document context or the conversation, clearly state that the provided files do not contain that information.
4. If analyzing a PDF/Doc, summarize key points clearly.
5. Use RECENT CONVERSATION to resolve follow-up questions, and LONG-TERM MEMORY only when it is relevant to the question.
"""

_SKIP = ("image", "tts", "live", "embedding", "audio")


class LLMError(Exception):
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


def _generate(model: str, prompt: str) -> str:
    config = types.GenerateContentConfig(system_instruction=SYSTEM_PROMPT, temperature=0.3)
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


def generate(prompt: str) -> str:
    if not settings.GOOGLE_API_KEY:
        raise LLMError("GOOGLE_API_KEY is not configured. Add it to the .env file and restart the server.")
    try:
        try:
            return _generate(settings.GEMINI_MODEL, prompt)
        except errors.ClientError as e:
            if e.code != 404:
                raise
            return _generate(_fallback_model(), prompt)
    except errors.APIError as e:
        raise LLMError(f"Gemini API error ({e.code}): {e.message}") from e
