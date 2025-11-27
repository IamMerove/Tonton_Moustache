from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Imports database
from database import engine, Base

# Imports des modèles
from roles.models import Role
from niveaux.models import Niveau
from matieres.models import Matiere
from agents.models import Agent
from users.models import User
from sessions.models import SessionConversation
from messages.models import Message

# Imports routers existants
from users import router as users_router
from agents.agents_routes import router as agents_router
from roles import router as roles_router
from niveaux import router as niveaux_router
from sessions import router as sessions_router
from messages.messages_routes import router as messages_router
from matieres import router as matieres_router
# Nouveau : import du router chatbot
from chatbot_routes import router as chatbot_router

# === NOUVEAU : import du router auth ===
from auth import router as auth_router

# Création des tables
Base.metadata.create_all(bind=engine)

# App
app = FastAPI(
    title="Tonton Moustache API",
    description="API de gestion d'agent IA",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Middleware CORS — OK avec authentification par cookie
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Routes de base
@app.get("/")
def read_root():
    return {
        "message": "Bienvenue sur l'API Tonton Moustache! 🍳",
        "version": "1.0.0",
        "endpoints": {
            "users": "/users/",
            "docs": "/docs",
            "redoc": "/redoc"
        }
    }

@app.get("/health")
def health_check():
    return {"status": "OK", "message": "API fonctionnelle"}

# Inclusion des routers

app.include_router(auth_router, prefix="/auth", tags=["Authentification"])
app.include_router(users_router, prefix="/users", tags=["Utilisateurs"])
app.include_router(agents_router, prefix="/agents", tags=["Agents"])
app.include_router(roles_router, prefix="/roles", tags=["Roles"])
app.include_router(niveaux_router, prefix="/niveau", tags=["Niveaux"])
app.include_router(matieres_router, prefix="/matieres", tags=["Matières"])
app.include_router(messages_router, prefix="/messages", tags=["Messages"])
app.include_router(sessions_router, prefix="/sessions", tags=["Sessions"])
# Inclusion du router chatbot
app.include_router(chatbot_router)

# Démarrage
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
