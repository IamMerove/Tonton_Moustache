from sqlalchemy.orm import Session
from sqlalchemy import or_
from typing import List, Optional
import bcrypt
from datetime import datetime

# Imports locaux
from .models import User
from .schemas import UserCreate, UserUpdate

# ============= FONCTIONS UTILITAIRES =============

def hash_password(password: str) -> str:
    """Hasher un mot de passe avec bcrypt (compatible avec PHP password_hash)"""
    # Générer le salt et hasher le mot de passe
    salt = bcrypt.gensalt()
    hashed = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed.decode('utf-8')

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifier un mot de passe"""
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))

# ============= CRUD UTILISATEURS =============

class UserCRUD:
    """Classe pour toutes les opérations utilisateurs"""
    
    @staticmethod
    def get_by_id(db: Session, user_id: int) -> Optional[User]:
        """Récupérer un étudiant par ID"""
        return db.query(User).filter(User.id_etudiant == user_id).first()
    
    @staticmethod
    def get_by_email(db: Session, email: str) -> Optional[User]:
        """Récupérer un étudiant par email"""
        return db.query(User).filter(User.email == email.lower()).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[User]:
        """Récupérer tous les étudiants avec recherche optionnelle"""
        query = db.query(User)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    User.nom.contains(search),
                    User.prenom.contains(search),
                    User.email.contains(search)
                )
            )
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def create(db: Session, user_data: UserCreate) -> User:
        """Créer un nouvel étudiant"""
        # Hasher le mot de passe
        hashed_password = hash_password(user_data.password)
        
        # Créer l'instance
        db_user = User(
            nom=user_data.nom,
            prenom=user_data.prenom,
            email=user_data.email.lower(),
            avatar=user_data.avatar,
            passwordhash=hashed_password,
            date_inscription=datetime.utcnow(),
            consentement_rgpd=user_data.consentement_rgpd,
            id_niveau=user_data.id_niveau,
            id_role=user_data.id_role
        )
        
        # Sauvegarder
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def update(db: Session, user_id: int, user_data: UserUpdate) -> Optional[User]:
        """Mettre à jour un étudiant"""
        db_user = UserCRUD.get_by_id(db, user_id)
        if not db_user:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = user_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            if field == "email" and value:
                value = value.lower()  # Email en minuscules
            setattr(db_user, field, value)
        
        db.commit()
        db.refresh(db_user)
        return db_user
    
    @staticmethod
    def delete(db: Session, user_id: int) -> bool:
        """Supprimer un étudiant"""
        db_user = UserCRUD.get_by_id(db, user_id)
        if db_user:
            db.delete(db_user)
            db.commit()
            return True
        return False
    
    @staticmethod
    def authenticate(db: Session, email: str, password: str) -> Optional[User]:
        """Authentifier un étudiant"""
        user = UserCRUD.get_by_email(db, email)
        if user and verify_password(password, user.passwordhash):
            return user
        return None
    
    @staticmethod
    def set_rgpd_consent(db: Session, user_id: int, consent: bool) -> Optional[User]:
        """Définir le consentement RGPD"""
        db_user = UserCRUD.get_by_id(db, user_id)
        if db_user:
            db_user.consentement_rgpd = consent
            db.commit()
            db.refresh(db_user)
        return db_user

