from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import bcrypt
from datetime import datetime

# Imports locaux
from .models import Matiere
from .schemas import MatiereCreate, MatiereUpdate

# ============= FONCTIONS UTILITAIRES =============

# ============= CRUD UTILISATEURS =============

class MatiereCRUD:
    """Classe pour toutes les opérations matières"""
    
    @staticmethod
    def get_by_id(db: Session, matiere_id: int) -> Optional[Matiere]:
        """Récupérer une matière par ID"""
        return db.query(Matiere).filter(Matiere.id_matieres == matiere_id).first()
    
    @staticmethod
    def get_by_name(db: Session, name: str) -> Optional[Matiere]:
        """Récupérer une matière par nom"""
        return db.query(Matiere).filter(Matiere.nom_matieres == name.lower()).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Matiere]:
        """Récupérer toutes les matières avec recherche optionnelle"""
        query = db.query(Matiere)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    Matiere.nom_matieres.contains(search)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, matiere_data: MatiereCreate) -> Matiere:
        """Créer une nouvelle matière"""
        
        # Créer l'instance
        db_matiere = Matiere(
            nom_matieres=matiere_data.nom_matieres,
            description_matiere=matiere_data.description_matiere
        )
        
        # Sauvegarder
        db.add(db_matiere)
        db.commit()
        db.refresh(db_matiere)
        return db_matiere
    
    @staticmethod
    def update(db: Session, matiere_id: int, matiere_data: MatiereUpdate) -> Optional[Matiere]:
        """Mettre à jour une matière"""
        db_matiere = MatiereCRUD.get_by_id(db, matiere_id)
        if not db_matiere:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = matiere_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "email" and value:
                value = value.lower()  # Email en minuscules
            setattr(db_matiere, field, value)
        
        db.commit()
        db.refresh(db_matiere)
        return db_matiere
    
    @staticmethod
    def delete(db: Session, matiere_id: int) -> bool:
        """Supprimer une matière"""
        db_matiere = UserCRUD.get_by_id(db, matiere_id)
        if db_matiere:
            db.delete(db_matiere)
            db.commit()
            return True
        return False
    