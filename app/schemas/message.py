from pydantic import BaseModel, Field, validator
from datetime import datetime
from typing import Literal, Optional


class MessageBase(BaseModel):
    """
    Esquema base para un mensaje de chat.
    """
    message_id: str = Field(..., description="Identificador único del mensaje")
    session_id: str = Field(..., description="Identificador de la sesión")
    content: str = Field(..., description="Contenido del mensaje de chat")
    timestamp: datetime = Field(..., description="Marca de tiempo en formato ISO")
    sender: Literal["user", "system"] = Field(..., description="Remitente del mensaje")


class MessageCreate(MessageBase):
    """
    Esquema para la recepción de nuevos mensajes (POST).
    Hereda todos los campos de MessageBase.
    """
    pass


class MessageMetadata(BaseModel):
    """
    Metadatos generados durante el procesamiento del mensaje.
    """
    word_count: int
    character_count: int
    processed_at: datetime


class MessageResponse(BaseModel):
    """
    Esquema de respuesta para un mensaje procesado y almacenado.
    Incluye el mensaje y sus metadatos.
    """
    status: str = "success"
    data: MessageBase  # Usa MessageBase si los datos de respuesta coinciden con los campos del mensaje
    metadata: MessageMetadata

    class Config:
        from_attributes = True  # Permite que Pydantic lea modelos de SQLAlchemy