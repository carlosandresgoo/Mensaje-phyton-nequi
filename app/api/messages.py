from fastapi import APIRouter, Depends, HTTPException, Security, Query
from sqlalchemy.orm import Session
from typing import List
from ..schemas.message import MessageCreate, MessageResponse
from ..services.message_service import message_service
from ..repositories.message_repository import MessageRepository
from ..core.database import get_db
from ..core.config import get_api_key  # Asegúrate de tener esto o definirlo aquí

router = APIRouter(prefix="/api", tags=["messages"])

@router.post("/messages", response_model=MessageResponse, status_code=201)
async def create_message(
    message: MessageCreate, 
    db: Session = Depends(get_db),
    api_key: str = Security(get_api_key)
):
    # Todo esto DEBE tener 4 espacios de sangría
    processed = message_service.process_message(message)
    db_message = MessageRepository.save(db, processed)
    return db_message

@router.get("/messages/{session_id}", response_model=List[MessageResponse])
async def get_messages(
    session_id: str,
    sender: str = Query(None),
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db),
    api_key: str = Security(get_api_key)
):
    # Todo esto DEBE tener 4 espacios de sangría
    messages = MessageRepository.get_messages(db, session_id, sender, skip, limit)
    return messages