from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import bcrypt
from datetime import datetime

# Imports locaux
from .models import Role
from .schemas import RoleBase, RoleCreate, RoleResponse, RoleUpdate


class RoleCRUD:

    @staticmethod
    def create(db: Session, role_data: RoleCreate) -> Role:
        """Créer un nouveau role"""
        
        # Créer l'instance
        db_role = Role(
            nom=role_data.nom,
            
        )
        
        # Sauvegarder
        db.add(db_role)
        db.commit()
        db.refresh(db_role)
        return db_role
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[Role]:
        """Récupérer tous les roles"""
        query = db.query(Role)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    Role.nom.contains(search),
                )
            )
        
        return query.offset(skip).limit(limit).all()
    

    @staticmethod
    def get_by_id(db: Session, role_id: int) -> Optional[Role]:
        """Récupérer un role par ID"""
        return db.query(Role).filter(Role.id_role == role_id).first()
    
    @staticmethod
    def update(db: Session, role_id: int, role_data: RoleUpdate) -> Optional[Role]:
        """Mettre à jour un étudiant"""
        db_role = RoleCRUD.get_by_id(db, role_id)
        if not db_role:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = role_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "nom_role" and value:
                value = value.lower()  # role en minuscules
            setattr(db_role, field, value)
        
        db.commit()
        db.refresh(db_role)
        return db_role
    
    @staticmethod
    def delete(db: Session, role_id: int) -> bool:
        """Supprimer un étudiant"""
        db_role = RoleCRUD.get_by_id(db, role_id)
        if db_role:
            db.delete(db_role)
            db.commit()
            return True
        return False