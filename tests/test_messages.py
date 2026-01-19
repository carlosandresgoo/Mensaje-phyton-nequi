from fastapi.testclient import TestClient
from app.main import app
import uuid

client = TestClient(app)
# Definimos el header global para los tests
HEADERS = {"X-API-Key": "nequi-secret-2026"}

def test_create_message():
    unique_id = f"msg-{uuid.uuid4()}"  # Genera un ID único cada vez
    payload = {
        "message_id": unique_id,
        "session_id": "sess-456",
        "content": "Hola, prueba técnica",
        "timestamp": "2023-06-15T14:30:00Z",
        "sender": "user"
    }
    response = client.post("/api/messages", json=payload, headers=HEADERS)
    assert response.status_code == 201

def test_get_messages():
    session_id = "sess-456"
    # Añadimos headers=HEADERS a la petición GET
    response = client.get(f"/api/messages?session_id={session_id}", headers=HEADERS)
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_unauthorized_access():
    # Prueba que sin la API Key el sistema rechaza la conexión
    session_id = "sess-456"
    response = client.get(f"/api/messages?session_id={session_id}") # Sin headers
    assert response.status_code == 401
    assert response.json()["detail"] == "Credenciales de API inválidas"