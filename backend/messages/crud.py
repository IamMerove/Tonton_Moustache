from sqlalchemy.orm import Session
from typing import List, Optional

from .models import Message
from .schemas import MessageCreate


class MessageCRUD:
    """Opérations CRUD pour les messages"""

    @staticmethod
    def get_by_id(db: Session, message_id: int) -> Optional[Message]:
        return db.query(Message).filter(Message.id_message == message_id).first()

    @staticmethod
    def get_by_session(db: Session, session_id: int, skip: int = 0, limit: int = 100) -> List[Message]:
        return (
            db.query(Message)
            .filter(Message.id_session == session_id)
            .order_by(Message.date_envoi.asc())
            .offset(skip)
            .limit(limit)
            .all()
        )

    @staticmethod
    def create(db: Session, message_data: MessageCreate) -> Message:
        db_msg = Message(
            role=message_data.role,
            contenu=message_data.contenu,
            id_session=message_data.id_session,
        )
        db.add(db_msg)
        db.commit()
        db.refresh(db_msg)
        return db_msg

    @staticmethod
    def delete(db: Session, message_id: int) -> bool:
        db_msg = MessageCRUD.get_by_id(db, message_id)
        if db_msg:
            db.delete(db_msg)
            db.commit()
            return True
        return False
