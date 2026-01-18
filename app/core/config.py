from fastapi import Security, HTTPException, status
from fastapi.security.api_key import APIKeyHeader


# Configuración de autenticación por API Key
API_KEY = "nequi-secret-2026"           # Valor de la API Key
API_KEY_NAME = "X-API-Key"              # Nombre del header esperado
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key_header: str = Security(api_key_header)):
    """
    Valida la API Key enviada en el header de la petición.
    Lanza un error 401 si la clave es incorrecta o falta.
    """
    if api_key_header == API_KEY:
        return api_key_header
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de API inválidas"
    )