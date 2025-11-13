from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime


# Schéma de base commun
class RoleBase(BaseModel):
    """Champs communs pour les roles"""
    nom_role: str = Field(..., min_length=2, max_length=50, description="Role de l'utilisateur")


# Schéma pour création d'un role avec validation de champ
class RoleCreate(RoleBase):
    """Données requises pour créer un role"""
    nom_role: str = Field(..., min_length=2, max_length=50, description="Role de l'utilisateur")



# Schéma pour la mise a jour des roles
class RoleUpdate(BaseModel):
    """Données optionnelles pour modifier un role"""
    nom_role: Optional[str] = Field(None, min_length=2, max_length=50, description="Role de l'utilisateur")

# ============= SCHÉMAS DE RÉPONSE =============

class RoleResponse(RoleBase):
    """Données retournées par l'API"""
    id_role: int
    nom_role: Optional[str] = Field(None, min_length=2, max_length=50, description="Role de l'étudiant")

    class Config:
        from_attributes = True
