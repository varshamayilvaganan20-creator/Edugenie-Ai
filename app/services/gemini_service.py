from functools import lru_cache
from typing import Type, TypeVar

from google import genai
from google.genai import types
from pydantic import BaseModel

from app.config import get_settings


T = TypeVar("T", bound=BaseModel)


SYSTEM_PROMPT = """
You are EduGenie, a friendly AI educational assistant.

Your purpose is to help students learn clearly and effectively.

Rules:

1. Give accurate educational information.
2. Use simple language whenever possible.
3. Explain difficult concepts step by step.
4. Use examples when useful.
5. Avoid unnecessary complexity.
6. Do not invent facts.
7. If information is uncertain, clearly say so.
8. Keep answers student-friendly.
"""


@lru_cache
def get_gemini_client():
    settings = get_settings()

    if not settings.gemini_api_key:
        raise RuntimeError(
            "GEMINI_API_KEY is not configured. "
            "Please add your Gemini API key to the .env file."
        )

    return genai.Client(
        api_key=settings.gemini_api_key
    )


def clean_input(text: str) -> str:
    settings = get_settings()

    return text[:settings.max_input_chars]


def generate_text(
    prompt: str,
    temperature: float = 0.3
) -> str:

    settings = get_settings()

    client = get_gemini_client()

    response = client.models.generate_content(
        model=settings.gemini_model,

        contents=(
            SYSTEM_PROMPT
            + "\n\n"
            + clean_input(prompt)
        ),

        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=2048,
        ),
    )

    result = (response.text or "").strip()

    if not result:
        raise RuntimeError(
            "Gemini returned an empty response."
        )

    return result


def generate_structured(
    prompt: str,
    schema: Type[T],
    temperature: float = 0.2
) -> T:

    settings = get_settings()

    client = get_gemini_client()

    response = client.models.generate_content(
        model=settings.gemini_model,

        contents=(
            SYSTEM_PROMPT
            + "\n\n"
            + clean_input(prompt)
        ),

        config=types.GenerateContentConfig(
            temperature=temperature,
            max_output_tokens=4096,
            response_mime_type="application/json",
            response_schema=schema,
        ),
    )

    if not response.text:
        raise RuntimeError(
            "Gemini returned an empty structured response."
        )

    return schema.model_validate_json(
        response.text
    )