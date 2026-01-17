from fastapi import APIRouter, Depends, HTTPException, Security, Query
from sqlalchemy.orm import Session
from typing import List
from ..schemas.message import MessageCreate, MessageResponse
from ..services.message_service import message_service
from ..repositories.message_repository import MessageRepository
from ..core.database import get_db
from ..core.config import get_api_key

router = APIRouter(prefix="/api", tags=["messages"])

@router.post("/messages", response_model=MessageResponse, status_code=201)
async def create_message(
    message: MessageCreate, 
    db: Session = Depends(get_db),
    api_key: str = Security(get_api_key)
):
    processed = message_service.process_message(message)
    db_message = MessageRepository.save(db, processed)
    return db_message

@router.get("/messages/{session_id}", response_model=List[MessageResponse])
async def search_messages(
    session_id: str,
    sender: str = Query(None, description="Filtrar por remitente"),
    query: str = Query(None, description="Palabra clave en el contenido"),
    skip: int = 0,
    limit: int = 20,
    db: Session = Depends(get_db),
    api_key: str = Security(get_api_key)
):
    # Lógica de búsqueda delegada al repositorio
    messages = MessageRepository.search(db, session_id, sender, query, skip, limit)
    return messages