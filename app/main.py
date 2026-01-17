from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.api.messages import router as messages_router
from app.core.database import engine, Base
from app.middleware.rate_limiter import RateLimitMiddleware

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

@app.get("/")
def root():
    return {"status": "success", "message": "API de Nequi operativa"}