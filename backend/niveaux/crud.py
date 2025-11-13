from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import bcrypt
from datetime import datetime

# Imports locaux
from .models import Niveau
from .schemas import NiveauBase, NiveauCreate, NiveauResponse, NiveauUpdate

class NiveauCRUD:

    @staticmethod
    def create(db: Session, niveau_data: NiveauCreate) -> Niveau:
        """Créer un nouveau niveau"""
        
        # Créer l'instance
        db_niveau = Niveau(
            nom_niveau=niveau_data.nom_niveau,
        )
        
        # Sauvegarder
        db.add(db_niveau)
        db.commit()
        db.refresh(db_niveau)
        return db_niveau
    
    @staticmethod
    def get_by_name(db: Session, nom_niveau: str) -> Optional[Niveau]:
        """Récupérer un niveau par nom"""
        return db.query(Niveau).filter(Niveau.nom_niveau == nom_niveau).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Niveau]:
        """Récupérer tous les niveaux"""
        query = db.query(Niveau)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    Niveau.nom_niveau.contains(search),
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_id(db: Session, niveau_id: int) -> Optional[Niveau]:
        """Récupérer un role par ID"""
        return db.query(Niveau).filter(Niveau.id_niveau == niveau_id).first()
    
    @staticmethod
    def update(db: Session, niveau_id: int, niveau_data: NiveauUpdate) -> Optional[Niveau]:
        """Mettre à jour un niveau"""
        db_niveau = NiveauCRUD.get_by_id(db, niveau_id)
        if not db_niveau:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = niveau_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "nom_niveau" and value:
                value = value.lower()  # niveau en minuscules
            setattr(db_niveau, field, value)
        
        db.commit()
        db.refresh(db_niveau)
        return db_niveau
    
    @staticmethod
    def delete(db: Session, niveau_id: int) -> bool:
        """Supprimer un Niveau"""
        db_niveau =   NiveauCRUD.get_by_id(db, niveau_id)
        if db_niveau:
            db.delete(db_niveau)
            db.commit()
            return True
        return False