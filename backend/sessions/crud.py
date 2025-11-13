from sqlalchemy.orm import Session
from sqlalchemy import or_, desc
from typing import List, Optional
from datetime import datetime, time

# Imports locaux
from .models import SessionConversation
from .schemas import SessionCreate, SessionUpdate

class SessionCRUD:

    @staticmethod
    def create(db: Session, session_data: SessionCreate) -> SessionConversation:
        """Créer une nouvelle session de conversation"""
        
        # Créer l'instance
        db_session = SessionConversation(
            titre=session_data.titre,
            date_heure_debut=datetime.utcnow(),
            id_agents=session_data.id_agents,
            id_etudiant=session_data.id_etudiant,
        )
        
        # Sauvegarder
        db.add(db_session)
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def get_by_id(db: Session, session_id: int) -> Optional[SessionConversation]:
        """Récupérer une session par ID"""
        return db.query(SessionConversation).filter(
            SessionConversation.id_session == session_id
        ).first()
    
    @staticmethod
    def get_all(db: Session, skip: int = 0, limit: int = 100, search: str = None) -> List[SessionConversation]:
        """Récupérer toutes les sessions"""
        query = db.query(SessionConversation)
        
        # Recherche optionnelle
        if search:
            query = query.filter(
                or_(
                    SessionConversation.titre.contains(search),
                )
            )
        
        # Trier par date décroissante (les plus récentes d'abord)
        query = query.order_by(desc(SessionConversation.date_heure_debut))
        
        return query.offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_student(db: Session, id_etudiant: int, skip: int = 0, limit: int = 100) -> List[SessionConversation]:
        """Récupérer toutes les sessions d'un étudiant"""
        return db.query(SessionConversation).filter(
            SessionConversation.id_etudiant == id_etudiant
        ).order_by(desc(SessionConversation.date_heure_debut)).offset(skip).limit(limit).all()
    
    @staticmethod
    def get_by_agent(db: Session, id_agents: int, skip: int = 0, limit: int = 100) -> List[SessionConversation]:
        """Récupérer toutes les sessions d'un agent"""
        return db.query(SessionConversation).filter(
            SessionConversation.id_agents == id_agents
        ).order_by(desc(SessionConversation.date_heure_debut)).offset(skip).limit(limit).all()
    
    @staticmethod
    def update(db: Session, session_id: int, session_data: SessionUpdate) -> Optional[SessionConversation]:
        """Mettre à jour une session"""
        db_session = SessionCRUD.get_by_id(db, session_id)
        if not db_session:
            return None
        
        # Mettre à jour seulement les champs fournis
        update_data = session_data.dict(exclude_unset=True)
        for field, value in update_data.items():
            setattr(db_session, field, value)
        
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def end_session(db: Session, session_id: int) -> Optional[SessionConversation]:
        """Terminer une session (enregistrer l'heure de fin et calculer la durée)"""
        db_session = SessionCRUD.get_by_id(db, session_id)
        if not db_session:
            return None
        
        # Enregistrer l'heure de fin
        db_session.date_heure_fin = datetime.utcnow()
        
        # Calculer la durée si possible
        if db_session.date_heure_debut:
            delta = db_session.date_heure_fin - db_session.date_heure_debut
            # Convertir timedelta en time
            hours, remainder = divmod(int(delta.total_seconds()), 3600)
            minutes, seconds = divmod(remainder, 60)
            db_session.duree_session = time(hour=hours, minute=minutes, second=seconds)
        
        db.commit()
        db.refresh(db_session)
        return db_session
    
    @staticmethod
    def delete(db: Session, session_id: int) -> bool:
        """Supprimer une session"""
        db_session = SessionCRUD.get_by_id(db, session_id)
        if db_session:
            db.delete(db_session)
            db.commit()
            return True
        return False
