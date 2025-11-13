from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

# Imports locaux
from .schemas import MatiereCreate, MatiereUpdate, MatiereResponse, MatierePublic
from .crud import MatiereCRUD

router = APIRouter()

# ============= ROUTES UTILISATEURS =============

@router.post("/", response_model=MatiereResponse, status_code=status.HTTP_201_CREATED)
def create_matiere(matiere: MatiereCreate, db: Session = Depends(get_db)):
    """
    Créer une nouvelle matière
    
    - **nom_matieres**: Nom de la matière (2-50 caractères)
    - **description_matiere**: Description optionnelle
    """
    # Vérifier si la matière existe déjà
    existing_matiere = MatiereCRUD.get_by_name(db, matiere.nom_matieres)
    if existing_matiere:
        raise HTTPException(
            status_code=400, 
            detail="Cette matière est déjà utilisée"
        )
    
    return MatiereCRUD.create(db, matiere)

@router.get("/", response_model=List[MatiereResponse])
def list_matieres(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max d'éléments"),
    search: Optional[str] = Query(None, description="Recherche par nom"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des matières
    
    - **skip**: Pagination - éléments à ignorer
    - **limit**: Pagination - nombre max d'éléments (1-1000)
    - **search**: Recherche optionnelle dans nom
    """
    return MatiereCRUD.get_all(db, skip=skip, limit=limit, search=search)

@router.get("/{matiere_id}", response_model=MatiereResponse)
def get_matiere(matiere_id: int, db: Session = Depends(get_db)):
    """
    Récupérer une matière par son ID
    """
    matiere = MatiereCRUD.get_by_id(db, matiere_id)
    if not matiere:
        raise HTTPException(
            status_code=404, 
            detail="Matière non trouvée"
        )
    return matiere

@router.put("/{matiere_id}", response_model=MatiereResponse)
def update_matiere(
    matiere_id: int, 
    matiere_update: MatiereUpdate, 
    db: Session = Depends(get_db)
):
    """
    Mettre à jour une matière
    
    Seuls les champs fournis seront modifiés
    """
    updated_matiere = MatiereCRUD.update(db, matiere_id, matiere_update)
    if not updated_matiere:
        raise HTTPException(
            status_code=404, 
            detail="Matière non trouvée"
        )
    return updated_matiere

@router.delete("/{matiere_id}")
def delete_matiere(matiere_id: int, db: Session = Depends(get_db)):
    """
    Supprimer une matière
    """
    success = MatiereCRUD.delete(db, matiere_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Matière non trouvée"
        )
    return {"message": "Matière supprimée avec succès"}

# ============= ROUTES SPÉCIALISÉES =============

@router.get("/name/{name}/exists")
def check_name_exists(name: str, db: Session = Depends(get_db)):
    """
    Vérifier si une matière existe déjà
    """
    matiere = MatiereCRUD.get_by_name(db, name)
    return {"exists": matiere is not None}

@router.get("/{matiere_id}/public", response_model=MatierePublic)
def get_matiere_public_info(matiere_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les informations publiques d'une matière
    """
    matiere = MatiereCRUD.get_by_id(db, matiere_id)
    if not matiere:
        raise HTTPException(
            status_code=404, 
            detail="Matière non trouvée"
        )
    return matiere
