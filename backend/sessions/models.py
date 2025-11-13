from sqlalchemy import Column, Integer, String, DateTime, Time, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

# ============= MODÈLE SESSION CONVERSATION =============
class SessionConversation(Base):
    __tablename__ = "session_conversation"
    
    id_session = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date_heure_debut = Column(DateTime, nullable=False, default=func.now())
    titre = Column(String(30), nullable=True)
    duree_session = Column(Time, nullable=True)
    date_heure_fin = Column(DateTime, nullable=True)
    
    # Clés étrangères
    id_agents = Column(Integer, ForeignKey("agent.id_agents"), nullable=False)
    id_etudiant = Column(Integer, ForeignKey("etudiants.id_etudiant"), nullable=False)
    
    # Relations
    agent = relationship("Agent", back_populates="sessions")
    etudiant = relationship("User", back_populates="sessions")
    # messages = relationship("Message", back_populates="session")
