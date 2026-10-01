from typing import List

from pydantic import BaseModel, Field, field_validator


class TextRequest(BaseModel):
    text: str = Field(
        ...,
        min_length=1,
        max_length=20000
    )

    @field_validator("text")
    @classmethod
    def validate_text(cls, value: str) -> str:
        value = value.strip()

        if not value:
            raise ValueError("Input cannot be empty.")

        return value


class QAResponse(BaseModel):
    answer: str


class ExplainResponse(BaseModel):
    explanation: str


class SummaryResponse(BaseModel):
    summary: str


class QuizQuestion(BaseModel):
    question: str

    options: List[str] = Field(
        ...,
        min_length=4,
        max_length=4
    )

    correct_answer: str


class QuizResponse(BaseModel):
    questions: List[QuizQuestion] = Field(
        ...,
        min_length=3,
        max_length=3
    )


class LearningStep(BaseModel):
    level: str

    topics: List[str]

    timeline: str

    resources: List[str]


class LearningPathResponse(BaseModel):
    topic: str

    goal: str

    steps: List[LearningStep]


class ErrorResponse(BaseModel):
    detail: str