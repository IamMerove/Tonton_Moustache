from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

# Imports locaux
from .schemas import AgentCreate, AgentUpdate, AgentResponse
from .crud import AgentCRUD

router = APIRouter()

# ============= ROUTES UTILISATEURS =============

@router.post("/", response_model=AgentResponse, status_code=status.HTTP_201_CREATED)
def create_agent(agent: AgentCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel agent
    
    - **name**: Nom de l'agent (2-100 caractères)
    - **email**: Email valide et unique
    - **password**: Mot de passe (minimum 6 caractères)
    - **description**: Description optionnelle
    """
    # Vérifier si l'agent existe déjà
    existing_agent = db.query(AgentCRUD.model_class).filter_by(nom_agent=agent.nom_agent).first() \
        if hasattr(AgentCRUD, "model_class") else None
    if existing_agent:
        raise HTTPException(status_code=400, detail="Un agent avec ce nom existe déjà")
    
    return AgentCRUD.create(db, agent)

@router.get("/", response_model=List[AgentResponse])
def list_agents(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max d'éléments"),
    search: Optional[str] = Query(None, description="Recherche par nom ou email"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des agents
    
    - **skip**: Pagination - éléments à ignorer
    - **limit**: Pagination - nombre max d'éléments (1-1000)
    - **search**: Recherche optionnelle dans nom/email
    """
    return AgentCRUD.get_all(db, skip=skip, limit=limit, search=search)

@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un agent par son ID
    """
    agent = AgentCRUD.get_by_id(db, agent_id)
    if not agent:
        raise HTTPException(
            status_code=404, 
            detail="agent non trouvé"
        )
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: int, 
    agent_update: AgentUpdate, 
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un agent
    
    Seuls les champs fournis seront modifiés
    """
    updated_agent = AgentCRUD.update(db, agent_id, agent_update)
    if not updated_agent:
        raise HTTPException(
            status_code=404, 
            detail="agent non trouvé"
        )
    return updated_agent

@router.delete("/{agent_id}")
def delete_agent(agent_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un agent
    """
    success = AgentCRUD.delete(db, agent_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="agent non trouvé"
        )
    return {"message": "Agent supprimé avec succès"}


