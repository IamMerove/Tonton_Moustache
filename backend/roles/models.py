from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

# ============= MODÈLE ROLE =============
class Role(Base):
    __tablename__ = "role"  # Nom de table au singulier pour correspondre aux Foreign Keys
    
    id_role = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom_role = Column(String(50), nullable=False, unique=True)
    
    # Relation inverse : tous les étudiants avec ce rôle
    etudiants = relationship("User", back_populates="role")
