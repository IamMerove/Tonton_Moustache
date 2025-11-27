from fastapi import APIRouter, HTTPException, Request
import os
from pydantic import BaseModel
from chatbot_service import ask_groq_chatbot

router = APIRouter(prefix="/chatbot", tags=["chatbot"])


from sqlalchemy.orm import Session
from fastapi import Depends
from users.crud import UserCRUD
from matieres.crud import MatiereCRUD
from database import get_db

class ChatRequest(BaseModel):
    message: str
    history: list = None  # Optionnel: historique de messages
    user_id: int = None
    matiere_id: int = None


@router.post("/ask")
def ask_chatbot(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        # Récupère infos utilisateur et matière si fournis
        user = None
        matiere = None
        if request.user_id:
            user = UserCRUD.get_by_id(db, request.user_id)
        if request.matiere_id:
            matiere = MatiereCRUD.get_by_id(db, request.matiere_id)

        # Construit le prompt système personnalisé
        system_prompt = os.getenv(
            "GROQ_PROMPT",
            "Tu es un assistant éducatif. Quand tu génères un cours, structure-le avec des titres, sous-titres, listes à puces, tableaux, et utilise le markdown pour la mise en forme. Aère la présentation avec des sauts de ligne et veille à la clarté visuelle. Sois clair, pédagogique et synthétique."
        )
        if user or matiere:
            infos = []
            if user:
                infos.append(f"L'utilisateur s'appelle {user.prenom} {user.nom}.")
            if matiere:
                infos.append(f"La matière choisie est : {matiere.nom_matieres}.")
            system_prompt = system_prompt + " " + " ".join(infos)

        response = ask_groq_chatbot(request.message, request.history, system_prompt)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
