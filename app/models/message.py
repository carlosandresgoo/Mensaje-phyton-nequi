from sqlalchemy import Column, String, DateTime, Integer, JSON
from ..core.database import Base

class MessageModel(Base):
    __tablename__ = "messages"

    message_id = Column(String, primary_key=True, index=True)
    session_id = Column(String, index=True)
    content = Column(String)
    timestamp = Column(DateTime)
    sender = Column(String)
    # Almacenamos los metadatos como un campo JSON
    metadata_info = Column(JSON)