from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

class Role(Base):
    __tablename__ = "roles"
    
    id_role = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom_role = Column(String(50), nullable=False)
