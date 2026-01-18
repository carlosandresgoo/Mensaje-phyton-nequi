from sqlalchemy.orm import Session
from ..models.message import MessageModel
from typing import List


class MessageRepository:
    """
    Repositorio para operaciones de persistencia y consulta de mensajes en la base de datos.
    """
    @staticmethod
    def save(db: Session, message_data: dict):
        """
        Persiste el mensaje y sus metadatos en SQLite.
        """
        db_message = MessageModel(
            message_id=message_data["data"].message_id,
            session_id=message_data["data"].session_id,
            content=message_data["data"].content,
            timestamp=message_data["data"].timestamp,
            sender=message_data["data"].sender,
            metadata_info=message_data["metadata"]
        )
        db.add(db_message)
        db.commit()
        db.refresh(db_message)

        return {
            "status": "success",
            "data": db_message,
            "metadata": db_message.metadata_info
        }

    @staticmethod
    def get_messages(db: Session, session_id: str, sender: str = None, skip: int = 0, limit: int = 10):
        """
        Recupera mensajes filtrados por sesión y opcionalmente por remitente.
        Permite paginación con skip y limit.
        """
        query = db.query(MessageModel).filter(MessageModel.session_id == session_id)

        if sender:
            query = query.filter(MessageModel.sender == sender)

        db_messages = query.offset(skip).limit(limit).all()

        return [
            {
                "status": "success",
                "data": msg,
                "metadata": msg.metadata_info
            } for msg in db_messages
        ]

    @staticmethod
    def search(db: Session, session_id: str = None, sender: str = None, query: str = None, skip: int = 0, limit: int = 20):
        """
        Implementa búsqueda avanzada con filtros opcionales por sesión, remitente y contenido.
        Permite paginación con skip y limit.
        Si no se especifica session_id, busca globalmente.
        """
        filters = []
        if session_id:
            filters.append(MessageModel.session_id == session_id)
        if sender:
            filters.append(MessageModel.sender == sender)
        if query:
            # Implementación de búsqueda parcial (LIKE) para palabras clave
            filters.append(MessageModel.content.ilike(f"%{query}%"))

        db_messages = db.query(MessageModel).filter(*filters).offset(skip).limit(limit).all()

        # Consistencia en el formato de salida para el Front-end
        return [
            {
                "status": "success",
                "data": msg,
                "metadata": msg.metadata_info 
            } for msg in db_messages
        ]