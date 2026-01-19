
from fastapi import WebSocket
from typing import List

class ConnectionManager:
    """
    Gestiona las conexiones WebSocket activas y permite enviar mensajes a todos los clientes conectados.
    """
    def __init__(self):
        # Lista de conexiones WebSocket activas
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        # Acepta una nueva conexión WebSocket y la agrega a la lista de conexiones activas.
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        # Elimina una conexión WebSocket de la lista de conexiones activas.
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)

    async def broadcast(self, message: dict):
        # Envía un mensaje a todos los clientes WebSocket conectados. Si una conexión falla, se elimina de la lista.
        for connection in self.active_connections[:]:  # Copia para evitar errores al eliminar
            try:
                await connection.send_json(message)
            except Exception:
                # Si la conexión está muerta, la eliminamos
                self.active_connections.remove(connection)

# Instancia global para gestionar conexiones WebSocket
manager = ConnectionManager()
