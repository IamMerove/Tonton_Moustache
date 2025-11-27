from fastapi import APIRouter, HTTPException, Request
from pydantic import BaseModel
from chatbot_service import ask_groq_chatbot

router = APIRouter(prefix="/chatbot", tags=["chatbot"])

class ChatRequest(BaseModel):
    message: str
    history: list = None  # Optionnel: historique de messages

@router.post("/ask")
def ask_chatbot(request: ChatRequest):
    try:
        response = ask_groq_chatbot(request.message, request.history)
        return {"response": response}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
