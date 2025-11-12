from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class AgentBase(BaseModel):
    """Champs communs pour les agents """
 
    nom_agent : str = Field(...,min_length=2, max_length=100, description="Nom de l'agent")
    type_agent : str = Field(...,min_length=2, max_length=50, description="Type de l'agent")
    avatar_agent: str = Field(...,min_length=2, max_length=255, description="URL de l'avatar de l'agent")
    est_actif: bool = Field(default=False, description="Indique si l'agent est actif")
    description: str = Field(...,min_length=2, max_length=255, description="Description de l'agent")
   

# ============= SCHÉMAS POUR CRÉATION =============

class AgentCreate(AgentBase):
    """Données requises pour créer un agent"""
    id_agent : int = Field(...,description="ID de l'agent")
    prompt_system: str= Field(...,description="Prompt system de l'agent")
    model : str = Field(...,min_length=2, max_length=50, description="Modele de l'agent")
    temperature : float =Field(...,description="Parametre de la temperature pour la generation")
    max_tokens :int =Field(...,description="Nombre maximum de tokens")
    top_p:float= Field(...,description="Top P pour le filtrage des tokens")
    reasoning_effort:int= Field(..., description="Niveau d'effort")
    id_matieres: int=Field(..., description="ID des matières associées")

# ============= SCHÉMAS POUR MISE À JOUR =============

class AgentUpdate(BaseModel):
    """Données optionnelles pour modifier un agent"""
    nom_agent: Optional[str] = Field(None)
    type_agent: Optional[str] = Field(None)
    avatar_agent: Optional[str] = Field(None)
    est_actif: Optional[bool] = Field(None)
    description: Optional[str] = Field(None)
    prompt_system: Optional[str] = Field(None)
    model: Optional[str] = Field(None)
    temperature: Optional[float] = Field(None)
    max_tokens: Optional[int] = Field(None)
    top_p: Optional[float] = Field(None)
    reasoning_effort: Optional[int] = Field(None)
    id_matieres: Optional[int] = Field(None)

# ============= SCHÉMAS DE RÉPONSE =============

class AgentResponse(AgentBase):
    """Données retournées par l'API"""
    id_agent: int = Field(..., description="Identifiant unique de l'agent")
    est_actif: bool
    prompt_system: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    reasoning_effort: int
    id_matieres: int
    
    class Config:
        from_attributes = True

