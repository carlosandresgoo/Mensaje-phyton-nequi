from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.messages import router as messages_router
from app.core.database import engine, Base
from app.middleware.rate_limiter import RateLimitMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager


# Crear las tablas en la base de datos SQLite al iniciar la aplicación
Base.metadata.create_all(bind=engine)

# Instancia principal de la aplicación FastAPI
app = FastAPI(title="Mensaje-Nequi API")

# Registrar el middleware de limitación de tasa (rate limiting)
app.add_middleware(RateLimitMiddleware)

# Registrar las rutas de la API REST
app.include_router(messages_router)

# Manejo global de errores para devolver respuestas uniformes
@app.exception_handler(Exception)
# Captura excepciones no manejadas y retorna un error con formato estándar.
async def global_exception_handler(request: Request, exc: Exception):
    return JSONResponse(
        status_code=400,
        content={
            "status": "error",
            "error": {
                "code": "BAD_REQUEST",
                "message": "Error en la solicitud",
                "details": str(exc)
            }
        }
    )

# Endpoint WebSocket para actualizaciones de mensajes en tiempo real
@app.websocket("/ws/messages")
# Permite a los clientes conectarse vía WebSocket y recibir mensajes en tiempo real. Cada mensaje recibido se retransmite a todos los clientes conectados (broadcast).
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Enviar el mensaje a todos los clientes conectados
            await manager.broadcast({"event": "new_message", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

# Endpoint raíz para verificación de estado
@app.get("/")
# Retorna un mensaje de estado para verificar que la API está operativa.
def root():
    return {"status": "success", "message": "API de Nequi operativa"}