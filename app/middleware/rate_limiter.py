import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict


class RateLimitMiddleware(BaseHTTPMiddleware):
    # Middleware para limitar la cantidad de peticiones por IP en un periodo de tiempo. Previene abusos y ataques de denegación de servicio (DoS).
    RATE_LIMIT_DURATION = 60  # Ventana de tiempo en segundos
    MAX_REQUESTS = 10         # Máximo de peticiones permitidas por IP

    def __init__(self, app):
        super().__init__(app)
        # Diccionario para almacenar los timestamps de las peticiones por IP
        self.request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        # Verifica si la IP ha excedido el límite de peticiones en la ventana de tiempo. Si se excede, retorna un error 429. Si no, permite continuar la petición.
        client_ip = request.client.host
        current_time = time.time()

        # Filtrar solo las peticiones dentro de la ventana de tiempo
        self.request_counts[client_ip] = [
            t for t in self.request_counts[client_ip]
            if current_time - t < self.RATE_LIMIT_DURATION
        ]

        if len(self.request_counts[client_ip]) >= self.MAX_REQUESTS:
            raise HTTPException(
                status_code=429,
                detail="Demasiadas peticiones. Límite de tasa excedido (Rate Limit)."
            )

        # Registrar la nueva petición
        self.request_counts[client_ip].append(current_time)
        return await call_next(request)
