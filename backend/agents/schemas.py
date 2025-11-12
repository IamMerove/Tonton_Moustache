from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class AgentBase(BaseModel):
    """Champs communs pour les agents """
 
    id_agent : int = Field(...,description="ID de l'agent")
    nom_agent : str = Field(...,min_length=2, max_length=100, description="Nom de l'agent")
    type_agent : str = Field(...,min_length=2, max_length=50, description="Type de l'agent")
    avatar_agent: str = Field(...,min_length=2, max_length=255, description="URL de l'avatar de l'agent")
    est_actif: bool = Field(default=False, description="Indique si l'agent est actif")
    description: str = Field(...,min_length=2, max_length=255, description="Description de l'agent")
   

# ============= SCHÉMAS POUR CRÉATION =============

class AgentCreate(AgentBase):
    """Données requises pour créer un agent"""
    
    prompt_system: str= Field(...,description="Prompt system de l'agent")
    model : str = Field(...,min_length=2, max_length=50, description="Modele de l'agent")
    temperature : float =Field(...,description="Parametre de la temperature pour la generation")
    max_tokens :int =Field(...,description="Nombre maximum de tokens")
    top_p:float= Field(...,description="Top P pour le filtrage des tokens")
    reasoning_effort:int= Field(..., description="Niveau d'effort")
    id_matieres: int=Field(..., description="ID des matières associées")

# ============= SCHÉMAS POUR MISE À JOUR =============

class AgentUpdate(BaseModel):
    """Données optionnelles pour modifier un étudiant"""
    nom: Optional[str] = Field(None, min_length=2, max_length=50)
    prenom: Optional[str] = Field(None, min_length=2, max_length=50)
    email: Optional[str] = None
    avatar: Optional[str] = Field(None, max_length=255)
    id_niveau: Optional[int] = None
    id_role: Optional[int] = None
    consentement_rgpd: Optional[bool] = None

# ============= SCHÉMAS DE RÉPONSE =============

class AgentResponse(AgentBase):
    """Données retournées par l'API"""
    id_etudiant: int
    date_inscription: datetime
    consentement_rgpd: bool
    
    class Config:
        from_attributes = True

# ============= SCHÉMAS SPÉCIALISÉS =============

class AgentLogin(BaseModel):
    """Schéma pour la connexion"""
    email: str = Field(..., description="Email de connexion")
    password: str = Field(..., min_length=6)

class AgentPublic(BaseModel):
    """Informations publiques d'un étudiant"""
    id_etudiant: int
    nom: str
    prenom: str
    avatar: Optional[str] = None
    id_niveau: int
    date_inscription: datetime
    
    class Config:
        from_attributes = True