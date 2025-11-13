from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Ajouter le dossier parent au path pour importer get_db
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

from .schemas import MessageCreate, MessageResponse
from .crud import MessageCRUD

router = APIRouter()  # Pas de prefix ni tags ici, définis dans main.py


@router.post("/", response_model=MessageResponse, status_code=status.HTTP_201_CREATED)
def create_message(message: MessageCreate, db: Session = Depends(get_db)):
    """Créer un message lié à une session"""
    return MessageCRUD.create(db, message)


@router.get("/session/{session_id}", response_model=List[MessageResponse])
def list_messages_by_session(
    session_id: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db),
):
    """Lister les messages d'une session de conversation"""
    return MessageCRUD.get_by_session(db, session_id, skip=skip, limit=limit)


@router.get("/{message_id}", response_model=MessageResponse)
def get_message(message_id: int, db: Session = Depends(get_db)):
    msg = MessageCRUD.get_by_id(db, message_id)
    if not msg:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    return msg


@router.delete("/{message_id}")
def delete_message(message_id: int, db: Session = Depends(get_db)):
    success = MessageCRUD.delete(db, message_id)
    if not success:
        raise HTTPException(status_code=404, detail="Message non trouvé")
    return {"message": "Message supprimé avec succès"}
