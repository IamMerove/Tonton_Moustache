from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Numeric, Enum as SQLEnum, Float
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sys
import os


# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

class Agent(Base):
    __tablename__ = "agent"  # CORRIGÉ: singulier pour correspondre au SQL
    
    id_agents = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom_agent = Column(String(50), nullable=False, unique=True)
    type_agent = Column(String(50), nullable=False)
    avatar_agent = Column(String(255), nullable=True)
    est_actif = Column(Boolean, nullable=False, default=True)
    description = Column(Text, nullable=True)
    date_creation = Column(DateTime, nullable=False, server_default=func.now())
    prompt_systeme = Column(Text, nullable=False)  # CORRIGÉ: prompt_systeme au lieu de prompt_system
    model = Column(String(100), nullable=False, default='openai/gpt-oss-20b')
    temperature = Column(Numeric(3, 2), nullable=False, default=0.7)
    max_tokens = Column(Integer, nullable=False, default=8192)
    top_p = Column(Numeric(3, 2), nullable=False, default=1.0)
    reasoning_effort = Column(SQLEnum('low', 'medium', 'high', name='reasoning_effort_enum'), nullable=False, default='medium')
    
    # Clé étrangère vers matieres
    id_matieres = Column(Integer, ForeignKey("matieres.id_matieres"), nullable=False)
    
    # Relations
    matiere = relationship("Matiere", back_populates="agents")
    sessions = relationship("SessionConversation", back_populates="agent")

    messages = relationship("AgentMessage", back_populates="agent", cascade="all, delete-orphan")

from .message import AgentMessage
    