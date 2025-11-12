from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

# Imports locaux
from .schemas import NiveauBase, NiveauCreate, NiveauResponse, NiveauUpdate
from .crud import NiveauCRUD


router = APIRouter()

# Route pour la création d'un role
@router.post("/create_Niveau", response_model=NiveauResponse, status_code=status.HTTP_201_CREATED)
def create_role(niveau: NiveauCreate, db: Session = Depends(get_db)):
    """
    Créer un nouveau Niveau
    
    - **nom_niveau**: Nom du Niveau (2-100 caractères)

    """
    # Vérifier si le niveau existe déjà
    existing_niveau = NiveauCRUD.create(db, niveau.nom_niveau)
    if existing_niveau:
        raise HTTPException(
            status_code=400, 
            detail="Ce niveau est déjà utilisé"
        )
    
    return NiveauCRUD.create(db, niveau)

# Route pour renvoyer tous les niveaux
@router.get("/read_all_niveau", response_model=List[NiveauResponse])
def list_niveaux(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max d'éléments"),
    search: Optional[str] = Query(None, description="Recherche par nom"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des niveaux
    
    - **skip**: Pagination - éléments à ignorer
    - **limit**: Pagination - nombre max d'éléments (1-1000)
    - **search**: Recherche optionnelle dans nom/email
    """
    return NiveauCRUD.get_all(db, skip=skip, limit=limit, search=search)

# Route pour récupéré un role par son id
@router.get("/{role_id}", response_model=RoleResponse)
def get_role(role_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un role par son ID
    """
    role = RoleCRUD.get_by_id(db, role_id)
    if not role:
        raise HTTPException(
            status_code=404, 
            detail="Role non trouvé"
        )
    return role

@router.put("/{role_id}", response_model=RoleResponse)
def update_role(
    role_id: int, 
    role_update: RoleUpdate, 
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un role
    
    Seuls les champs fournis seront modifiés
    """
    updated_role = RoleCRUD.update(db, role_id, role_update)
    if not updated_role:
        raise HTTPException(
            status_code=404, 
            detail="Role non trouvé"
        )
    return updated_role

@router.delete("/{role_id}")
def delete_role(role_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur
    """
    success = RoleCRUD.delete(db, role_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Role non trouvé"
        )
    return {"message": "Role supprimé avec succès"}


