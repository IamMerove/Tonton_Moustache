from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
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
        return db.query(Agent).filter(Agent.id_agents == agent_id).first()  # CORRIGÉ: id_agents
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Agent]:
        """Récupérer tous les agents avec recherche optionnelle"""
        query = db.query(Agent)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    Agent.nom_agent.contains(search),
                    Agent.type_agent.contains(search),
                    Agent.model.contains(search)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, agent_data: AgentCreate) -> Agent:
        """Créer un nouvel agent"""
        
        # Créer l'instance
        db_agent = Agent(
            nom_agent=agent_data.nom_agent,
            type_agent=agent_data.type_agent,
            avatar_agent=agent_data.avatar_agent,
            est_actif=agent_data.est_actif,
            description=agent_data.description,
            prompt_systeme=agent_data.prompt_system,  # CORRIGÉ: prompt_systeme dans le modèle
            model=agent_data.model,
            temperature=agent_data.temperature,
            max_tokens=agent_data.max_tokens,  # CORRIGÉ: max_tokens
            top_p=agent_data.top_p,
            reasoning_effort=agent_data.reasoning_effort,
            id_matieres=agent_data.id_matieres  # CORRIGÉ: id_matieres
            # date_creation sera auto-généré par le server_default
        )
        
        # Sauvegarder
        db.add(db_agent)
        db.commit()
        db.refresh(db_agent)
        return db_agent
    
    @staticmethod
    def update(db: Session, agent_id: int, agent_data: AgentUpdate) -> Optional[Agent]:
        """Mettre à jour un agent"""
        db_agent = AgentCRUD.get_by_id(db, agent_id)
        if not db_agent:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = agent_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            # Mapper prompt_system vers prompt_systeme dans le modèle
            if field == "prompt_system":
                setattr(db_agent, "prompt_systeme", value)
            else:
                setattr(db_agent, field, value)
        
        db.commit()
        db.refresh(db_agent)
        return db_agent
    
    @staticmethod
    def delete(db: Session, agent_id: int) -> bool:
        """Supprimer un agent"""
        db_agent = AgentCRUD.get_by_id(db, agent_id)
        if db_agent:
            db.delete(db_agent)
            db.commit()
            return True
        return False
    
  

