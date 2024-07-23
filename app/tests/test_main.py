from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Welcome to the PDF Chatbot API"}

def test_upload_pdf():
    with open("tests/sample.pdf", "rb") as f:
        response = client.post("/upload_pdf/", files={"file": f})
    assert response.status_code == 200
    assert "session_id" in response.json()

def test_query_pdf():
    with open("tests/sample.pdf", "rb") as f:
        upload_response = client.post("/upload_pdf/", files={"file": f})
    
    session_id = upload_response.json()["session_id"]
    query_response = client.post("/query/", json={"query": "What is the PDF about?", "session_id": session_id})
    
    assert query_response.status_code == 200
    assert "response" in query_response.json()