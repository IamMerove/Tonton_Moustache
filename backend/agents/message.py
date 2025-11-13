from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from database import Base  # Importe Base de ton database.py

class Message(Base):
    """
    Modèle pour les messages du chat, lié à un Agent.
    """
    __tablename__ = "messages"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(Text, nullable=False)  # Contenu du message (peut être long)
    role = Column(String(10), nullable=False)  # 'user' ou 'assistant'
    agent_id = Column(Integer, ForeignKey("agent.id_agents"), nullable=False)  # Lien vers Agent
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # Relation optionnelle : Récupère l'agent parent
    agent = relationship("Agent", back_populates="messages")

# Note : Dans agents/models.py, ajoute : from .message import Message
# Et dans database.py, assure-toi que Base inclut ce modèle (create_all le fera auto)