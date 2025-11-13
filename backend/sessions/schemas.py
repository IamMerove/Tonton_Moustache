from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime, time

# ============= SCHÉMAS DE BASE =============

class SessionBase(BaseModel):
    """Champs communs pour les sessions"""
    titre: Optional[str] = Field(None, max_length=30, description="Titre de la session")
    id_agents: int = Field(..., description="ID de l'agent")
    id_etudiant: int = Field(..., description="ID de l'étudiant")

# ============= SCHÉMAS POUR CRÉATION =============

class SessionCreate(SessionBase):
    """Données requises pour créer une session"""
    pass

# ============= SCHÉMAS POUR MISE À JOUR =============

class SessionUpdate(BaseModel):
    """Données optionnelles pour modifier une session"""
    titre: Optional[str] = Field(None, max_length=30)
    duree_session: Optional[time] = Field(None, description="Durée de la session")
    date_heure_fin: Optional[datetime] = Field(None, description="Date et heure de fin")

# ============= SCHÉMAS DE RÉPONSE =============

class SessionResponse(SessionBase):
    """Données retournées par l'API"""
    id_session: int
    date_heure_debut: datetime
    duree_session: Optional[time] = None
    date_heure_fin: Optional[datetime] = None
    
    class Config:
        from_attributes = True

# ============= SCHÉMAS SPÉCIALISÉS =============

class SessionWithDetails(SessionResponse):
    """Session avec détails complets"""
    # Infos de l'agent et de l'étudiant si besoin
    pass
