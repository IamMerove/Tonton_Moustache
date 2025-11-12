from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import bcrypt
from datetime import datetime

# Imports locaux
from .models import Agent
from .schemas import AgentCreate, AgentUpdate



# ============= CRUD UTILISATEURS =============

class AgentCRUD:
    """Classe pour toutes les opérations de l'agent"""
    
    @staticmethod
    def get_by_id(db: Session, agent_id: int) -> Optional[Agent]:
        """Récupérer un agent par ID"""
        return db.query(Agent).filter(Agent.id_agent == agent_id).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Agent]:
        """Récupérer tous les agent avec recherche optionnelle"""
        query = db.query(Agent)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    Agent.nom_agent.contains(search),
                    Agent.type_agent.contains(search),
                    Agent.date_creation.contains(search),
                    Agent.model.contains(search)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, agent_data: AgentCreate) -> Agent:
        """Créer un nouvel agent"""
        
        # Créer l'instance
        db_Agent = Agent(
        
            id_agent =agent_data.id_agent,
            nom_agent =agent_data.nom_agent,
            type_agent =agent_data.type_agent,
            avatar_agent = agent_data.avatar_agent,
            est_actif = agent_data.est_actif,
            date_creation = agent_data.date_creation,
            prompt_system = agent_data.prompt_system,
            model = agent_data.model,
            temperature = agent_data.temperature,
            max_tokens = agent_data.max_tokoen,
            top_p=agent_data. top_p,
            reasoning_effort=agent_data.reasoning_effort,
            id_matieres=agent_data.id_matiere
        )
        
        # Sauvegarder
        db.add(db_Agent)
        db.commit()
        db.refresh(db_Agent)
        return db_Agent
    
    @staticmethod
    def update(db: Session, Agent_id: int, agent_data: AgentUpdate) -> Optional[Agent]:
        """Mettre à jour un agent"""
        db_Agent = AgentCRUD.get_by_id(db, Agent_id)
        if not db_Agent:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = agent_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "email" and value:
                value = value.lower()  # Email en minuscules
            setattr(db_Agent, field, value)
        
        db.commit()
        db.refresh(db_Agent)
        return db_Agent
    
    @staticmethod
    def delete(db: Session, Agent_id: int) -> bool:
        """Supprimer un étudiant"""
        db_Agent = AgentCRUD.get_by_id(db, Agent_id)
        if db_Agent:
            db.delete(db_Agent)
            db.commit()
            return True
        return False
    
  

