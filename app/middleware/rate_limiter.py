import time
from fastapi import Request, HTTPException
from starlette.middleware.base import BaseHTTPMiddleware
from collections import defaultdict

class RateLimitMiddleware(BaseHTTPMiddleware):
    RATE_LIMIT_DURATION = 60  
    MAX_REQUESTS = 10 
    
    def __init__(self, app):
        super().__init__(app)
        self.request_counts = defaultdict(list)

    async def dispatch(self, request: Request, call_next):
        client_ip = request.client.host
        current_time = time.time()

        self.request_counts[client_ip] = [
            t for t in self.request_counts[client_ip] 
            if current_time - t < self.RATE_LIMIT_DURATION
        ]

        if len(self.request_counts[client_ip]) >= self.MAX_REQUESTS:
            raise HTTPException(
                status_code=429, 
                detail="Demasiadas peticiones. Límite de tasa excedido (Rate Limit)."
            )

        self.request_counts[client_ip].append(current_time)
        return await call_next(request)
