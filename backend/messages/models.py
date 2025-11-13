from sqlalchemy import Column, Integer, Text, DateTime, Enum, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base


class Message(Base):
    __tablename__ = "message"

    id_message = Column(Integer, primary_key=True, index=True, autoincrement=True)
    role = Column(Enum('etudiant', 'assistant', name='role_enum'), nullable=False)
    contenu = Column(Text, nullable=False)
    date_envoi = Column(DateTime, nullable=False, server_default=func.now())
    id_session = Column(Integer, ForeignKey("session_conversation.id_session"), nullable=False)

    # Relation optionnelle vers la session (si présent dans le modèle session_conversation)
    session = relationship("SessionConversation", back_populates="messages", lazy="joined")
