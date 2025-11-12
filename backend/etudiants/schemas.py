from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class UserBase(BaseModel):
    """Champs communs pour les utilisateurs (étudiants)"""
    nom: str = Field(..., min_length=2, max_length=50, description="Nom de l'étudiant")
    prenom: str = Field(..., min_length=2, max_length=50, description="Prénom de l'étudiant")
    email: str = Field(..., description="Email valide requis")
    avatar: Optional[str] = Field(None, max_length=255, description="URL de l'avatar")
    id_niveau: int = Field(..., description="Niveau scolaire de l'étudiant")
    id_role: int = Field(..., description="Rôle de l'utilisateur")

# ============= SCHÉMAS POUR CRÉATION =============

class UserCreate(UserBase):
    """Données requises pour créer un étudiant"""
    password: str = Field(..., min_length=6, description="Mot de passe (min 6 caractères)")
    consentement_rgpd: bool = Field(False, description="Consentement RGPD")

# ============= SCHÉMAS POUR MISE À JOUR =============

class UserUpdate(BaseModel):
    """Données optionnelles pour modifier un étudiant"""
    nom: Optional[str] = Field(None, min_length=2, max_length=50)
    prenom: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    avatar: Optional[str] = Field(None, max_length=255)
    id_niveau: Optional[int] = None
    id_role: Optional[int] = None
    consentement_rgpd: Optional[bool] = None

# ============= SCHÉMAS DE RÉPONSE =============

class UserResponse(UserBase):
    """Données retournées par l'API"""
    id_etudiant: int
    date_inscription: datetime
    consentement_rgpd: bool
    
    class Config:
        from_attributes = True

# ============= SCHÉMAS SPÉCIALISÉS =============

class UserLogin(BaseModel):
    """Schéma pour la connexion"""
    email: str = Field(..., description="Email de connexion")
    password: str = Field(..., min_length=6)

class UserPublic(BaseModel):
    """Informations publiques d'un étudiant"""
    id_etudiant: int
    nom: str
    prenom: str
    avatar: Optional[str] = None
    id_niveau: int
    date_inscription: datetime
    
    class Config:
        from_attributes = True