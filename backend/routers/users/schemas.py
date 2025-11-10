from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class UserBase(BaseModel):
    """Champs communs pour les utilisateurs"""
    name: str = Field(..., min_length=2, max_length=100, description="Nom de l'utilisateur")
    email: str = Field(..., description="Email valide requis")
    description: Optional[str] = Field(None, max_length=500, description="Description optionnelle")

# ============= SCHÉMAS POUR CRÉATION =============

class UserCreate(UserBase):
    """Données requises pour créer un utilisateur"""
    password: str = Field(..., min_length=6, description="Mot de passe (min 6 caractères)")

# ============= SCHÉMAS POUR MISE À JOUR =============

class UserUpdate(BaseModel):
    """Données optionnelles pour modifier un utilisateur"""
    name: Optional[str] = Field(None, min_length=2, max_length=100)
    email: Optional[str] = None
    description: Optional[str] = Field(None, max_length=500)

# ============= SCHÉMAS DE RÉPONSE =============

class UserResponse(UserBase):
    """Données retournées par l'API"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    class Config:
        from_attributes = True

# ============= SCHÉMAS SPÉCIALISÉS =============

class UserLogin(BaseModel):
    """Schéma pour la connexion"""
    email: str = Field(..., description="Email de connexion")
    password: str = Field(..., min_length=6)

class UserPublic(BaseModel):
    """Informations publiques d'un utilisateur"""
    id: int
    name: str
    description: Optional[str] = None
    created_at: datetime
    
    class Config:
        from_attributes = True