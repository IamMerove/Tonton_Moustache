from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.orm import Session
from typing import List, Optional
import sys
import os

# Ajouter le dossier parent au path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from database import get_db

# Imports locaux
from .schemas import UserCreate, UserUpdate, UserResponse, UserLogin, UserPublic
from .crud import UserCRUD

router = APIRouter()

# ============= ROUTES UTILISATEURS =============

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    """
    Créer un nouvel utilisateur
    
    - **name**: Nom de l'utilisateur (2-100 caractères)
    - **email**: Email valide et unique
    - **password**: Mot de passe (minimum 6 caractères)
    - **description**: Description optionnelle
    """
    # Vérifier si l'email existe déjà
    existing_user = UserCRUD.get_by_email(db, user.email)
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Cet email est déjà utilisé"
        )
    
    return UserCRUD.create(db, user)

@router.get("/", response_model=List[UserResponse])
def list_users(
    skip: int = Query(0, ge=0, description="Nombre d'éléments à ignorer"),
    limit: int = Query(100, ge=1, le=1000, description="Nombre max d'éléments"),
    search: Optional[str] = Query(None, description="Recherche par nom ou email"),
    db: Session = Depends(get_db)
):
    """
    Récupérer la liste des utilisateurs
    
    - **skip**: Pagination - éléments à ignorer
    - **limit**: Pagination - nombre max d'éléments (1-1000)
    - **search**: Recherche optionnelle dans nom/email
    """
    return UserCRUD.get_all(db, skip=skip, limit=limit, search=search)

@router.get("/{user_id}", response_model=UserResponse)
def get_user(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer un utilisateur par son ID
    """
    user = UserCRUD.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    return user

@router.put("/{user_id}", response_model=UserResponse)
def update_user(
    user_id: int, 
    user_update: UserUpdate, 
    db: Session = Depends(get_db)
):
    """
    Mettre à jour un utilisateur
    
    Seuls les champs fournis seront modifiés
    """
    updated_user = UserCRUD.update(db, user_id, user_update)
    if not updated_user:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    return updated_user

@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    """
    Supprimer un utilisateur
    """
    success = UserCRUD.delete(db, user_id)
    if not success:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    return {"message": "Utilisateur supprimé avec succès"}

# ============= ROUTES SPÉCIALISÉES =============

@router.post("/login")
def login(credentials: UserLogin, db: Session = Depends(get_db)):
    """
    Authentifier un utilisateur
    
    - **email**: Email de l'utilisateur
    - **password**: Mot de passe
    """
    user = UserCRUD.authenticate(db, credentials.email, credentials.password)
    if not user:
        raise HTTPException(
            status_code=401, 
            detail="Email ou mot de passe incorrect"
        )
    
    if not user.is_active:
        raise HTTPException(
            status_code=403, 
            detail="Compte utilisateur désactivé"
        )
    
    return {
        "message": "Connexion réussie",
        "user_id": user.id,
        "user_name": user.name
    }

@router.get("/email/{email}/exists")
def check_email_exists(email: str, db: Session = Depends(get_db)):
    """
    Vérifier si un email existe déjà
    """
    user = UserCRUD.get_by_email(db, email)
    return {"exists": user is not None}

@router.patch("/{user_id}/activate")
def activate_user(user_id: int, db: Session = Depends(get_db)):
    """Activer un compte utilisateur"""
    user = UserCRUD.set_active_status(db, user_id, True)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    return {"message": "Utilisateur activé"}

@router.patch("/{user_id}/deactivate")
def deactivate_user(user_id: int, db: Session = Depends(get_db)):
    """Désactiver un compte utilisateur"""
    user = UserCRUD.set_active_status(db, user_id, False)
    if not user:
        raise HTTPException(
            status_code=404,
            detail="Utilisateur non trouvé"
        )
    return {"message": "Utilisateur désactivé"}

@router.get("/{user_id}/public", response_model=UserPublic)
def get_user_public_info(user_id: int, db: Session = Depends(get_db)):
    """
    Récupérer les informations publiques d'un utilisateur
    """
    user = UserCRUD.get_by_id(db, user_id)
    if not user:
        raise HTTPException(
            status_code=404, 
            detail="Utilisateur non trouvé"
        )
    return user
