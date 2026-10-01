from app.services.gemini_service import generate_text


def answer_question(question: str) -> str:

    prompt = f"""
Answer the following educational question.

Question:
{question}

Use the following format:

Direct Answer:
Give the answer clearly.

Explanation:
Explain the answer simply.

Example:
Give one simple example if appropriate.
"""

    return generate_text(prompt)