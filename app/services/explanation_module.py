from app.config import get_settings
from app.services.gemini_service import generate_text


def local_explanation(topic: str) -> str:

    from transformers import pipeline

    generator = pipeline(
        "text2text-generation",
        model="MBZUAI/LaMini-Flan-T5-783M"
    )

    result = generator(
        f"""
        Explain the following topic simply
        for a beginner.

        Topic:
        {topic}
        """,
        max_new_tokens=200,
        do_sample=False,
    )

    return result[0]["generated_text"].strip()


def explain_topic(topic: str) -> str:

    settings = get_settings()

    if settings.local_explanation:

        try:
            return local_explanation(topic)

        except Exception:
            # If local model fails,
            # automatically use Gemini.
            pass

    prompt = f"""
Explain the following topic to a beginner.

Topic:
{topic}

Use this structure:

1. What is it?
2. How does it work?
3. Simple example
4. Important points to remember
"""

    return generate_text(prompt)