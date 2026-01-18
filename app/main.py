from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.messages import router as messages_router
from app.core.database import engine, Base
from app.middleware.rate_limiter import RateLimitMiddleware
from fastapi import WebSocket, WebSocketDisconnect
from app.core.websocket_manager import manager

# Crea las tablas en SQLite al arrancar
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Mensaje-Nequi API")
# Registrar el middleware justo después de instanciar FastAPI
app.add_middleware(RateLimitMiddleware)

# Registrar rutas
app.include_router(messages_router)

# Manejo de errores global según el formato solicitado
@app.exception_handler(Exception)
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
@app.websocket("/ws/messages")
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            # Broadcast a todos los clientes conectados
            await manager.broadcast({"event": "new_message", "data": data})
    except WebSocketDisconnect:
        manager.disconnect(websocket)
    except Exception:
        manager.disconnect(websocket)

@app.get("/")
def root():
    return {"status": "success", "message": "API de Nequi operativa"}