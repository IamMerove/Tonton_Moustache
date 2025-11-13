from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime


class MessageBase(BaseModel):
    role: Literal['user', 'assistant'] = Field(..., description="'user' (étudiant) ou 'assistant' (agent)")
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
