# matieres/__init__.py - Facilite l'importation du module matieres

from .matieres_routes import router
from .models import Matiere
from .schemas import MatiereCreate, MatiereUpdate, MatiereResponse, MatierePublic
from .crud import MatiereCRUD

# Export des éléments principaux
__all__ = [
    "router",
    "Matiere", 
    "MatiereCreate", 
    "MatiereUpdate", 
    "MatiereResponse", 
    "MatiereLogin", 
    "MatierePublic",
    "MatiereCRUD"
]