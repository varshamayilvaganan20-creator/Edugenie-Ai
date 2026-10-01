from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_home_page():

    response = client.get("/")

    assert response.status_code == 200

    assert "EduGenie" in response.text


def test_health():

    response = client.get(
        "/health"
    )

    assert response.status_code == 200

    data = response.json()

    assert data["status"] == "ok"


def test_home_contains_features():

    response = client.get("/")

    assert "Ask a Question" in response.text

    assert "Explain a Topic" in response.text

    assert "Generate Quiz" in response.text

    assert "Summarize Text" in response.text

    assert "Learning Path" in response.text