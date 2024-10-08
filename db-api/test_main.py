import pytest
from fastapi.testclient import TestClient
from main import app, verify_token

client = TestClient(app)

# Mock the database connection
@pytest.fixture(autouse=True)
def mock_db_connection(monkeypatch):
    def mock_cursor():
        return None
    monkeypatch.setattr("main.cursor", mock_cursor)

# Mock the verify_token function
@pytest.fixture(autouse=True)
def mock_verify_token(monkeypatch):
    def mock_verify():
        return True
    monkeypatch.setattr("main.verify_token", mock_verify)

# Test cases for each CRUD operation
def test_create_analysis():
    analysis_data = {
        "user_id": 1,
        "content": "Test content",
        "result": "Test result",
        "analysis_duration": 5.230,
        "is_satisfied": True
    }
    response = client.post("/analysis/", json=analysis_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Analysis created"}

def test_get_analyses():
    response = client.get("/analysis/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_get_analysis():
    response = client.get("/analysis/1")
    assert response.status_code == 200
    assert isinstance(response.json(), dict)

def test_update_analysis():
    analysis_data = {
        "user_id": 1,
        "content": "Updated content",
        "result": "Updated result",
        "analysis_duration": "6 seconds",
        "is_satisfied": False
    }
    response = client.put("/analysis/1", json=analysis_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Analysis updated"}

def test_delete_analysis():
    response = client.delete("/analysis/1")
    assert response.status_code == 200
    assert response.json() == {"message": "Analysis deleted"}

def test_create_article():
    article_data = {
        "source": "Test source",
        "title": "Test title",
        "content": "Test content",
        "language": "en"
    }
    response = client.post("/article/", json=article_data)
    assert response.status_code == 200
    assert response.json() == {"message": "Article created"}

def test_get_articles():
    response = client.get("/article/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_create_llm_call_log():
    log_data = {
        "model": "test_model",
        "input": "Test input",
        "output": "Test output",
        "response_time": 1.5,
        "user_satisfaction": 5
    }
    response = client.post("/llm_call_log/", json=log_data)
    assert response.status_code == 200
    assert response.json() == {"message": "LLM call log created"}

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}
