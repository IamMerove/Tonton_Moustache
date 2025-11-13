from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

# ============= SCHÉMAS DE BASE =============

class AgentBase(BaseModel):
    """Champs communs pour les agents"""
    nom_agent: str = Field(..., min_length=2, max_length=50, description="Nom de l'agent")
    type_agent: str = Field(..., min_length=2, max_length=50, description="Type de l'agent")
    avatar_agent: Optional[str] = Field(None, max_length=255, description="URL de l'avatar de l'agent")
    est_actif: bool = Field(default=True, description="Indique si l'agent est actif")
    description: Optional[str] = Field(None, description="Description de l'agent")
   

# ============= SCHÉMAS POUR CRÉATION =============

class AgentCreate(AgentBase):
    """Données requises pour créer un agent"""
    prompt_system: str = Field(..., description="Prompt système de l'agent")
    model: str = Field(default='openai/gpt-oss-20b', max_length=100, description="Modèle de l'agent")
    temperature: float = Field(default=0.7, ge=0.0, le=2.0, description="Paramètre de température")
    max_tokens: int = Field(default=8192, gt=0, description="Nombre maximum de tokens")
    top_p: float = Field(default=1.0, ge=0.0, le=1.0, description="Top P pour le filtrage")
    reasoning_effort: str = Field(default='medium', description="Niveau d'effort (low, medium, high)")
    id_matieres: int = Field(..., description="ID de la matière associée")

# ============= SCHÉMAS POUR MISE À JOUR =============

class AgentUpdate(BaseModel):
    """Données optionnelles pour modifier un agent"""
    nom_agent: Optional[str] = Field(None, min_length=2, max_length=50)
    type_agent: Optional[str] = Field(None, min_length=2, max_length=50)
    avatar_agent: Optional[str] = Field(None, max_length=255)
    est_actif: Optional[bool] = Field(None)
    description: Optional[str] = Field(None)
    prompt_system: Optional[str] = Field(None)
    model: Optional[str] = Field(None, max_length=100)
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    max_tokens: Optional[int] = Field(None, gt=0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    reasoning_effort: Optional[str] = Field(None)
    id_matieres: Optional[int] = Field(None)



class AgentResponse(AgentBase):
    """Données retournées par l'API"""
    id_agents: int = Field(..., description="Identifiant unique de l'agent")
    date_creation: datetime
    prompt_systeme: str
    model: str
    temperature: float
    max_tokens: int
    top_p: float
    reasoning_effort: str
    id_matieres: int
    
    class Config:
        from_attributes = True

# ============= SCHÉMAS MESSAGE IA =============

class ChatMessage(BaseModel):
    """
    Schéma pour les messages envoyés au chat IA.
    """
    content: str
    agent_id: Optional[int] = None  # Optionnel : Associe à un agent pour persistance

class MessageResponse(BaseModel):
    """
    Schéma de réponse pour un message persistant.
    """
    id: int
    content: str
    role: str  # 'user' ou 'assistant'
    agent_id: int
    created_at: Optional[str] = None

    class Config:
        from_attributes = True  # Pour SQLAlchemy compat

