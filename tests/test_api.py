import os
os.environ["DATABASE_URL"] = "sqlite:///./test_feedback.db"
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, engine
from app.services import ai_service

client = TestClient(app)


def setup_function():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)


def fake_analysis(text):
    return {
        "sentiment": "Positive",
        "sentiment_score": 0.95,
        "positive_points": ["Helpful service"],
        "negative_points": [],
        "topics": ["service"],
        "short_summary": "Customer liked the service.",
        "improvement_suggestions": ["Keep service quality consistent"],
    }


def test_health():
    assert client.get("/health").json()["status"] == "ok"


def test_create_and_list_review(monkeypatch):
    monkeypatch.setattr(ai_service, "analyze_review", fake_analysis)
    response = client.post("/api/reviews", json={"review_text": "The service was very helpful."})
    assert response.status_code == 201
    assert response.json()["sentiment"] == "Positive"
    assert len(client.get("/api/reviews").json()) == 1


def test_analytics(monkeypatch):
    monkeypatch.setattr(ai_service, "analyze_review", fake_analysis)
    client.post("/api/reviews", json={"review_text": "Helpful support from the team."})
    data = client.get("/api/analytics").json()
    assert data["total_reviews"] == 1
    assert data["sentiment_counts"]["Positive"] == 1


def test_review_validation():
    response = client.post("/api/reviews", json={"review_text": "bad"})
    assert response.status_code == 422
