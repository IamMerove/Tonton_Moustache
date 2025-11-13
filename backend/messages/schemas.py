from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class MessageBase(BaseModel):
    role: str = Field(..., description="'user' or 'assistant'")
    contenu: str = Field(..., min_length=1, description="Texte du message")
    id_session: int = Field(..., description="ID de la session associée")


class MessageCreate(MessageBase):
    """Schéma utilisé pour créer un message"""
    pass


class MessageResponse(MessageBase):
    id_message: int
    date_envoi: Optional[datetime]

    class Config:
        from_attributes = True
