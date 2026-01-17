from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Literal, Optional

class MessageBase(BaseModel):
    # Campos obligatorios según el requerimiento [cite: 32-36]
    message_id: str = Field(..., description="Identificador único del mensaje")
    session_id: str = Field(..., description="Identificador de la sesión")
    content: str = Field(..., description="Contenido del mensaje de chat")
    timestamp: datetime = Field(..., description="Marca de tiempo en formato ISO")
    sender: Literal["user", "system"] = Field(..., description="Remitente del mensaje")

class MessageCreate(MessageBase):
    """Esquema para la recepción de nuevos mensajes (POST)"""
    pass

class MessageMetadata(BaseModel):
    """Metadatos generados durante el procesamiento [cite: 42, 117-120]"""
    word_count: int
    character_count: int
    processed_at: datetime

class MessageResponse(BaseModel):
    status: str = "success"
    data: MessageBase # Usa MessageBase si los datos de respuesta coinciden con los campos del mensaje
    metadata: MessageMetadata

    class Config:
        from_attributes = True # Esto permite que Pydantic lea modelos de SQLAlchemy