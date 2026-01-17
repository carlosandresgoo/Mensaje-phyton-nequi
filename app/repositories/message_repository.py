from sqlalchemy.orm import Session
from ..models.message import MessageModel

class MessageRepository:
    @staticmethod
    def save(db: Session, message_data: dict):
        """Persiste el mensaje y sus metadatos en SQLite."""
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
        
        # Retornamos un diccionario con la estructura que espera MessageResponse
        return {
            "status": "success",
            "data": db_message,
            "metadata": db_message.metadata_info
        }

    @staticmethod
    def get_messages(db: Session, session_id: str, sender: str = None, skip: int = 0, limit: int = 10):
        """Recupera mensajes filtrados por sesión y opcionalmente por remitente."""
        query = db.query(MessageModel).filter(MessageModel.session_id == session_id)
        
        if sender:
            query = query.filter(MessageModel.sender == sender)
        
        db_messages = query.offset(skip).limit(limit).all()
        
        # Mapeo manual para asegurar que Pydantic reciba los campos correctos
        return [
            {
                "status": "success",
                "data": msg,
                "metadata": msg.metadata_info 
            } for msg in db_messages
        ]