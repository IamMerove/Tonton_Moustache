from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class MatiereBase(BaseModel):
    """Champs communs pour les matières"""
    nom_matieres: str = Field(..., min_length=2, max_length=50, description="Nom de la matière")

# ============= SCHÉMAS POUR CRÉATION =============

class MatiereCreate(MatiereBase):
    """Données requises pour créer une matière"""
    nom_matieres: str = Field(..., min_length=2, max_length=50, description="Nom de la matière")
    description_matiere: Optional[str] = Field(None, description="Description de la matière")

# ============= SCHÉMAS POUR MISE À JOUR =============

class MatiereUpdate(BaseModel):
    """Données optionnelles pour modifier une matière"""
    nom_matieres: Optional[str] = Field(None, min_length=2, max_length=50)
    description_matiere: Optional[str] = Field(None)

# ============= SCHÉMAS DE RÉPONSE =============

class MatiereResponse(BaseModel):
    """Données retournées par l'API"""
    id_matieres: int
    nom_matieres: str
    description_matiere: Optional[str]
    
    class Config:
        from_attributes = True

# ============= SCHÉMAS SPÉCIALISÉS =============

class MatierePublic(BaseModel):
    """Informations publiques d'une matière"""
    id_matieres: int
    nom_matieres: str
    description_matiere: Optional[str]
    
    class Config:
        from_attributes = True