from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import hashlib
from datetime import datetime

# Imports locaux
from .models import User
from .schemas import UserCreate, UserUpdate

# ============= FONCTIONS UTILITAIRES =============

def hash_password(password: str) -> str:
    """Hasher un mot de passe avec SHA-256"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return hash_password(plain_password) == hashed_password

# ============= CRUD UTILISATEURS =============

class UserCRUD:
    """Classe pour toutes les opérations utilisateurs"""
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Récupérer un utilisateur par ID"""
        return db.query(User).filter(User.id == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Récupérer un utilisateur par email"""
        return db.query(User).filter(User.email == email.lower()).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[User]:
        """Récupérer tous les utilisateurs avec recherche optionnelle"""
        query = db.query(User)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    User.name.contains(search),
                    User.email.contains(search),
                    User.description.contains(search)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """Créer un nouvel utilisateur"""
        # Hasher le mot de passe
        hashed_password = hash_password(user_data.password)
        
        # Créer l'instance
        db_user = User(
            name=user_data.name,
            email=user_data.email.lower(),
            password_hash=hashed_password,
            description=user_data.description,
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Sauvegarder
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Mettre à jour un utilisateur"""
        db_user = UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "email" and value:
                value = value.lower()  # Email en minuscules
            setattr(db_user, field, value)
        
        # Mettre à jour la date de modification
        db_user.updated_at = datetime.utcnow()
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Supprimer un utilisateur"""
        db_user = UserCRUD.get_by_id(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        """Authentifier un utilisateur"""
        user = UserCRUD.get_by_email(db, email)
        if user and verify_password(password, user.password_hash):
            return user
        return None
    
    @staticmethod
    def set_active_status(db: Session, user_id: int, is_active: bool) -> Optional[User]:
        """Activer/désactiver un utilisateur"""
        db_user = UserCRUD.get_by_id(db, user_id)
        if db_user:
            db_user.is_active = is_active
            db_user.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(db_user)
        return db_user

