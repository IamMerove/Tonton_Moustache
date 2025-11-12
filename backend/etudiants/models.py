from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.sql import func
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

class User(Base):
    __tablename__ = "etudiants"
    
    id_etudiant = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom = Column(String(50), nullable=False)
    prenom = Column(String(50), nullable=False)
    email = Column(String(100), unique=True, nullable=False, index=True)
    avatar = Column(String(255), nullable=True)
    passwordhash = Column(String(255), nullable=False)
    date_inscription = Column(DateTime, nullable=False, default=func.now())
    consentement_rgpd = Column(Boolean, nullable=False, default=False)
    id_niveau = Column(Integer, nullable=False)
    id_role = Column(Integer, nullable=False)