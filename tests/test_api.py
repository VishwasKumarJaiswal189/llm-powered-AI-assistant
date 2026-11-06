from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)

def test_home_ui():
    response = client.get("/")
    assert response.status_code == 200
    assert "LLM AI Assistant" in response.text

@patch("app.services.llm.llm_service.generate_response")
def test_chat_endpoint(mock_generate):
    mock_generate.return_value = "Blue is a wonderful color!"
    payload = {"message": "What is my favorite color?", "session_id": "test_session"}
    response = client.post("/chat", json=payload)
    
    assert response.status_code == 200
    data = response.json()
    assert data["session_id"] == "test_session"
    assert data["response"] == "Blue is a wonderful color!"

def test_history_endpoint():
    response = client.get("/history/test_session")
    assert response.status_code == 200
    assert "messages" in response.json()