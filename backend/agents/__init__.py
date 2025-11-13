"""Package agents: exports utiles pour importer le module agents depuis l'application.

Exemple d'utilisation dans main.py:
	from agents import router as agents_router
"""

from .agents_routes import router
from .models import Agent
from .schemas import AgentCreate, AgentUpdate
from .crud import AgentCRUD

__all__ = [
	"router",
	"Agent",
	"AgentCreate",
	"AgentUpdate",
	"AgentCRUD",
]
