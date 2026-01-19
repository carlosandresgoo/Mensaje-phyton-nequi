from sqlalchemy import Column, String, DateTime, Integer, JSON
from ..core.database import Base


class MessageModel(Base):
    # Modelo ORM para la tabla de mensajes en la base de datos.
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)  # ID único del mensaje
    session_id = Column(String, index=True)                    # ID de la sesión
    content = Column(String)                                   # Contenido del mensaje
    timestamp = Column(DateTime)                              # Fecha y hora del mensaje
    sender = Column(String)                                   # Remitente ('user' o 'system')
    metadata_info = Column(JSON)                              # Metadatos almacenados como JSON