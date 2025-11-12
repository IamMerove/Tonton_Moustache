from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

# ============= MODÈLE NIVEAUX =============
class Niveau(Base):
    __tablename__ = "niveaux"
    
    id_niveau= Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom_niveau = Column(String(50), nullable=False)
