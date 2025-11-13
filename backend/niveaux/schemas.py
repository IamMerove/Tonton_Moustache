from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class NiveauBase(BaseModel):
    """Champs communs pour les niveaux"""
    nom_niveau: str = Field(..., min_length=2, max_length=50, description="Nom du niveau")


# ============= SCHÉMAS POUR CRÉATION =============

class NiveauCreate(NiveauBase):
    """Données requises pour créer un niveau"""
    pass

# ============= SCHÉMAS POUR MISE À JOUR =============

class NiveauUpdate(BaseModel):
    """Données optionnelles pour modifier un niveau"""
    nom_niveau: Optional[str] = Field(None, min_length=2, max_length=50, description="Nom du niveau")

# ============= SCHÉMAS DE RÉPONSE =============

class NiveauResponse(NiveauBase):
    """Données retournées par l'API"""
    id_niveau: int
    
    class Config:
        from_attributes = True
