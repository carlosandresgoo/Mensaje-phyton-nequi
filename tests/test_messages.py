from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)
# Definimos el header global para los tests
HEADERS = {"X-API-Key": "nequi-secret-2026"}

def test_create_message():
    payload = {
        "message_id": "msg-123",
        "session_id": "sess-456",
        "content": "Hola, prueba técnica",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }
    # Añadimos headers=HEADERS a la petición
    response = client.post("/api/messages", json=payload, headers=HEADERS)
    assert response.status_code == 201
    assert response.json()["data"]["message_id"] == "msg-123"

def test_get_messages():
    session_id = "sess-456"
    # Añadimos headers=HEADERS a la petición GET
    response = client.get(f"/api/messages/{session_id}", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_unauthorized_access():
    """Prueba que sin la API Key el sistema rechaza la conexión"""
    response = client.get("/api/messages/sess-456") # Sin headers
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales de API inválidas"