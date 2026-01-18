from datetime import datetime
from app.schemas.message import MessageCreate


class MessageService:
    """
    Servicio encargado de procesar mensajes: filtra palabras prohibidas y genera metadatos.
    """
    def __init__(self):
        # Lista de palabras prohibidas a filtrar
        self.forbidden_words = ["inapropiado", "malo"]

    def process_message(self, message: MessageCreate):
        """
        Filtra palabras prohibidas en el contenido y genera metadatos del mensaje.
        """
        # Filtrado simple de palabras prohibidas
        content_filtered = message.content
        for word in self.forbidden_words:
            content_filtered = content_filtered.replace(word, "****")

        # Generar metadatos del mensaje
        words = message.content.split()
        metadata = {
            "word_count": len(words),
            "character_count": len(message.content),
            "processed_at": datetime.now().isoformat()
        }

        # Actualizar el contenido con el filtrado
        message.content = content_filtered

        return {
            "data": message,
            "metadata": metadata
        }

# Instancia global del servicio de mensajes
message_service = MessageService()