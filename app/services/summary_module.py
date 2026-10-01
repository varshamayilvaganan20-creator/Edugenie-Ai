from app.services.gemini_service import generate_text


def summarize_text(text: str) -> str:

    prompt = f"""
Summarize the following educational content.

Requirements:

1. Keep the important information.
2. Remove unnecessary repetition.
3. Use simple language.
4. Make it useful for exam revision.
5. Use bullet points where appropriate.

Content:

{text}
"""

    return generate_text(prompt)