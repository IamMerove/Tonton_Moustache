<<<<<<< HEAD
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Text, Numeric, Enum
from sqlalchemy.orm import relationship
=======
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Float
>>>>>>> a3edcbb00f2e45b6da6604430f4b1385540d459d
from sqlalchemy.sql import func
import sys
import os

# Ajouter le dossier parent au path pour importer database
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import Base

class Agent(Base):
    __tablename__ = "agents"
    
    id_agent = Column(Integer, primary_key=True, index=True, autoincrement=True)
    nom_agent = Column(String(50), nullable=False)
    type_agent = Column(String(50), nullable=False)
    avatar_agent = Column(String(100), unique=True, nullable=False, index=True)
    est_actif = Column(Boolean, nullable=False, default=True)
    description = Column(String(255), nullable=False)
    date_creation = Column(DateTime, nullable=False, server_default=func.now())
    prompt_system = Column(String, nullable=False, default=False)
    model = Column(String(100), nullable=False)
    temperature = Column(Float, nullable=False, default=0.7)
    max_tokens = Column(Integer, nullable=False)
    top_p= Column(Integer, nullable=False)
    reasoning_effort=Column(Integer, nullable=False)
    id_matieres=Column(Integer, nullable=False)

    