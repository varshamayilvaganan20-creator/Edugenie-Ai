from app.services.gemini_service import generate_text


def recommend_learning_path(topic: str):
    """
    Generate a structured learning path for the given topic.
    """

    prompt = f"""
You are EduGenie, an AI learning assistant.

Create a beginner-friendly learning path for:

{topic}

Return the response in this format:

Learning Path for: {topic}

1. Basics
- Explain what the learner should understand first.

2. Fundamentals
- List the important concepts.

3. Intermediate Level
- List the concepts to learn next.

4. Advanced Level
- List advanced concepts.

5. Practice
- Suggest practical exercises or mini projects.

6. Final Project
- Suggest one project to apply the knowledge.

7. Recommended Order
- Give a simple step-by-step order.

Keep the explanation simple and student-friendly.
Do not use complicated technical language unless necessary.
"""

    return generate_text(prompt)