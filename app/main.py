from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app.config import settings
from app.services.qna import answer_question
from app.services.explanation_module import explain_topic
from app.services.quiz_module import generate_quiz
from app.services.summary_module import summarize_text
from app.services.learning_path import recommend_learning_path


# ============================================================
# EduGenie FastAPI Application
# ============================================================

app = FastAPI(
    title="EduGenie - AI Learning Assistant",
    description="Google Gemini powered educational assistant",
    version="1.0.0",
)


# ============================================================
# Static Files and Templates
# ============================================================

app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static"
)

templates = Jinja2Templates(
    directory="templates"
)


# ============================================================
# Home Page
# ============================================================

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
   return templates.TemplateResponse(
    request=request,
    name="index.html",
    context={"request": request}
)


# ============================================================
# Health Check
# ============================================================

@app.get("/health")
async def health():
    return {
        "status": "ok",
        "service": "EduGenie"
    }


# ============================================================
# Helper Function
# ============================================================

def error_response(error: Exception):
    """
    Convert backend/API errors into JSON.

    This prevents the frontend from receiving
    plain-text 'Internal Server Error' responses.
    """

    error_message = str(error)

    # Gemini temporarily unavailable
    if "503" in error_message or "UNAVAILABLE" in error_message:

        return JSONResponse(
            status_code=503,
            content={
                "detail": (
                    "Google Gemini is temporarily busy. "
                    "Please try again in a few seconds."
                )
            }
        )

    # Gemini invalid request
    if "400" in error_message or "INVALID_ARGUMENT" in error_message:

        return JSONResponse(
            status_code=400,
            content={
                "detail": (
                    "Gemini rejected the request. "
                    "Please check the input and model configuration."
                )
            }
        )

    # Gemini authentication/API key problem
    if "401" in error_message or "UNAUTHENTICATED" in error_message:

        return JSONResponse(
            status_code=401,
            content={
                "detail": (
                    "Gemini API authentication failed. "
                    "Please check your GEMINI_API_KEY."
                )
            }
        )

    # Gemini permission problem
    if "403" in error_message or "PERMISSION_DENIED" in error_message:

        return JSONResponse(
            status_code=403,
            content={
                "detail": (
                    "Gemini API access was denied. "
                    "Please check your API key and permissions."
                )
            }
        )

    # Gemini model not found
    if "404" in error_message or "NOT_FOUND" in error_message:

        return JSONResponse(
            status_code=404,
            content={
                "detail": (
                    "The configured Gemini model was not found. "
                    "Please check GEMINI_MODEL in the .env file."
                )
            }
        )

    # General error
    return JSONResponse(
        status_code=500,
        content={
            "detail": (
                "EduGenie encountered an unexpected error. "
                "Please try again."
            )
        }
    )


# ============================================================
# Q&A
# ============================================================

@app.post("/qa")
async def qa(request: dict):

    try:

        text = request.get("text", "").strip()

        if not text:

            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Please enter a question."
                }
            )

        answer = answer_question(text)

        return {
            "answer": answer
        }

    except Exception as error:

        return error_response(error)


# ============================================================
# Explain Topic
# ============================================================

@app.post("/explain")
async def explain(request: dict):

    try:

        text = request.get("text", "").strip()

        if not text:

            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Please enter a topic to explain."
                }
            )

        explanation = explain_topic(text)

        return {
            "explanation": explanation
        }

    except Exception as error:

        return error_response(error)


# ============================================================
# Quiz
# ============================================================

@app.post("/quiz")
async def quiz(request: dict):

    try:

        text = request.get("text", "").strip()

        if not text:

            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Please enter a topic for the quiz."
                }
            )

        quiz_result = generate_quiz(text)

        return quiz_result

    except Exception as error:

        return error_response(error)


# ============================================================
# Summary
# ============================================================

@app.post("/summarize")
async def summarize(request: dict):

    try:

        text = request.get("text", "").strip()

        if not text:

            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Please enter content to summarize."
                }
            )

        summary = summarize_text(text)

        return {
            "summary": summary
        }

    except Exception as error:

        return error_response(error)


# ============================================================
# Learning Recommendations
# ============================================================

@app.post("/learn/recommendations")
async def learning_recommendations(request: dict):

    try:

        text = request.get("text", "").strip()

        if not text:

            return JSONResponse(
                status_code=400,
                content={
                    "detail": "Please enter a subject or skill."
                }
            )

        recommendations = recommend_learning_path(text)

        return recommendations

    except Exception as error:

        return error_response(error)


# ============================================================
# Run Information
# ============================================================

@app.get("/api/info")
async def api_info():

    return {
        "application": "EduGenie",
        "version": "1.0.0",
        "ai_model": settings.gemini_model,
        "features": [
            "Question Answering",
            "Topic Explanation",
            "AI Quiz Generation",
            "Text Summarization",
            "Learning Path Recommendations"
        ]
    }