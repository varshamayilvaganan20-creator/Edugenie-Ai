from app.schemas.models import QuizResponse
from app.services.gemini_service import generate_structured


def generate_quiz(text: str) -> QuizResponse:

    prompt = f"""
Create exactly 3 multiple-choice questions
from the educational passage below.

Rules:

1. Create exactly 3 questions.
2. Every question must have exactly 4 options.
3. Only one option must be correct.
4. The correct_answer must exactly match
   one of the four options.
5. Questions must be based on the passage.
6. Questions should test understanding.
7. Keep the questions suitable for students.

Passage:

{text}
"""

    return generate_structured(
        prompt,
        QuizResponse
    )