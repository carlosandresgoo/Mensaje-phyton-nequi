from datetime import datetime
from app.schemas.message import MessageCreate

class MessageService:
    def __init__(self):
        self.forbidden_words = ["inapropiado", "malo"]

    def process_message(self, message: MessageCreate):
        # Filtrado simple
        content_filtered = message.content
        for word in self.forbidden_words:
            content_filtered = content_filtered.replace(word, "****")

        # Metadatos
        words = message.content.split()
        metadata = {
            "word_count": len(words),
            "character_count": len(message.content),
            "processed_at": datetime.now().isoformat()
        }
        
        # Actualizamos el contenido con el filtrado
        message.content = content_filtered

        return {
            "data": message,
            "metadata": metadata
        }

message_service = MessageService()