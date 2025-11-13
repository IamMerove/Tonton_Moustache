from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

# Imports locaux
from .schemas import SessionBase, SessionCreate, SessionResponse, SessionUpdate
from .crud import SessionCRUD

router = APIRouter()

# ============= ROUTES CRÉATION =============

@router.post("/create_session", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
def create_session(session: SessionCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle session de conversation
    
    - **titre**: Titre optionnel de la session (max 30 caractères)
    - **id_agents**: ID de l'agent IA
    - **id_etudiant**: ID de l'étudiant
    """
    return SessionCRUD.create(db, session)

# ============= ROUTES LECTURE =============

@router.get("/read_all_sessions", response_model=List[SessionResponse])
def list_sessions(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max d'éléments"),
    search: Optional[str] = Query(None, description="Recherche par titre"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des sessions
    
    - **skip**: Pagination - éléments à ignorer
    - **limit**: Pagination - nombre max d'éléments (1-1000)
    - **search**: Recherche optionnelle dans le titre
    """
    return SessionCRUD.get_all(db, skip=skip, limit=limit, search=search)

@router.get("/session/{session_id}", response_model=SessionResponse)
def get_session(session_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une session par son ID
    """
    session = SessionCRUD.get_by_id(db, session_id)
    if not session:
        raise HTTPException(
            status_code=404, 
            detail="Session non trouvée"
        )
    return session

@router.get("/student/{id_etudiant}/sessions", response_model=List[SessionResponse])
def get_student_sessions(
    id_etudiant: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Récupérer toutes les sessions d'un étudiant
    """
    return SessionCRUD.get_by_student(db, id_etudiant, skip=skip, limit=limit)

@router.get("/agent/{id_agents}/sessions", response_model=List[SessionResponse])
def get_agent_sessions(
    id_agents: int,
    skip: int = Query(0, ge=0),
    limit: int = Query(100, ge=1, le=1000),
    db: Session = Depends(get_db)
):
    """
    Récupérer toutes les sessions d'un agent
    """
    return SessionCRUD.get_by_agent(db, id_agents, skip=skip, limit=limit)

# ============= ROUTES MISE À JOUR =============

@router.put("/session/{session_id}", response_model=SessionResponse)
def update_session(
    session_id: int, 
    session_update: SessionUpdate, 
    db: Session = Depends(get_db)
):
    """
    Mettre à jour une session
    
    Seuls les champs fournis seront modifiés
    """
    updated_session = SessionCRUD.update(db, session_id, session_update)
    if not updated_session:
        raise HTTPException(
            status_code=404, 
            detail="Session non trouvée"
        )
    return updated_session

@router.post("/session/{session_id}/end", response_model=SessionResponse)
def end_session(session_id: int, db: Session = Depends(get_db)):
    """
    Terminer une session (enregistre l'heure de fin et calcule la durée)
    """
    session = SessionCRUD.end_session(db, session_id)
    if not session:
        raise HTTPException(
            status_code=404, 
            detail="Session non trouvée"
        )
    return session

# ============= ROUTES SUPPRESSION =============

@router.delete("/session/{session_id}")
def delete_session(session_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une session
    """
    success = SessionCRUD.delete(db, session_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Session non trouvée"
        )
    return {"message": "Session supprimée avec succès"}
